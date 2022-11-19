import uuid
import os
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Album, List, Photo
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
    id_list = album.lists.all().values_list('id')
    lists_album_doesnt_have = List.objects.exclude(id__in=id_list)
    listen_form = ListenForm()
    return render(request, 'albums/detail.html', {
        'album': album, 'listen_form': listen_form, 'lists': lists_album_doesnt_have
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

def assoc_list(request, album_id, list_id):
    Album.objects.get(id=album_id).lists.add(list_id)
    return redirect('detail', album_id=album_id)

def remove_list(request, album_id, list_id):
    Album.objects.get(id=album_id).lists.remove(list_id)
    return redirect('detail', album_id=album_id)

def add_photo(request, album_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, album_id=album_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', album_id=album_id)