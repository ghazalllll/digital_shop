from django.urls import path
from products.views import (
    ProductListView,ProductDetailView,CategoryListView,
    CategoryDetailView,FileListlView,FileDetailView,

)

urlpatterns = [
    path('categories/', CategoryListView.as_view(),name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(),name='category_detail'),

    path('products/', ProductListView.as_view(),name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(),name='product_detail'),
    
    path('products/<int:product_pk>/files/', FileListlView.as_view(), name='file-list'), 
    path('products/<int:product_pk>/files/<int:pk>/', FileDetailView.as_view(), name='file-detail')
]