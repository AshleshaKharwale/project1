from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import JobDescription
from job.serializers import (JobDescriptionSerializer,
                             JobDescriptionDetailSerializer)
from django.contrib.auth import get_user_model


JD_URL = reverse("jobtitle:jobdescription-list")


def get_detail_url(jd_id):
    return reverse("jobtitle:jobdescription-detail", args=[jd_id])


class JobDescriptionTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email="test1@gmail.com",
            password="testpassword"
        )

        self.data = {
            "user": self.user,
            "role": "test role",
            "description_text": "Testing job description viewset"
        }

        self.jd = JobDescription.objects.create(**self.data)
        self.client.force_authenticate(self.user)

    def test_post_job_description(self):
        res = self.client.post(JD_URL, self.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get("role"), self.data.get("role"))

    def test_retrieve_job_description_list(self):
        JobDescription.objects.create(
            user=self.user,
            role="test role 1",
            description_text=" 1 Testing job description viewset"
        )

        JobDescription.objects.create(
            user=self.user,
            role="test role 2",
            description_text=" 2 Testing job description viewset"
        )

        jd = JobDescription.objects.all().order_by("-id")
        serializer = JobDescriptionSerializer(jd, many=True)
        res = self.client.get(JD_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_retrieve_job_description_detail(self):

        jd1 = JobDescription.objects.get(id=self.jd.id)
        serializer = JobDescriptionDetailSerializer(jd1)
        url = get_detail_url(jd1.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_job_description(self):
        # while sending post request, no need to provide user.
        # user will be picked up from request.user(authenticated user)
        payload = {
            "role": "python developer",
            "description_text": "skills required - django, rest framework"
        }
        res = self.client.post(JD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload["role"], res.data["role"])

    def test_partial_job_description_update(self):
        payload = {
            "description_text": "patch test"
        }
        url = get_detail_url(self.jd.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["description_text"],
                         res.data["description_text"])

# class PublicAPITest(TestCase):
#
#     def setUp(self) -> None:
#         self.client = APIClient()
#
#     def test_unauthorized_jd_list(self):
#         res = self.client.get(JD_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_unauthorized_jd_detail(self):
#         detail_url = get_detail_url(2)
#         res = self.client.get(detail_url)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
