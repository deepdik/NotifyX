# portfolio/admin.py

from django.contrib import admin
from .models import CollegeItem, ProjectItem, BlogItem, Chip, WorkExperience, WorkExperienceTask, Profile, Technology


@admin.register(CollegeItem)
class CollegeItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'college', 'major', 'year', 'order')
    list_display_links = ('id', 'college')
    list_editable = ('order',)
    search_fields = ('college', 'major', 'year')
    ordering = ['order']

@admin.register(Chip)
class ChipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order')
    list_display_links = ('id', 'name')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ['order']

@admin.register(ProjectItem)
class ProjectItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_chips', 'order')
    list_display_links = ('id', 'title')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    filter_horizontal = ('chips',)
    ordering = ['order']

    def get_chips(self, obj):
        return ", ".join([chip.name for chip in obj.chips.all()])
    get_chips.short_description = 'Chips'

@admin.register(BlogItem)
class BlogItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'redirect', 'get_chips', 'order')
    list_display_links = ('id', 'title')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    filter_horizontal = ('chips',)
    ordering = ['order']

    def get_chips(self, obj):
        return ", ".join([chip.name for chip in obj.chips.all()])
    get_chips.short_description = 'Chips'


class WorkExperienceTaskInline(admin.TabularInline):
    model = WorkExperienceTask
    extra = 1

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'start_date', 'end_date', 'order')
    list_display_links = ('id', 'title')
    list_editable = ('order',)
    search_fields = ('title', 'company')
    filter_horizontal = ('skills',)
    ordering = ['order']
    inlines = [WorkExperienceTaskInline]

admin.site.register(Profile)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')