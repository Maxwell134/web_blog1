
from django.urls import path
from .views import HomeView, PostDetailView, UpdatePost, DeletePost, AddBlog, contact_view, contact_details,home_view


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', PostDetailView, name='details'),  # Update this line
    path('add_post/', AddBlog.as_view(), name='add_post'),
    path('article/edit/<int:pk>/', UpdatePost.as_view(), name='update'),
    path('article/<int:pk>/remove/', DeletePost, name='delete'),
    path('article/contact/', contact_view, name='contact'),
    path('article/contact_info/', contact_details, name='contact_info'),
    path('home/', home_view, name='translator'),

]
