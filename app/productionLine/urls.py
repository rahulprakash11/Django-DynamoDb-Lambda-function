from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ProductionLinesView.as_view(), name='productionLines'),
    path('<str:id>/', views.ProductionLineDetailView.as_view(), name='productionLine'),
    path('<str:id>/move/', views.ProductionLineMoveView.as_view(), name='productionLine-move'),
    path('<str:pId>/actions/', include('app.productionLine.actions.urls'), name='productionLine-action'),
]

