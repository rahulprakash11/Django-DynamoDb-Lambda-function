from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductsView.as_view(), name='products'),
    path('<str:id>/', views.ProductDetailView.as_view(), name='products-item'),

]
