import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    # Metadata about this command.
    help = "this commands creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = (
            user_models.User.objects.all()
        )  # Field rooms.Room.host cannot be null 에러 때문에 추가함
        room_types = (
            room_models.RoomType.objects.all()
        )  # django_seed.exceptions.SeederException: Field rooms.Room.room_type cannot be null 에러때문에 추가함

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),  # name 이 너무 길게 생성되지 않기 위해(#9.3)
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": random.randint(1, 300),
                "beds": random.randint(1, 5),
                "bedrooms": random.randint(1, 5),
                "guests": random.randint(1, 20),
                "baths": random.randint(1, 5),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!!"))
