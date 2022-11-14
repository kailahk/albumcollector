from django.shortcuts import render

# baby step - usually a model is used
albums = [
    {'name': 'To Pimp a Butterfly', 'artist': 'Kendrick Lamar', 'list': 'All Time Favorites'},
    {'name': 'The Score', 'artist': 'The Fugees', 'list': 'All Time Favorites'},
    {'name': 'Crash', 'artist': 'Charli XCX', 'list': 'Best of 2022'},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def albums_index(request):
    return render(request, 'albums/index.html', {
        'albums': albums
    })