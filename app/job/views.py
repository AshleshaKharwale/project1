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

    def perform_create(self, serializer):
        """Create a new job title
        # TODO - refer
        https://www.django-rest-framework.org/api-guide/generic-views/#methods
        Args:
            serializer: validated serializer
        Returns:
        """

        serializer.save(user=self.request.user)


class PortalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PortalDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Portal.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.PortalSerializer
        return self.serializer_class

    def get_queryset(self):
        """
        We want to filter out jobtitles for authenticated users
        """

        return self.queryset.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobDescriptionViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()
    serializer_class = serializers.JobDescriptionDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.JobDescriptionSerializer
        return self.serializer_class

    def get_queryset(self):
        """
        We want to filter out jobtitles for authenticated users
        """

        return self.queryset.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
