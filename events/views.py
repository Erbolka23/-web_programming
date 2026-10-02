from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

from .forms import EventForm
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        queryset = Event.objects.select_related('organizer').order_by('date', 'pk')
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(location__icontains=query)
            )
        return queryset


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)


class EventOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().organizer_id == self.request.user.pk


class EventUpdateView(EventOwnerMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class EventDeleteView(EventOwnerMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('event_list')


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
