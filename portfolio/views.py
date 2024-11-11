# portfolio/views.py

from rest_framework import generics
from .models import CollegeItem, ProjectItem, BlogItem, WorkExperience, Profile, Technology
from .serializers import CollegeItemSerializer, ProjectItemSerializer, BlogItemSerializer, WorkExperienceSerializer, \
    ProfileSerializer, TechnologySerializer
from rest_framework.views import APIView
from rest_framework.response import Response



class CollegeItemList(generics.ListAPIView):
    queryset = CollegeItem.objects.all()
    serializer_class = CollegeItemSerializer


class ProjectItemList(generics.ListAPIView):
    queryset = ProjectItem.objects.all()
    serializer_class = ProjectItemSerializer


class BlogItemList(generics.ListAPIView):
    queryset = BlogItem.objects.all()
    serializer_class = BlogItemSerializer


class WorkExperienceList(generics.ListAPIView):
    queryset = WorkExperience.objects.prefetch_related('skills', 'tasks')
    serializer_class = WorkExperienceSerializer


class CombinedDataView(APIView):
    def get(self, request, format=None):
        colleges = CollegeItem.objects.all().order_by('order')
        projects = ProjectItem.objects.all().order_by('order')
        blogs = BlogItem.objects.all().order_by('order')
        work_experiences = WorkExperience.objects.prefetch_related('skills', 'tasks').order_by('order')
        profile = Profile.objects.first()
        technologies = Technology.objects.all()  # Fetch all technologies

        data = {
            'colleges': CollegeItemSerializer(colleges, many=True).data,
            'projects': ProjectItemSerializer(projects, many=True, context={'request': request}).data,
            'blogs': BlogItemSerializer(blogs, many=True, context={'request': request}).data,
            'work_experiences': WorkExperienceSerializer(work_experiences, many=True).data,
            'profile': ProfileSerializer(profile, context={'request': request}).data if profile else None,
            'technologies': TechnologySerializer(technologies, many=True, context={'request': request}).data


        }

        return Response(data)
