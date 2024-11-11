# portfolio/serializers.py

from rest_framework import serializers
from .models import CollegeItem, ProjectItem, BlogItem, Chip, WorkExperience, WorkExperienceTask, Profile, Technology


class ChipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chip
        fields = ['name', 'order']


class WorkExperienceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceTask
        fields = ['description']


class WorkExperienceSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = WorkExperience
        fields = ['id', 'title', 'company', 'skills', 'start_date', 'end_date', 'tasks', 'order']

    def get_tasks(self, obj):
        return obj.tasks.values_list('description', flat=True)


class CollegeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeItem
        fields = ['id', 'college', 'major', 'year', 'order']


class ProjectItemSerializer(serializers.ModelSerializer):
    chips = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    bannerImage = serializers.ImageField(source='banner_image', use_url=True)

    class Meta:
        model = ProjectItem
        fields = ['id', 'title', 'bannerImage', 'description', 'chips', 'order']


class BlogItemSerializer(serializers.ModelSerializer):
    chips = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    bannerImage = serializers.ImageField(source='banner_image', use_url=True)

    class Meta:
        model = BlogItem
        fields = ['id', 'title', 'bannerImage', 'description', 'chips', 'redirect', 'order']


# portfolio/serializers.py

class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    intro_video = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'name', 'about_me', 'image', 'linkedin_url', 'github_url',
            'facebook_url', 'stackoverflow_url', 'instagram_url',
            'intro_video', 'intro_characteristics'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if obj.image else None

    def get_intro_video(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.intro_video.url) if obj.intro_video else None


class TechnologySerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)  # Ensure full URL for file

    class Meta:
        model = Technology
        fields = ['name', 'file']  # Use 'file' instead of 'image'


class CombinedDataSerializer(serializers.Serializer):
    colleges = CollegeItemSerializer(many=True)
    projects = ProjectItemSerializer(many=True)
    blogs = BlogItemSerializer(many=True)
    work_experiences = WorkExperienceSerializer(many=True)
    profile = ProfileSerializer()
