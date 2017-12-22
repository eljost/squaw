import re

from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import (Basis, Calculation, Method, Molecule,
                     Program, Project, Task, Workflow)


class TaskInline(admin.TabularInline):
    # Modify the queryset to only include Task objects belonging
    # to the current workflow.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
             obj_id = request.resolver_match.kwargs["object_id"]
             kwargs["queryset"] = Task.objects.filter(workflow_id=obj_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    model = Task
    extra = 1


class WorkflowAdmin(admin.ModelAdmin):
    inlines = [TaskInline]


class CalculationInline(admin.TabularInline):
    model = Calculation
    extra = 1
    # This will be filled by a callback function
    #exclude = ["basis", "method", "program"]


class MoleculeAdmin(admin.ModelAdmin):
    inlines = [CalculationInline]


admin.site.register(Basis)
admin.site.register(Calculation)
admin.site.register(Method)
admin.site.register(Molecule, MoleculeAdmin)
admin.site.register(Program)
admin.site.register(Project)
admin.site.register(Task, DraggableMPTTAdmin)
admin.site.register(Workflow, WorkflowAdmin)
