# portfolio/urls.py

from django.urls import path

from .views import CollegeItemList, ProjectItemList, BlogItemList, WorkExperienceList, CombinedDataView

urlpatterns = [
    path('colleges/', CollegeItemList.as_view(), name='collegeitem-list'),
    path('projects/', ProjectItemList.as_view(), name='projectitem-list'),
    path('blogs/', BlogItemList.as_view(), name='blogitem-list'),
    path('work-experiences/', WorkExperienceList.as_view(), name='workexperience-list'),
    path('all-data/', CombinedDataView.as_view(), name='combined-data'),

]
