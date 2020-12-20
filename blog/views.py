from django.shortcuts import render, reverse
from django.views.generic import ListView,DetailView
from .models import *
from taggit.models import Tag
from django.http import HttpResponseRedirect
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

        # adding like count
        like_status = False
        ip = get_client_ip(request)
        if self.object.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
            like_status = True
        else:
            like_status=False
        context['like_status'] = like_status


        return self.render_to_response(context)


def postLike(request, pk):
    post_id = request.POST.get('blog-id')
    post = Blog.objects.get(pk=post_id)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))
