from django.urls import path, include

from . import views

#view_name = 'review-action-list'
app_name = 'productionLine'

urlpatterns = [
    path('', views.ProductionLineActionView.as_view(), name='v2-productionline-action'),
]