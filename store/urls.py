from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.customer_list),
    path('customers/<int:pk>', views.customer_detail),
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
    path('collections/', views.collection_list),
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail')
]
