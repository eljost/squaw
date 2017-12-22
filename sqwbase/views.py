from django.shortcuts import render

from .models import Project, Task, Workflow


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
    tasks = Task.objects.filter(workflow__pk=workflow_id)
    context = {
                "tasks": tasks,
    }
    return render(request, "sqwbase/workflow.html", context)
