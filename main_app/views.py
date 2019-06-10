from django.shortcuts import render

class Plant:
    def __init__(self, name, type, description, size):
        self.name = name
        self.type = type
        self.description = description
        self.size = size

plants = [
    Plant('Sir Teddington von Planten', 'Fiddle Leaf Fig', 'Loves the sun and weekly waterings', 'Medium'),
    Plant('Mortimer', 'ZZ Plant', 'Likes to chill in the shade, water when dry', 'Medium'),
    Plant('Moira', 'Echeveria', 'ALL the sun, water only when wrinkly', 'Mini'),
]


# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1> Hello Plants </h1')

def about(request):
    return render(request, 'about.html')

def plants_index(request):
    return render(request, 'plants/index.html', { 'plants': plants })