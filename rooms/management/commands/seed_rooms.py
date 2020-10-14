import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
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
        # Field rooms.Room.host cannot be null 에러 때문에 추가함
        all_users = user_models.User.objects.all()

        # django_seed.exceptions.SeederException: Field rooms.Room.room_type cannot be null 에러때문에 추가함
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),  # name 이 너무 길게 생성되지 않기 위해(#9.3)
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 20),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(
            list(created_photos.values())
        )  # created_photos의 이상한 모양?([[14]]<약간 이런식?) 을 정리해준다

        # 나에게 하나의 querySet 을 주는 장고 모듈들 생성!
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        for pk in created_clean:  # 생성된 모든 room들에 대해
            # 데이터 가져와! 사진 찾기. 사진 얻기 (primary_key 로 그 room 을 찾고)
            room_potato = room_models.Room.objects.get(pk=pk)
            # 첫번째 pk?장고는 기본적으로 pk를 생성해주는데, id 값이라고 생각하면 됨! 데이터 추가 시 자동으로 증가하는 숫자 (ex.1,2,3 ... )

            # 3이 최저, 최대는 10-17사이의 랜덤 숫자가 되게끔, photos의 랜덤 번호를 뽑기 위함
            for i in range(3, random.randint(10, 17)):
                room_models.Photo.objects.create(  # 사진 생성. 사진 만들기
                    caption=seeder.faker.sentence(),
                    room=room_potato,
                    file=f"room_photos/{random.randint(1,31)}.webp",  # 그리고, file 주기
                )

            # amenities 안의 amenity를 가져와서 room안의 amenities에 추가할 것임
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room_potato.amenities.add(a)  # add ? >> 다대다 필드에서 무언가 추가하는 방법 !!

            # facilities안의 facility를 가져와서 rooms안의 facilities 에 추가할 것 임
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room_potato.facilities.add(f)

            # houserule 가져와서 room 에 추가할 것 임
            for hr in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room_potato.house_rule.add(hr)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!!"))
