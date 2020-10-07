from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):
    """Conversation Model Definition"""

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        return str(
            self.created
        )  # str 해주는 이유(에러가 났었다)-#5.3 ? 내가 conversation을 만들었는데 이게 나를 다시 list로 데려간 것이고 거기서 내 str 을 불렀는데 non-string이란 에러가 낫음.


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    # 이론상으로는 우리가 유저에게 message를 쓸 수 있지만, 그걸 하고 싶지 않은 것이다.
    #  왜냐면 우린 그걸 conversation에서 할 것이기 때문
    # 그럼 누가 message 를 만드느냐? 바로 아래 user 이다.
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE
    )  # 우리가 user 을 없애면 message 도 없어져야 한다.
    conversations = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE
    )  # 우리가 conversation 없애면 message 도 같이 없어져야한다.

    def __str__(self):
        return f"{self.user} says : {self.message}"
