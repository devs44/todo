
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import generics

from dashboard.models import Designation, Todo
from dashboard.mixins import NonDeletedListMixin

from .serializers import DesignationSerializer, TodoSerializer
from .mypaginations import MyCursorPagination

class DesignationListAPIView(NonDeletedListMixin, ListAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class TodoListCreate(NonDeletedListMixin, generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = MyCursorPagination


class TodoUpdateDelete(NonDeletedListMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = MyCursorPagination
