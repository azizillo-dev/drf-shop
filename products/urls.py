from django.urls import path
from .views import *


urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:id>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:id>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('categories/', CategoriesView.as_view(), name='categories'),

    path('likes/', UserLikesView.as_view(), name="userslikes"),
    path('comments/', UserCommentsView.as_view(), name="user-comments"),
    
    path('products/<int:id>/like/', LikedView.as_view(), name='product-like'),
    path('products/<int:pk>/comments/', CommentsView.as_view(), name='product-comment'),
]





