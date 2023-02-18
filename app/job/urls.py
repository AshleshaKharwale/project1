"""URLs for job API"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job import views

# `DefaultRouter` provided by DRF automatically creates URL routing for us
# TODO - Refer
# https://www.django-rest-framework.org/api-guide/routers/#defaultrouter

router = DefaultRouter()

# this app name will be utilized in reverse function
app_name = "jobtitle"
router.register("jobtitles", views.JobTitleViewSet)  # private api
router.register("portals", views.PortalViewSet)  # private api
router.register("jobdescription", views.JobDescriptionViewSet)  # public api


urlpatterns = [
    path("", include(router.urls))
]

"""
http://127.0.0.1:8000/api/jobtitle/jobtitles/ - jobtitles-list
http://127.0.0.1:8000/api/jobtitle/jobtitles/1/ - jobtitles-detail
http://127.0.0.1:8000/api/jobtitle/portals/ - portals-list
http://127.0.0.1:8000/api/jobtitle/portals/2/ - portals-detail
http://127.0.0.1:8000/api/jobtitle/jobdescription/ - jobdescription-list
http://127.0.0.1:8000/api/jobtitle/jobdescription/2/ - jobdescription-detail
"""