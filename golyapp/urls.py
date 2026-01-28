from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("player/<int:ide>",views.pdetail,name="detp"),
    path("season",views.archiv,name="archivne"),
    path("nation",views.slovak,name="nation"),
    path("club",views.klub,name="klub"),
    path("slovak",views.cze, name="czech")
]

