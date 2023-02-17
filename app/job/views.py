"""Views for Job API"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

## import models
from core.models import JobTitle, Portal, JobDescription
from job import serializers


class JobTitleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.JobTitleDetailSerializer

    # represents objects that are available for this viewset.
    # queryset objects that are manageable by this view.
    queryset = JobTitle.objects.all()

    # In order to use endpoint provided by this viewset, we will need ]
    # authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        We want to filter out jobtitles for authenticated users
        """

        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Returns the serializer class to be used for the request"""

        if self.action == "list":
            return serializers.JobTitleSerializer
        return self.serializer_class


class PortalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PortalDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Portal.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.PortalSerializer
        return self.serializer_class

