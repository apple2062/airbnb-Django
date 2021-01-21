import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    # Metadata about this command.
    help = "this commands creates lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many lists do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms_potato = room_models.Room.objects.all()
        # rooms = room_models.Room.objects.all()[4:10] # 모든 방을 주되 4에서 10 사이의 방만 주라는 뜻

        seeder.add_entity(
            list_models.List,
            number,
            {
                # "rooms": lambda x: random.choice(rooms_potato),
                "user": lambda x: random.choice(users),
            },
        )
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))

        for pk in created_clean:
            list_model = list_models.List.objects.get(pk=pk)
            # 랜덤한 방의 수 얻기
            to_add = rooms_potato[random.randint(0, 5) : random.randint(6, 30)]

            # 왜 to_add 안하고 *to_add? >> 포인터개념으로, 그냥 to_add 하면 쿼리셋,즉 array가 되기 때문에 나는 array 안에 있는 요소 "값" 을 원하므로 *to_add 라고 해주었다.
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} lists created!!"))
