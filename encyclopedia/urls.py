from django.urls import path

from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/NewPage", views.newPage, name="NewPage"),
    path("wiki/EditPage/<str:page>", views.editPage, name="EditPage"),
    path("wiki/<str:page>", views.entryPage, name="entryPage")
]
