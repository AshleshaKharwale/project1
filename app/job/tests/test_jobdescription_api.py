from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import JobDescription
from job.serializers import JobDescriptionSerializer, JobDescriptionDetailSerializer


class JobDescriptionTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse("jobtitle:jobdescription-list")
        self.data = {
            "role": "test role",
            "description_text": "Testing job description viewset"
        }

    def test_post_jobdescription(self):
        res = self.client.post(self.url, self.data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get("role"), self.data.get("role"))

    def test_retrieve_jobdescription_list(self):
        JobDescription.objects.create(
            role="test role 1",
            description_text=" 1 Testing job description viewset"
        )

        JobDescription.objects.create(
            role="test role 2",
            description_text=" 2 Testing job description viewset"
        )

        jd = JobDescription.objects.all()
        serializer = JobDescriptionSerializer(jd, many=True)
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    @staticmethod
    def get_detail_url(jd_id):
        return reverse("jobtitle:jobdescription-detail", args=[jd_id])

    def test_retrieve_jobdescription_detail(self):
        JobDescription.objects.create(**self.data)
        jd1 = JobDescription.objects.get(role="test role")
        serializer = JobDescriptionDetailSerializer(jd1)
        url = self.get_detail_url(jd1.id)
        breakpoint()
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

