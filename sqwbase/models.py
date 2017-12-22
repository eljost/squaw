from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Workflow(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)

    def __str__(self):
        return "{} - {}".format(self.project.name, self.name)


class Task(MPTTModel):
    workflow = models.ForeignKey(Workflow, blank=True, null=True,
                                 on_delete=models.CASCADE)
    parent = TreeForeignKey("self", blank=True, null=True,
                            on_delete=models.PROTECT)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class BaseMolecule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class WFMolecule(models.Model):
    molecule = models.ForeignKey(BaseMolecule, on_delete=models.PROTECT)
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)


class Method(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Basis(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=20)

    def __str__(self):
        return "{} {}".format(self.name, self.version)


class Calculation(models.Model):
    task = TreeForeignKey(Task, on_delete=models.PROTECT)
    molecule = models.ForeignKey(WFMolecule, on_delete=models.PROTECT)
    local_path = models.CharField(max_length=250, blank=True)
    remote_path = models.CharField(max_length=250, blank=True)
    calculation_comment = models.TextField(blank=True)

    method = models.ForeignKey(Method, null=True, blank=True,
                               on_delete=models.PROTECT)
    basis = models.ForeignKey(Basis, null=True, blank=True,
                              on_delete=models.PROTECT)
    program = models.ForeignKey(Program, null=True, blank=True,
                                on_delete=models.PROTECT)
