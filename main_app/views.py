import uuid
import os
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Album, List, Photo
from .forms import ListenForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def albums_index(request):
    albums = Album.objects.filter(user=request.user)
    return render(request, 'albums/index.html', {
        'albums': albums
    })

@login_required
def albums_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    id_list = album.lists.all().values_list('id')
    lists_album_doesnt_have = List.objects.exclude(id__in=id_list)
    listen_form = ListenForm()
    return render(request, 'albums/detail.html', {
        'album': album, 'listen_form': listen_form, 'lists': lists_album_doesnt_have
    })

class CreateAlbum(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'artist', 'genres', 'release_year', 'track_list']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateAlbum(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['title', 'artist', 'genres', 'release_year', 'track_list']

class DeleteAlbum(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = '/albums'

@login_required
def add_listen(request, album_id):
    form = ListenForm(request.POST)
    if form.is_valid():
        new_listen = form.save(commit=False)
        new_listen.album_id = album_id
        new_listen.save()
    return redirect('detail', album_id=album_id)

class ListList(LoginRequiredMixin, ListView):
    model = List

class ListDetail(LoginRequiredMixin, DetailView):
    model = List

class ListCreate(LoginRequiredMixin, CreateView):
    model = List
    fields = ['name', 'color']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListUpdate(LoginRequiredMixin, UpdateView):
    model = List
    fields = ['name', 'color']

class ListDelete(LoginRequiredMixin, DeleteView):
    model = List
    success_url = '/lists'

@login_required
def assoc_list(request, album_id, list_id):
    Album.objects.get(id=album_id).lists.add(list_id)
    return redirect('detail', album_id=album_id)

@login_required
def remove_list(request, album_id, list_id):
    Album.objects.get(id=album_id).lists.remove(list_id)
    return redirect('detail', album_id=album_id)

@login_required
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)