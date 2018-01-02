from django.db.models import prefetch_related_objects
from django.shortcuts import render

from .models import (Calculation, BaseMolecule, Project,
                     Task, WFMolecule, Workflow)


def index(request):
    rel_fields = ("molecule", "molecule__project", "workflow")
    wf_molecules = WFMolecule.objects.select_related(*rel_fields).all()
    context = {
                "molecules": wf_molecules,
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


def workflow_molecule(request, workflow_id):
    # https://stackoverflow.com/questions/31172680
    # prefetch geht nicht weil task kein workflow foreign key hat
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
