from django.urls import path
from .import views

urlpatterns = [
    path('',views.logins,name='login'),
    path('home',views.home,name='home'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('admin_page',views.admin1,name='admin'),
    path('logouts',views.logouts,name='logouts'),
    path('add',views.add,name='add'),
    path('edit',views.edit,name='edit'),
    path('update/<str:id>/',views.update,name='update'),
    path('delete/<str:id>/',views.delete1,name='delete'),

]
