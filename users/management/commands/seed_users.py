from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models  # amenity 를 import 하기 위해 선언해준다. (seed 만들라고)


class Command(BaseCommand):

    # Metadata about this command.
    help = "this commands creates many users"

    # command가 우리가 만든 argument(times) 를 이해하지 못하기 떄문에 parser을 생성해야 한다!
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many users do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()  # seed 생성
        seeder.add_entity(
            user_models.User,
            number,  # seed 의 개수
            {
                "is_staff": False,
                "is_superuser": False,
            },  # 무작위로 생성된 user 가 superhost 나 staff 이 되면 안되므로 이 조건 필요
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} user created!!"))
