from django import forms
from .models import Movie

class EventForm(forms.Form):
    title = forms.CharField(label="Название мероприятия", max_length=200)
    date = forms.DateField(label="Дата проведения", widget=forms.DateInput(attrs={'type': 'date'}))

class ParticipantForm(forms.Form):
    email = forms.EmailField(label="Email участника")

ParticipantFormSet = forms.formset_factory(ParticipantForm, extra=1)

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'country', 'poster', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'validate'}),
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'country': forms.TextInput(attrs={'class': 'validate'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'validate'}),
        }
