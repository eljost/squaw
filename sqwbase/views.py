from django.shortcuts import render

from .models import Calculation, Project, Task, Workflow


def index(request):
    projects = Project.objects.all()
    workflows_per_proj = [Workflow.objects.filter(project__name=p.name)
                          for p in projects]
    zipped = zip(projects, workflows_per_proj)
    context = {
                "zipped": zipped,
    }
    return render(request, "sqwbase/index.html", context)


def workflow(request, workflow_id):
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
