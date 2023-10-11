from django.urls import path
from .views import PostCategoryView, PostsList, PostDetail, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearch, subscribe_category, unsubscribe_category

app_name = 'news'
urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='products'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),    
    path('subscribe_category/<int:pk>/', subscribe_category, name='subscribe_category'),
    path('unsubscribe_category/<int:pk>/', unsubscribe_category, name='unsubscribe_category'),
    path('', PostsList.as_view(), name='posts'),
    path('search/', PostSearch.as_view(), name='post_search'),
]