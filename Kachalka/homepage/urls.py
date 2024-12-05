from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('records_add/', views.RecordsAddView.as_view(), name='radd'),
    path('<int:pk>/records_edit/', views.RecordsEditView.as_view(), name='edit'),
    path('<int:pk>/records_delete/', views.rdelete, name='rdelete'),
    path('statis_add/', views.StatisAdd.as_view(), name='sadd'),
    path('<int:pk>/statis_edit', views.StatisEdit.as_view(), name='sedit'),
    path('<int:pk>/statis_delete/', views.sdelete, name='sdelete'),
    path('<int:pk>/userhref_add/', views.userhref, name='userhref_add')
]
