from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Plant, Accessory, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'plantcollectorjkc'

# Create your views here.
from django.http import HttpResponse

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def plants_index(request):
  plants = Plant.objects.filter(user=request.user)
  return render(request, 'plants/index.html', { 'plants': plants })

@login_required
def plants_detail(request, plant_id):
  plant = Plant.objects.get(id=plant_id)
  accessories_plant_doesnt_have = Accessory.objects.exclude(id__in = plant.accessories.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'plants/detail.html', { 
      'plant': plant, 'feeding_form': feeding_form, 
      'accessories' : accessories_plant_doesnt_have 
  })

@login_required
def add_feeding(request, plant_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.plant_id = plant_id
    new_feeding.save()
  return redirect('detail', plant_id=plant_id)

class PlantCreate(LoginRequiredMixin, CreateView):
  model = Plant
  fields = ['name', 'species', 'description', 'light', 'water', 'humidity']
  success_url = '/plants/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PlantUpdate(LoginRequiredMixin, UpdateView):
  model = Plant
  fields = ['species', 'description', 'light', 'water', 'humidity']

class PlantDelete(LoginRequiredMixin, DeleteView):
  model = Plant
  success_url = '/plants/'

class AccessoryList(LoginRequiredMixin, ListView):
  model = Accessory

class AccessoryDetail(LoginRequiredMixin, DetailView):
  model = Accessory

class AccessoryCreate(LoginRequiredMixin, CreateView):
  model = Accessory
  fields = '__all__'

class AccessoryUpdate(LoginRequiredMixin, UpdateView):
  model = Accessory
  fields = ['name', 'color']

class AccessoryDelete(LoginRequiredMixin, DeleteView):
  model = Accessory
  success_url = '/accessories/'

@login_required
def assoc_accessory(request, plant_id, accessory_id):
  Plant.objects.get(id=plant_id).accessories.add(accessory_id)
  return redirect('detail', plant_id=plant_id)

@login_required
def remove_accessory(request, plant_id, accessory_id):
  Plant.objects.get(id=plant_id).accessories.remove(accessory_id)
  return redirect('detail', plant_id=plant_id)

@login_required
def add_photo(request, plant_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        session = boto3.Session(profile_name='project1')
        s3 = session.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, plant_id=plant_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', plant_id=plant_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)