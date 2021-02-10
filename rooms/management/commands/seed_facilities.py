from django.core.management.base import BaseCommand
from rooms import models as room_models  # amenity 를 import 하기 위해 선언해준다. (seed 만들라고)


class Command(BaseCommand):

    # Metadata about this command.
    help = "this commands creates facilities"

    """
    # command가 우리가 만든 argument(times) 를 이해하지 못하기 떄문에 parser을 생성해야 한다!
    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that i luv u?"
        )
    """

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Free parking on premises",
            "Paid parking on premises",
            "Parking",
            "Elavator",
            "Gym",
            "Pool",
        ]
        for f in facilities:
            room_models.Facility.objects.create(
                name=f
            )  # facilities는 모듈이고, 모듈은 objects를 가지고, objects는 manager가 있고 manager가 생성하고, 삭제하고, 편집하고,업뎃하고..
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} Facilitied created!"))
