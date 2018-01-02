from django.db.models import prefetch_related_objects
from django.shortcuts import render
from django.views.generic import DetailView

from .models import (Calculation, Molecule, Project,
                     Task, Workflow)


def index(request):
    fields = ("project", "workflow")
    molecules = Molecule.objects.prefetch_related(*fields).all()
    context = {
                "molecules": molecules,
    }
    return render(request, "sqwbase/index.html", context)


def workflow(request, workflow_id):
    workflow = Workflow.objects.get(pk=workflow_id)
    tasks = list()
    for t in Task.objects.filter(workflow__pk=workflow_id):
        t.calculations = Calculation.objects.filter(task=t)
        tasks.append(t)
    context = {
                "workflow": workflow,
                "tasks": tasks,
    }
    return render(request, "sqwbase/workflow.html", context)


def mol_workflow(request, workflow_id, molecule_id):
    # https://stackoverflow.com/questions/31172680
    # prefetch geht nicht weil task kein workflow foreign key hat
    molecule = Molecule.objects.select_related("project").get(pk=molecule_id)
    workflow = Workflow.objects.get(pk=workflow_id)
    tasks = list()
    for t in Task.objects.filter(workflow__pk=workflow_id):
        filters = {
            "task": t,
        }
        t.calculations = Calculation.objects.filter(**filters)
        tasks.append(t)
    context = {
                "molecule": molecule,
                "workflow": workflow,
                "tasks": tasks,
    }
    return render(request, "sqwbase/mol_workflow.html", context)


class CalculationDetail(DetailView):
    model = Calculation
