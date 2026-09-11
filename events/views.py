from django.shortcuts import render
from .models import Event


def event_list(request):
    events = Event.objects.filter(is_published=True).order_by('-starts_at')
    return render(request, 'events/index.html', {'events': events})
