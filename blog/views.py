from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import *
from taggit.models import Tag
# Create your views here.
class TagMixin(object):
          def get_context_data(self, **kwargs):
              context = super(TagMixin, self).get_context_data(**kwargs)
              context['tags'] = Tag.objects.all()
              return context

class PostIndexView(TagMixin,ListView):
    model = Blog
    template_name = 'blog.html'
    queryset=Blog.objects.all()
    context_object_name = 'posts'

class TagIndexView(TagMixin,ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.objects.filter(tags__slug=self.kwargs.get('tag_slug'))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PostDetailView(DetailView):
    model = Blog
    context_object_name = 'post'
    template_name = 'blog-detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        ip = get_client_ip(self.request)
        print(ip)
        if IpModel.objects.filter(ip=ip).exists():
            print("ip already present")
            post_id = request.GET.get('post-id')
            print(post_id)
            post = Blog.objects.get(pk=post_id)
            post.views.add(IpModel.objects.get(ip=ip))
        else:
            IpModel.objects.create(ip=ip)
            post_id = request.GET.get('post-id')
            post = Blog.objects.get(pk=post_id)
            post.views.add(IpModel.objects.get(ip=ip))
        return self.render_to_response(context)
