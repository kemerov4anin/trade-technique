from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Albums
from .serializers import AlbumsSerializer
from django.views.generic import ListView, DetailView


class ApiAlbumsViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumsSerializer
    queryset = Albums.objects.all()


class AlbumsView(ListView):
    model = Albums
    template_name = "albums.html"
    context_object_name = "albums"
    queryset = Albums.objects.all()


class AlbumDetailView(DetailView):
    model = Albums
    template_name = "albums_detail.html"
    context_object_name = "album"

