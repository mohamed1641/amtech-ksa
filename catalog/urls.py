from django.urls import path
from . import views


app_name = 'catalog'


urlpatterns = [
    path('', views.product_list, name='product_list'),

    # Product details page by slug.
    # Example: /products/ergozm/
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]