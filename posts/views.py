from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .mixins import AuthorRequiredMixin

class PostListView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = "posts"
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"

class PostCreateView(CreateView):
    model = Post
    fields = ["title", "body"]
    success_message = "Announcement published."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ["title", "body"]
    success_message = "Announcement updated."

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:home")
    http_method_names = ["post"]

    def form_valid(self, form):
        messages.success(self.request, "Announcement deleted.")
        return super().form_valid(form)
    
