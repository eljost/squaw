import re

from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import (Molecule, Basis, Calculation, Method,
                     Program, Project, Task, Workflow)


class TaskAdmin(DraggableMPTTAdmin):
    list_filter = ["workflow"]


class TaskInline(admin.TabularInline):
    # Modify the queryset to only include Task objects belonging
    # to the current workflow.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if ("object_id" in request.resolver_match.kwargs
            and db_field.name == "parent"):
            obj_id = request.resolver_match.kwargs["object_id"]
            kwargs["queryset"] = Task.objects.filter(workflow_id=obj_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    model = Task
    extra = 1


class WorkflowAdmin(admin.ModelAdmin):
    inlines = [TaskInline]


class CalculationInline(admin.StackedInline):
    model = Calculation
    extra = 1
    # Modify the queryset to only include Task objects belonging
    # to Workflows of the project.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "task":
            obj_id = request.resolver_match.kwargs["object_id"]
            workflow_ids = Molecule.objects.get(pk=obj_id).workflow.values("id")
            kwargs["queryset"] = Task.objects.filter(workflow_id__in=workflow_ids)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MoleculeAdmin(admin.ModelAdmin):
    inlines = [CalculationInline]


admin.site.register(Basis)
admin.site.register(Calculation)
admin.site.register(Method)
admin.site.register(Molecule, MoleculeAdmin)
admin.site.register(Program)
admin.site.register(Project)
admin.site.register(Task, TaskAdmin)
admin.site.register(Workflow, WorkflowAdmin)
