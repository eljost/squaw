from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from . import views

app_name = "sqwbase"
urlpatterns = [
    path("", views.index, name="index"),
    path("workflow/<int:workflow_id>/", views.workflow, name="workflow"),
    path("workflow/<int:workflow_id>/molecule/<int:molecule_id>",
         views.mol_workflow, name="mol_workflow"),
    #path("calculation/<int:pk>", views.CalculationDetail.as_view(),
    #     name="calculation"),
    #path("molecule/<int:pk>", views.MoleculeDetail.as_view(),
    #     name="molecule"),
    path("calculation/<int:calculation_id>/", views.calculation, name="calculation"),
    path("molecule/<int:molecule_id>/", views.molecule, name="molecule"),
    path("molecules/", views.MoleculeList.as_view(), name="molecules"),
    path("workflows/", views.WorkflowList.as_view(), name="workflows"),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {
            "document_root": settings.MEDIA_ROOT,
        }),
    ]
