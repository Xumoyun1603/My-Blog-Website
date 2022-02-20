from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
)
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    ListView, DetailView, UpdateView,
    DeleteView, CreateView,
)
from django.urls import reverse_lazy, reverse


from .forms import CommentForm
from .models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    paginate_by = 3


# class ArticleDetailView(LoginRequiredMixin, DetailView):
#     model = Article
#     template_name = 'article_detail.html'

@login_required
def article_detail_view(request, slug):
    template_name = "article_detail.html"
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.article = article
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "article": article,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'photo',)
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        return reverse('article-detail', kwargs={'slug': self.object.slug})


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'summary', 'body', 'photo', 'slug')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('article-detail', kwargs={'slug': self.object.slug})