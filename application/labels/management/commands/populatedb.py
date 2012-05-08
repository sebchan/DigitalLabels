from django.core.management.base import BaseCommand
from labels.models import DigitalLabel, Group

RECORDS = "O77488 O9253 O79056 O52823 O79053 O73631 O78977 O34066 O11451"


class Command(BaseCommand):

    args = "<object_number object_number>"
    help = "Preloads the database with the specified objects"

    def handle(self, *args, **options):

        if not args:
            chip_grp, cr = Group.objects.get_or_create(name="Chippendale")
            recs = RECORDS.split(' ')
            for object_number in recs:
                dl, cr = DigitalLabel.objects.get_or_create(
                                            object_number=object_number)
                dl.group = chip_grp
                dl.save()

        else:
            for object_number in args:
                dl, cr = DigitalLabel.objects.get_or_create(
                                            object_number=object_number)
                dl.save()
