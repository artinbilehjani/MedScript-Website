from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    DeleteView,
    UpdateView,
    TemplateView,
    ListView,
    DetailView,
    FormView,
    CreateView,
)
from django.views.generic.base import RedirectView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

from django.shortcuts import render

def index_view(request):
    return render(request, 'blog/archive-page.html') # Assuming index.html is in blog/templates/blog/



# def indexViewF(request):
#     return render(request, "index.html")


# class indexView(TemplateView):
#     template_name = "index.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["name"] = "ali"
#         context["posts"] = Post.objects.all()
#         return context




""" FBV for redirect

def redirectToGoogle(request):
    return redirect('https://google.com')
"""


class RedirectToGoogle(RedirectView):
    url = "https://www.google.com"

    def get_redirect_urls(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])

        return super().get_redirect_urls(*args, **kwargs)


class PostListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "blog.view_post"
    # model = Post
    context_object_name = "posts"
    paginate_by = 2
    ordering = "-created_date"

    def get_queryset(self):
        qs = Post.objects.filter(status=True)
        return qs.order_by(self.ordering)

class PostListApiView(TemplateView):
    template_name = 'blog/post_list_api.html'

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"


"""
class PostCreateview(FormView):
    template_name = 'contact.html'
    form_class = PostForm
    success_url = '/blog/post/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
"""


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    # success_url = '/blog/post/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        self.success_url = reverse_lazy(
            "blog:post-detail", kwargs={"pk": form.instance.pk}
        )
        return super().form_valid(form)


class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blog:post-list")


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog:post-list")
    context_object_name = "post"
