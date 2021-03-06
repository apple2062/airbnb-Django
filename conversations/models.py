from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):
    """Conversation Model Definition"""

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            # 이게 모든 participants, 모든 users의 querySet을 줄 것임(쿼리셋이 모든 유저를 준다는 점이 핵심!)
            usernames.append(user.username)
        return " , ".join(usernames)

    def count_messages(self):
        return (
            self.messages.count()
        )  # message.count가 가능한 이유? >> 보다시피 conversation 내에는 masseage 를 가지고 있지 않음
        # 그러나, message 클라스는 conversation을 FK를 messages 로 가지고있다. 때문에 이렇게 count 가 가능!

    count_messages.short_description = "Number of Conversations"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participantss"


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    # 이론상으로는 우리가 유저에게 message를 쓸 수 있지만, 그걸 하고 싶지 않은 것이다.
    #  왜냐면 우린 그걸 conversation에서 할 것이기 때문
    # 그럼 누가 message 를 만드느냐? 바로 아래 user 이다.
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )  # 우리가 user 을 없애면 message 도 없어져야 한다.
    conversations = models.ForeignKey(  # message 는 conversation에도 보내져야 하므로 연결시켜주었음
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )  # 우리가 conversation 없애면 message 도 같이 없어져야한다.

    def __str__(self):
        return f"{self.user} says : {self.message}"
