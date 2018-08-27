from rest_framework import viewsets

from .models import Knowledge
from .serializers import KnowledgeSerializers


class KnowledgeViewSet(viewsets.ModelViewSet):

    model = Knowledge
    serializer_class = KnowledgeSerializers
    # ordering = ('-sort',)

    def get_queryset(self):
        queryset = Knowledge.objects.filter()
        # if self.kwargs.get('city'):
        #     queryset = queryset.filter(city=self.kwargs['city'])
        return queryset
