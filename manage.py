#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import dotenv


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # 장고가 main() 함수를 call 하기 전에 아래와 같이 작성해주기만 하면, 코드 상에 적힌 내 개인적 비밀번호, 정보들 .env로 인해 보호 가능
    dotenv.read_dotenv()
    main()
