from rest_framework import viewsets

from .models import Event
from .serializers import EventSerializers


class EventViewSet(viewsets.ModelViewSet):

    model = Event
    serializer_class = EventSerializers
    # ordering = ('-sort',)

    def get_queryset(self):
        queryset = Event.objects.filter()
        # if self.kwargs.get('city'):
        #     queryset = queryset.filter(city=self.kwargs['city'])
        return queryset
