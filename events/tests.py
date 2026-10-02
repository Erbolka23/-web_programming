from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .models import Event


class EventWorkflowTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username='event-owner',
            password='Owner-password-2026!',
        )
        self.other_user = user_model.objects.create_user(
            username='other-user',
            password='Other-password-2026!',
        )
        self.event = Event.objects.create(
            title='Community meetup',
            slug='community-meetup',
            summary='Meet your neighbors',
            description='An evening for the community.',
            location='Garden Hall',
            date=timezone.now(),
            organizer=self.owner,
        )

    def test_list_searches_title_and_location_and_paginates(self):
        for index in range(6):
            Event.objects.create(
                title=f'Other meetup {index}',
                slug=f'other-meetup-{index}',
                description='Another event.',
                location='Other Hall',
                date=timezone.now(),
                organizer=self.owner,
            )

        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)

        response = self.client.get(reverse('event_list'), {'q': 'Garden'})
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        self.assertContains(response, 'Community meetup')

    def test_detail_resolves_event_by_slug(self):
        response = self.client.get(self.event.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Community meetup')

    def test_create_requires_login_and_assigns_current_user(self):
        create_url = reverse('event_create')
        response = self.client.post(create_url, {})
        self.assertRedirects(response, f'{reverse("login")}?next={create_url}')

        self.client.force_login(self.owner)
        response = self.client.post(create_url, {
            'title': 'First event',
            'summary': '',
            'description': 'A new event.',
            'location': 'Library room',
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        })

        created_event = Event.objects.get(slug='first-event')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(created_event.organizer, self.owner)

    def test_only_event_owner_can_update_or_delete(self):
        update_url = reverse('event_update', kwargs={'slug': self.event.slug})
        delete_url = reverse('event_delete', kwargs={'slug': self.event.slug})

        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(update_url).status_code, 403)
        self.assertEqual(self.client.get(delete_url).status_code, 403)

        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(update_url).status_code, 200)
        self.assertEqual(self.client.post(delete_url).status_code, 302)
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())

    def test_registration_logs_user_in_and_logout_clears_session(self):
        response = self.client.post(reverse('register'), {
            'username': 'new-member',
            'password1': 'Bright-forest-2026!',
            'password2': 'Bright-forest-2026!',
        })

        self.assertRedirects(response, reverse('event_list'))
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('event_list'))
        self.assertNotIn('_auth_user_id', self.client.session)


class EventModelTests(TestCase):
    def test_event_metadata_and_absolute_url(self):
        organizer = get_user_model().objects.create_user(
            username='organizer',
            password='test-password',
        )
        event = Event.objects.create(
            title='Community meetup',
            slug='community-meetup',
            summary='A local meetup',
            description='Meet and share ideas.',
            location='Community hall',
            date=timezone.now(),
            organizer=organizer,
        )

        self.assertEqual(str(event), 'Community meetup')
        self.assertEqual(event.organizer, organizer)
        self.assertEqual(event.get_absolute_url(), '/event/community-meetup/')
