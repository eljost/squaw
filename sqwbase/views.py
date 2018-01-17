from django.db.models import prefetch_related_objects
from django.shortcuts import render
from django.views.generic import DetailView, ListView

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
            "molecule": molecule,
        }
        t.calculations = Calculation.objects.filter(**filters)
        tasks.append(t)
    context = {
                "molecule": molecule,
                "workflow": workflow,
                "tasks": tasks,
    }
    return render(request, "sqwbase/mol_workflow.html", context)


def calculation(request, calculation_id):
    calculation = Calculation.objects.get(pk=calculation_id)
    if calculation.pdb_file:
        with open(calculation.pdb_file.path) as handle:
            pdb = handle.read()
    else:
        pdb = False

    context = {
        "calculation": calculation,
        "pdb": pdb,
    }
    return render(request, "sqwbase/calculation_detail.html", context)


#class CalculationDetail(DetailView):
#    model = Calculation


class MoleculeDetail(DetailView):
    model = Molecule


def molecule(request, molecule_id):
    molecule = Molecule.objects.get(pk=molecule_id)
    if molecule.pdb_file:
        with open(molecule.pdb_file.path) as handle:
            pdb = handle.read()
    else:
        pdb = False

    context = {
        "molecule": molecule,
        "pdb": pdb,
    }
    return render(request, "sqwbase/molecule_detail.html", context)

class MoleculeList(ListView):
    model = Molecule


class WorkflowList(ListView):
    model = Workflow
