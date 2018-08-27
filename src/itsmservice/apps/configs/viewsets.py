from rest_framework import viewsets

from .models import Config
from .serializers import ConfigSerializers


class ConfigViewSet(viewsets.ModelViewSet):

    model = Config
    serializer_class = ConfigSerializers
    # ordering = ('-sort',)

    def get_queryset(self):
        queryset = Config.objects.filter()
        # if self.kwargs.get('city'):
        #     queryset = queryset.filter(city=self.kwargs['city'])
        return queryset
