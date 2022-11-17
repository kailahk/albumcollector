from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Album, List
from .forms import ListenForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def albums_index(request):
    albums = Album.objects.all()
    return render(request, 'albums/index.html', {
        'albums': albums
    })

def albums_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    listen_form = ListenForm()
    return render(request, 'albums/detail.html', {
        'album': album, 'listen_form': listen_form
    })

class CreateAlbum(CreateView):
    model = Album
    fields = ['title', 'artist', 'genres', 'release_year', 'track_list']

class UpdateAlbum(UpdateView):
    model = Album
    fields = ['title', 'artist', 'genres', 'release_year', 'track_list']

class DeleteAlbum(DeleteView):
    model = Album
    success_url = '/albums'

def add_listen(request, album_id):
    form = ListenForm(request.POST)
    if form.is_valid():
        new_listen = form.save(commit=False)
        new_listen.album_id = album_id
        new_listen.save()
    return redirect('detail', album_id=album_id)

class ListList(ListView):
    model = List

class ListDetail(DetailView):
    model = List

class ListCreate(CreateView):
    model = List
    fields = ['name', 'color']

class ListUpdate(UpdateView):
    model = List
    fields = ['name', 'color']

class ListDelete(DeleteView):
    model = List
    success_url = '/lists'