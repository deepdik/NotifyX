# portfolio/models.py

from django.db import models



class Profile(models.Model):
    name = models.CharField(max_length=255)
    about_me = models.TextField()
    image = models.ImageField(upload_to='profile_images/')
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    github_url = models.URLField(max_length=255, blank=True, null=True)
    facebook_url = models.URLField(max_length=255, blank=True, null=True)
    stackoverflow_url = models.URLField(max_length=255, blank=True, null=True)
    instagram_url = models.URLField(max_length=255, blank=True, null=True)
    intro_video = models.FileField(upload_to='intro_videos/', blank=True, null=True)
    intro_characteristics = models.JSONField(default=list)  # Stores a list of text items for characteristics

    def __str__(self):
        return self.name


class Chip(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class WorkExperience(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    skills = models.ManyToManyField(Chip)
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        ordering = ['order']


class WorkExperienceTask(models.Model):
    work_experience = models.ForeignKey(WorkExperience, related_name='tasks', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Task for {self.work_experience.title}: {self.description[:50]}"

    class Meta:
        ordering = ['id']



class CollegeItem(models.Model):
    college = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    year = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.college} - {self.major}"

    class Meta:
        ordering = ['order']  # Default ordering by 'order' field





class ProjectItem(models.Model):
    title = models.CharField(max_length=255)
    banner_image = models.FileField(upload_to='project_banners/', blank=True, null=True)
    description = models.TextField()
    chips = models.ManyToManyField(Chip)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class BlogItem(models.Model):
    title = models.CharField(max_length=255)
    banner_image = models.FileField(upload_to='project_banners/', blank=True, null=True)
    description = models.TextField()
    chips = models.ManyToManyField(Chip)
    redirect = models.URLField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']



class Technology(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='technology_files/')  # Change ImageField to FileField

    def __str__(self):
        return self.name
