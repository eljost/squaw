from django.core.files import File
from django.forms.models import model_to_dict

import cloudpickle

from calcsyncer.main import sync_calculation

def calculation_callback(sender, **kwargs):
    # Always pickle calculation
    instance = kwargs["instance"]
    as_dict = model_to_dict(instance)
    dump = cloudpickle.dumps(as_dict)
    dump_fn = f"/scratch/programme/squaw/calc_dumps/calc_pk{instance.pk}"
    with open(dump_fn, "wb") as handle:
        handle.write(dump)

    # Only try to sync information at creation
    if not kwargs["created"]:
        return
    local_dir, pp_dict = sync_calculation(instance)
    if (not instance.pdb_file) and ("pdb" in pp_dict):
        pdb_fn = pp_dict["pdb"]
        save_to = str(pdb_fn.name)
        instance.pdb_file.save(save_to, File(open(pdb_fn, "r")))
