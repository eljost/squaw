from django.urls import path

from . import views

app_name = "sqwbase"
urlpatterns = [
    path("", views.index, name="index"),
    path("workflow/<int:workflow_id>/", views.workflow, name="workflow"),
    path("workflow/<int:workflow_id>/molecule/<int:molecule_id>",
         views.mol_workflow, name="mol_workflow"),
    path("calculation/<int:pk>", views.CalculationDetail.as_view(),
         name="calculation"),
]
