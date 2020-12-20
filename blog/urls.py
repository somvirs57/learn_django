from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostIndexView.as_view(), name='post-list'),
    path('tags/<slug:tag_slug>/', views.TagIndexView.as_view(), name='posts_by_tag'),
    path('detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('like/<int:pk>', views.postLike, name='blog_like'),
]
