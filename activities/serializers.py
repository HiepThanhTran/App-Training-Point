from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from interacts.models import Like
from activities.models import Activity, Participation, DeficiencyReport
from tpm.serializers import BaseSerializer
from tpm.utils import factory


class ActivitySerializer(BaseSerializer):
    class Meta:
        model = Activity
        exclude = [
            "created_by_type", "created_by_id", "list_of_participants", "is_active", "created_date", "updated_date"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["criterion"] = instance.criterion.name
        data["semester"] = instance.semester.name
        data["faculty"] = instance.faculty.name

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        request = self.context.get("request")

        instance, serializer_class = factory.get_instance_by_role(request.user)
        user_instance = getattr(request.user, instance, None)

        if user_instance:
            content_type = ContentType.objects.get_for_model(user_instance)
            data["created_by_type"] = content_type
            data["created_by_id"] = user_instance.id

        activity = Activity.objects.create(**data)

        return activity


class AuthenticatedActivitySerializer(ActivitySerializer):
    liked = serializers.SerializerMethodField()

    class Meta:
        model = ActivitySerializer.Meta.model
        exclude = ActivitySerializer.Meta.exclude

    def get_liked(self, instance):
        request = self.context.get("request")

        try:
            like = Like.objects.get(account=request.user, activity=instance)
        except ObjectDoesNotExist:
            return False

        return like.is_active


class AuthenticatedActivityDetailsSerializer(AuthenticatedActivitySerializer):
    from users import serializers as user_serializers
    list_of_participants = user_serializers.StudentSerializer(many=True, required=False)

    created_by = serializers.SerializerMethodField()

    class Meta:
        model = ActivitySerializer.Meta.model
        exclude = ["created_by_type", "created_by_id"]

    def get_created_by(self, instance):
        user = factory.find_user(instance.created_by_id)

        instance, serializer_class, _ = factory.get_instance(user)

        if serializer_class:
            return serializer_class(instance.created_by).data


class ParticipationSerializer(BaseSerializer):
    from users import serializers as user_serializers
    student = user_serializers.StudentSerializer()
    activity = ActivitySerializer()

    class Meta:
        model = Participation
        fields = "__all__"


class DeficiencyReportSerializer(BaseSerializer):
    image = serializers.ImageField(required=False)
    content = serializers.CharField(required=False)

    from users import serializers as user_serializers
    student = user_serializers.StudentSerializer()
    activity = ActivitySerializer()

    class Meta:
        model = DeficiencyReport
        fields = ["id", "is_resolved", "image", "content", "student", "activity", "created_date", "updated_date"]
        extra_kwargs = {
            "is_resolved": {
                "read_only": "true",
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        image = data.get("image", None)
        if image:
            data["image"] = instance.image.url

        return data

    def validate(self, data):
        image = data.get("image")
        content = data.get("content")

        if not image and not content:
            data["image"] = None
            data["content"] = None

        return data
