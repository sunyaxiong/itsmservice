from rest_framework import viewsets

from .models import Event, EventProcessLog, EventAttachments
from .serializers import EventSerializers, EventLogSerializers
from .serializers import EventAttachmentsSerializers


class EventViewSet(viewsets.ModelViewSet):

    model = Event
    serializer_class = EventSerializers
    filter_fields = ('id', )
    # ordering = ('-sort',)

    def get_queryset(self):
        queryset = Event.objects.filter()
        # if self.kwargs.get('city'):
        #     queryset = queryset.filter(city=self.kwargs['city'])
        return queryset


class EventLogViewSet(viewsets.ModelViewSet):

    model = EventProcessLog
    serializer_class = EventLogSerializers
    filter_fields = ('id', 'event_obj')

    def get_queryset(self):
        queryset = EventProcessLog.objects.filter()
        return queryset


class EventAttachmentsViewSet(viewsets.ModelViewSet):

    model = EventAttachments
    serializer_class = EventAttachmentsSerializers
    filter_fields = ('id', 'event')

    def get_queryset(self):
        queryset = EventAttachments.objects.filter()
        return queryset
