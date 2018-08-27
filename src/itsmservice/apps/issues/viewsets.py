from rest_framework import viewsets

from .models import Issue
from .serializers import IssueSerializers


class IssueViewSet(viewsets.ModelViewSet):

    model = Issue
    serializer_class = IssueSerializers
    # ordering = ('-sort',)

    def get_queryset(self):
        queryset = Issue.objects.filter()
        # if self.kwargs.get('city'):
        #     queryset = queryset.filter(city=self.kwargs['city'])
        return queryset
