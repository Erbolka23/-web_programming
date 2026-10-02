from django import forms
from django.utils.text import slugify

from .models import Event


class EventForm(forms.ModelForm):
    summary = forms.CharField(required=False, max_length=240)
    slug = forms.SlugField(required=False)

    class Meta:
        model = Event
        fields = ('title', 'slug', 'summary', 'description', 'location', 'date', 'poster')
        widgets = {
            'date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%dT%H:%M']
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            return slug

        base_slug = slugify(self.cleaned_data['title']) or 'event'
        candidate = base_slug
        suffix = 2
        existing_slugs = Event.objects.all()
        if self.instance.pk:
            existing_slugs = existing_slugs.exclude(pk=self.instance.pk)
        while existing_slugs.filter(slug=candidate).exists():
            candidate = f'{base_slug}-{suffix}'
            suffix += 1
        return candidate