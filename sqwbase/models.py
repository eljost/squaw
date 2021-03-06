from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


def rename_pdb(instance, filename):
    if isinstance(instance, Molecule):
        prefix = "molecule_"
    elif isinstance(instance, Calculation):
        prefix = "calc_"
    else:
        prefix = ""
    save_to = "pdbs/" + f"{prefix}pk{instance.pk}_" + filename
    return save_to


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Workflow(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        #return "{} - {}".format(self.project.name, self.name)
        return self.name


class Task(MPTTModel):
    workflow = models.ForeignKey(Workflow, blank=True, null=True,
                                 on_delete=models.CASCADE)
    parent = TreeForeignKey("self", blank=True, null=True,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    analysis = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Molecule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    workflow = models.ManyToManyField(Workflow)
    description = models.TextField(blank=True)
    pdb_file = models.FileField(blank=True, upload_to=rename_pdb)

    def __str__(self):
        return self.name


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


class SolventModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Calculation(models.Model):
    title = models.CharField(max_length=250)
    task = TreeForeignKey(Task, on_delete=models.CASCADE)
    molecule = models.ForeignKey(Molecule, on_delete=models.CASCADE)
    local_path = models.CharField(max_length=250, blank=True)
    remote_path = models.CharField(max_length=250, blank=True)
    calculation_comment = models.TextField(blank=True)
    solvent = models.ForeignKey(SolventModel, blank=True,
                                on_delete=models.CASCADE)

    method = models.ForeignKey(Method, null=True, blank=True,
                               on_delete=models.CASCADE)
    basis = models.ForeignKey(Basis, null=True, blank=True,
                              on_delete=models.CASCADE)
    program = models.ForeignKey(Program, null=True, blank=True,
                                on_delete=models.CASCADE)
    pdb_file = models.FileField(blank=True, upload_to=rename_pdb)
    result = models.BooleanField()

    def __str__(self):
        return self.title


class MoleculeTaskMatrix(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task)
    molecule = models.ManyToManyField(Molecule)
