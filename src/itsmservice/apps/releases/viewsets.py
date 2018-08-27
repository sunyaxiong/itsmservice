from rest_framework import viewsets

from .models import Release
from .serializers import ReleaseSerializers


class ReleaseViewSet(viewsets.ModelViewSet):

    model = Release
    serializer_class = ReleaseSerializers
    # ordering = ('-sort',)

    def get_queryset(self):
        queryset = Release.objects.filter()
        # if self.kwargs.get('city'):
        #     queryset = queryset.filter(city=self.kwargs['city'])
        return queryset
