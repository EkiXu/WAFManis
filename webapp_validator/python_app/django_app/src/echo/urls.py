from django.urls import path
from . import views
urlpatterns = {
    path("", views.echo)#第一个参数表示路径
}
