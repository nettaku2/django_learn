from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='carts')
carts_router = routers.NestedDefaultRouter(
    router, 'carts', lookup='cart')
carts_router.register('cartitems', views.CartItemViewSet,
                      basename='cart-cartitems')
products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls)),
    path('orders/', views.order_list),
    path('orders/<int:pk>/', views.order_detail),
    path('orderitems/', views.orderitem_list),
    path('orderitems/<int:pk>', views.orderitem_detail),
    path('customers/', views.customer_list),
    path('customers/<int:pk>/', views.customer_detail),
]
