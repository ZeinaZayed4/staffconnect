from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = "posts"
    paginate_by = 5
