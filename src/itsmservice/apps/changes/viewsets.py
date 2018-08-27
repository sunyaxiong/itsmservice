from rest_framework import viewsets

from .models import Change
from .serializers import ChangeSerializers


class ChangeViewSet(viewsets.ModelViewSet):

    model = Change
    serializer_class = ChangeSerializers
    # ordering = ('-sort',)

    def get_queryset(self):
        queryset = Change.objects.filter()
        # if self.kwargs.get('city'):
        #     queryset = queryset.filter(city=self.kwargs['city'])
        return queryset
