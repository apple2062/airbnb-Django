import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

# reservation panel 살펴보니, status 는 랜덤하게 될거고, guest 도 랜덤이야.
# guest 랑 room만 하면 될듯 !
# 유저와 게스트, 그리고 룸이 필요하겠구나
# 쳌킨 첵아웃은 , 반드시 첵아웃이 첵킨보다는 더 뒷시간? 이 되어야하잖아? 그러나 일단 먼저 가짜를 만들고, 그러고 나서 첵킨과 첵아웃을 조정해보도록 하자


class Command(BaseCommand):

    # Metadata about this command.
    help = "this commands creates reservations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many reservations do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms_potato = room_models.Room.objects.all()
        # rooms = room_models.Room.objects.all()[4:10] # 모든 방을 주되 4에서 10 사이의 방만 주라는 뜻

        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms_potato),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),  # 최소 3일에서 최대 25일 머문다는 기준으로 작성
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reservations created!!"))
