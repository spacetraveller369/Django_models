import json
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .forms import EventForm, ParticipantFormSet
from django.core.files.storage import FileSystemStorage
from .forms import MovieForm
from .models import Movie

# === ЗАНЯТИЕ 2 (Новостной портал) ===
CATEGORIES = {"tech": "Технологии и IT", "sports": "Спорт", "science": "Наука"}
NEWS = [
    {"id": 1, "category": "tech", "title": "Вышел Python 3.14", "image": "app/news1.jpg", "text": "Полный текст про Python..."},
    {"id": 2, "category": "tech", "title": "Django юбилей", "image": "app/news2.jpg", "text": "Полный текст про Django..."},
]

def categories_list_view(request):
    return render(request, "app/categories.html", {"categories": CATEGORIES})

def category_detail_view(request, category_id):
    if category_id not in CATEGORIES:
        raise Http404()
    filtered = [n for n in NEWS if n["category"] == category_id]
    return render(request, "app/category_detail.html", {"category_name": CATEGORIES[category_id], "news_list": filtered})

def news_detail_view(request, news_id):
    item = next((n for n in NEWS if n["id"] == news_id), None)
    if item is None:
        raise Http404()
    return render(request, "app/news_detail.html", {"news": item})

# === ЗАНЯТИЕ 3 (Форма) ===
def create_event_view(request):
    if request.method == "POST":
        event_form = EventForm(request.POST)
        participant_formset = ParticipantFormSet(request.POST)
        if event_form.is_valid() and participant_formset.is_valid():
            event_data = event_form.cleaned_data
            participants = [f.cleaned_data['email'] for f in participant_formset if f.is_valid() and f.cleaned_data]
            request.session['saved_event'] = {'title': event_data['title'], 'date': str(event_data['date']), 'participants': participants}
            return redirect('event_detail')
    else:
        event_form = EventForm()
        participant_formset = ParticipantFormSet()
    return render(request, 'app/create_event.html', {'event_form': event_form, 'participant_formset': participant_formset})

def event_detail_view(request):
    event_data = request.session.get('saved_event')
    if not event_data:
        return redirect('create_event')
    return render(request, 'app/event_detail.html', {'event': event_data})

# === ЗАНЯТИЕ 5 (Фильмы обновленные) ===

def movies_list_view(request):
    
    sort_by = request.GET.get('sort', 'title')
    
    if sort_by == 'rating':
        
        movies = Movie.objects.all().order_by('-rating')
    elif sort_by == 'release_date':
       
        movies = Movie.objects.all().order_by('-release_date')
    else:
        movies = Movie.objects.all()

    return render(request, 'app/movies_list.html', {'movies': movies, 'current_sort': sort_by})

def add_movie_view(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return redirect('/movies/')
    else:
        form = MovieForm()
    return render(request, 'app/add_movie.html', {'form': form})


def movie_detail_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'app/movie_detail.html', {'movie': movie})


def edit_movie_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect(f'/movies/{movie.id}/')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'app/add_movie.html', {'form': form, 'edit_mode': True})


def delete_movie_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        movie.delete()
        return redirect('/movies/')
    return render(request, 'app/delete_movie_confirm.html', {'movie': movie})