from django.urls import path

from .views import ProductList, ProductDetail,search,GetProductsByPrice

urlpatterns = [
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('search/', search, name='search'),
    path('products/filter-by-price/', GetProductsByPrice.as_view(), name='get-products-by-price'),
   #path('products/filter/',AdsDataFilter.as_view(), name='product-filter'),
    # path('filter/', ProductListAPIView.as_view(), name='product-list'),
]
