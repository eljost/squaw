from django.urls import path

from . import views

app_name = "sqwbase"
urlpatterns = [
    path("", views.index, name="index"),
    path("workflow/<int:workflow_id>/", views.workflow, name="workflow"),
]
