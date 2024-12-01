from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management.base import BaseCommand
from .models import BinModel

cmd = BaseCommand()

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == "app_apiwhs":
        cmd.stdout.write(cmd.style.MIGRATE_HEADING("Custom initial data upload:"))
        bins = ["GR-ZONE", "GI-ZONE"]
        for bin in bins:
            if not BinModel.objects.filter(id_bin__iexact=bin).exists():
                instance = BinModel.objects.create(
                                                    id_bin=bin,
                                                    created_by="migration")
                message = f"  Bin {instance.id_bin} was created."
                cmd.stdout.write(cmd.style.MIGRATE_LABEL(message))
        cmd.stdout.write(cmd.style.MIGRATE_LABEL("  Initial data complete."))
