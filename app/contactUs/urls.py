from django.urls import path

from . import views


urlpatterns = [
    path('', views.ContactsView.as_view(), name = 'contacts'),
    path('<str:id>/', views.ContactDetailView.as_view(), name='contactsList'),
]