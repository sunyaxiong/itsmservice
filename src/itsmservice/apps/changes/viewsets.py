from rest_framework import viewsets

from .models import Change
from .models import ChangeProcessLog
from .serializers import ChangeSerializers
from .serializers import ChangeLogSerializers


class ChangeViewSet(viewsets.ModelViewSet):

    model = Change
    serializer_class = ChangeSerializers
    # ordering = ('-sort',)

    def get_queryset(self):
        queryset = Change.objects.filter()
        # if self.kwargs.get('city'):
        #     queryset = queryset.filter(city=self.kwargs['city'])
        return queryset


class ChangLogViewSet(viewsets.ModelViewSet):

    model = ChangeProcessLog
    serializer_class = ChangeLogSerializers

    def get_queryset(self):
        queryset = ChangeProcessLog.objects.filter()

        return queryset