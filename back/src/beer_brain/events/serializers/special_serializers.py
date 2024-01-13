# from rest_framework import serializers
# from rest_framework.request import Request
#
# from .. import models
#
#
# class MembersCountEventSerializer(serializers.ModelSerializer):
#     members_count = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = models.Event
#         fields = "__all__"
#
#     def retrieve(self):
#         request: Request = self.context["request"]
#         members = models.Member.objects.filter(user=request.user)
#         return [member.event for member in members]
#
#     @staticmethod
#     def get_members_count(event: models.Event):
#         return event.users.count()
