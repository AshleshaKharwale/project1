"""Tests for job API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone

from django.urls import reverse, reverse_lazy

# We have registered `core` as an application under `INSTALLED_APPS`
from core.models import JobTitle, Portal, JobDescription
from job.serializers import (
    JobTitleSerializer,
    JobTitleDetailSerializer,
    PortalSerializer,
    PortalDetailSerializer
)


JOB_TITLE_URL = reverse("jobtitle:jobtitle-list")  # /api/jobtitle/jobtitles
PORTAL_URL = reverse("jobtitle:portal-list")  # /api/jobtitle/portal

"""
TODO - refer
https://www.django-rest-framework.org/api-guide/routers/#routers
reverse(<applicationname>:<basename>-list)
reverse(<applicationname>:<basename>-detail)

where, 
'basename'- model name in small case 
'applicationname' - app_name stored in urls.py 
"""


def detail_url(job_title_id):
    """create and return a job title detail URL"""

    return reverse("jobtitle:jobtitle-detail", args=[job_title_id])


def create_job_description(**params):
    """create and return new job description"""

    defaults = {
        "role": "Simple Job Title",
        "description_text": "should know git,CICD, Linux and must know Python",
        "pub_date": timezone.now()
    }
    defaults.update(**params)
    job_description = JobDescription.objects.create(**defaults)
    return job_description


def create_job_title(user, portal, job_description, **params):
    """create and return a sample job title"""

    defaults = {
        "title": "Simple Job Title"
    }
    defaults.update(params)
    job_title = JobTitle.objects.create(
        user=user,
        job_description=job_description,
        portal=portal,
        **params
    )
    return job_title


class PublicJobTitleApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth required API call"""

        res = self.client.get(JOB_TITLE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJobTitleApiTests(TestCase):
    """Test authorized API requests"""

    def setUp(self) -> None:
        """Test fixtures"""

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com",
            "password@321"
        )

        # portal
        self.portal = Portal.objects.create(
            name="naukri.com",
            description="famous job hunting website"
        )

        # job_description
        self.job_description = JobDescription.objects.create(
            role="To build backend microservices",
            description_text="should know git,CICD, Linux and must know Python",
            pub_date=timezone.now()
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_job_titles(self):
        """Test retrieving a list of job titles"""

        create_job_title(
            user=self.user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description()
        )
        create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=create_job_description()
        )

        job_titles = JobTitle.objects.all().order_by("-id")
        serializer = JobTitleSerializer(job_titles, many=True)

        res = self.client.get(JOB_TITLE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_job_title_list_limited_to_user(self):
        """Test list of job titles is limited to authenticated user"""

        other_user = get_user_model().objects.create_user(
            "other@example.com",
            "password@123"
        )
        create_job_title(
            user=other_user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description()
        )
        create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=create_job_description()
        )

        res = self.client.get(JOB_TITLE_URL)

        job_titles = JobTitle.objects.all()
        job_titles = job_titles.filter(user=self.user).order_by("-id")
        serializer = JobTitleSerializer(job_titles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_jobtitle_detail(self):
        """Test get details of particular job title"""

        job_title = create_job_title(
            user=self.user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description()
        )
        url = detail_url(job_title.id)
        res = self.client.get(url)
        serializer = JobTitleDetailSerializer(job_title)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)


class PrivatePortalApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.portal = Portal.objects.create(name="test portal",
                                       description="Testing portal")

        self.user = get_user_model().objects.create_user("test@example.com",
                                                         "password@321")

        self.client.force_authenticate(self.user)

    def test_portal_list(self):
        portal = Portal.objects.all().order_by("-id")
        serializer = PortalSerializer(portal, many=True)
        res = self.client.get(PORTAL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    @staticmethod
    def portal_detail_url(portal_id):
        return reverse("jobtitle:portal-detail", args=[portal_id])

    def test_portal_detail(self):
        portal = Portal.objects.get(name="test portal")
        serializer = PortalDetailSerializer(portal)
        url = self.portal_detail_url(portal.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PublicPortalApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_unauthorized(self):
        res = self.client.get(PORTAL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
