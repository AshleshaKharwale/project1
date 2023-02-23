# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from django.urls import reverse
# from core.models import Portal
# from ..serializers import PortalSerializer, PortalDetailSerializer
# from django.contrib.auth import get_user_model
#
#
# PORTAL_URL = reverse("jobtitle:portal-list")
#
#
# class PrivatePortalApiTests(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#
#         self.user = get_user_model().objects.create_user("test@example.com",
#                                                          "password@321")
#
#         self.portal = Portal.objects.create(user=self.user,
#                                             name="test portal",
#                                             description="Testing portal")
#
#         self.client.force_authenticate(self.user)
#
#     def test_portal_list(self):
#         portal = Portal.objects.all().order_by("-id")
#         serializer = PortalSerializer(portal, many=True)
#         res = self.client.get(PORTAL_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
#
#     @staticmethod
#     def portal_detail_url(portal_id):
#         return reverse("jobtitle:portal-detail", args=[portal_id])
#
#     def test_portal_detail(self):
#         portal = Portal.objects.get(name="test portal")
#         serializer = PortalDetailSerializer(portal)
#         url = self.portal_detail_url(portal.id)
#         res = self.client.get(url)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
#
#
# class PublicPortalApiTest(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#
#     def test_unauthorized(self):
#         res = self.client.get(PORTAL_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
