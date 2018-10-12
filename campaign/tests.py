from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

import unittest

from model_mommy import mommy

from . import forms
from . import models
from characters.models import Player
from posts.models import Post


class CampaignTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=3)

        self.campaign = mommy.make(
            models.Campaign,
            user=self.users[0],
            _fill_optional=True,
        )
        self.chapter = mommy.make(
            models.Chapter,
            user=self.users[0],
            campaign=self.campaign,
            _fill_optional=True,
        )
        self.section = mommy.make(
            models.Section,
            user=self.users[0],
            chapter=self.chapter,
            campaign=self.campaign,
            _fill_optional=True,
        )

        self.campaign2 = mommy.make(
            models.Campaign,
            user=self.users[1],
            _fill_optional=True,
        )
        self.chapter2 = mommy.make(
            models.Chapter,
            user=self.users[1],
            campaign=self.campaign2,
            _fill_optional=True,
        )
        self.section2 = mommy.make(
            models.Section,
            user=self.users[1],
            chapter=self.chapter2,
            campaign=self.campaign2,
            _fill_optional=True,
        )

        self.players = mommy.make(
            Player,
            _quantity=3,
            user=self.users[1],
            _fill_optional=True,
        )
        self.players[1].campaigns.add(self.campaign)
        self.players[2].campaigns.add(self.campaign)

        self.post = mommy.make(
            Post,
            user=self.users[0],
            campaign=self.campaign,
            _fill_optional=True,
        )

    def test_campaign_creation_time(self):
        campaign = models.Campaign.objects.create(
            user=self.users[0],
            title="test campaign time",
        )
        now = timezone.now()
        self.assertLess(campaign.created_at, now)

    def test_unique_public_url(self):
        campaign = models.Campaign.objects.create(
            user=self.users[0],
            title="testing uuid",
        )
        check = models.Campaign.objects.filter(public_url=campaign.public_url)
        self.assertEqual(check.count(), 1)

    def test_campaign_exists(self):
        campaigns = models.Campaign.objects.all()

        self.assertIn(self.campaign, campaigns)
        self.assertIn(self.campaign2, campaigns)

    def test_chapter_exists(self):
        chapters = models.Chapter.objects.all()

        self.assertIn(self.chapter, chapters)
        self.assertIn(self.chapter2, chapters)

    def test_section_exists(self):
        sections = models.Section.objects.all()

        self.assertIn(self.section, sections)
        self.assertIn(self.section2, sections)

    def test_campaign_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.chapter.content)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)

    def test_campaign_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/'.format(self.campaign2.pk))

        self.assertEqual(response.status_code, 404)

    def test_campaign_create(self):
        self.client.force_login(self.users[0])

        data = {
            'title': 'test campaign title'
        }
        response = self.client.post('/campaign/create/', data)

        campaign = models.Campaign.objects.get(title='test campaign title')
        self.assertRedirects(response, '/campaign/{}/'.format(campaign.pk), 302, 200)

        response = self.client.get('/campaign/{}/'.format(campaign.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test campaign title')

    def test_campaign_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/edit/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)

    def test_campaign_edit(self):
        self.client.force_login(self.users[0])
        data = {
            'title': 'test campaign title EDIT',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.chapter.pk,
            'form-0-order': 1,
            'form-0-title': self.chapter.title,
        }
        response = self.client.post('/campaign/{}/edit/'.format(self.campaign.pk), data)
        self.assertRedirects(response, '/campaign/{}/'.format(self.campaign.pk), 302, 200)

        response = self.client.get('/campaign/{}/'.format(self.campaign.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test campaign title EDIT')

    def test_campaign_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/delete/'.format(self.campaign.pk), {})
        self.assertRedirects(response, '/', 302, 200)

        campaigns = models.Campaign.objects.all()
        self.assertNotIn(self.campaign, campaigns)
        self.assertEqual(campaigns.count(), 1)

    def test_campaign_print_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/print/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.chapter.content)

    def test_campaign_export_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/print/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.chapter.content)

    def test_chapter_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaign.pk, self.chapter.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.chapter.content)

    def test_chapter_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaign2.pk, self.chapter2.pk))

        self.assertEqual(response.status_code, 404)

    def test_chapter_create(self):
        self.client.force_login(self.users[0])

        data = {
            'title': 'test chapter title',
            'content': 'zzzzzzzzzz',
            'order': '1',
        }
        response = self.client.post('/campaign/{}/chapter/create/'.format(self.campaign.pk), data)

        chapter = models.Chapter.objects.get(title='test chapter title')
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaign.pk, chapter.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaign.pk, chapter.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test chapter title')

    def test_chapter_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/edit/'.format(self.campaign.pk, self.chapter.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.chapter.content)
        self.assertContains(response, self.chapter.order)
        sections = models.Section.objects.filter(chapter=self.chapter)
        for section in sections:
            self.assertContains(response, section.title)

    def test_chapter_edit(self):
        self.client.force_login(self.users[0])
        data = {
            'title': 'test chapter title EDIT',
            'content': 'zzzzzzzzzz EDIT',
            'order': '2',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.section.pk,
            'form-0-order': 1,
            'form-0-title': self.section.title,
        }
        response = self.client.post('/campaign/{}/chapter/{}/edit/'.format(self.campaign.pk, self.chapter.pk), data)
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaign.pk, self.chapter.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaign.pk, self.chapter.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test chapter title EDIT')

    def test_chapter_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/chapter/{}/delete/'.format(self.campaign.pk, self.chapter.pk), {})
        self.assertRedirects(response, '/campaign/{}/'.format(self.campaign.pk), 302, 200)

        chapters = models.Chapter.objects.all()
        self.assertNotIn(self.chapter, chapters)
        self.assertEqual(chapters.count(), 1)

    def test_section_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, self.section.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.section.content)

    def test_section_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaign2.pk, self.chapter2.pk, self.section2.pk))

        self.assertEqual(response.status_code, 404)

    def test_section_create(self):
        self.client.force_login(self.users[0])

        data = {
            'title': 'test section title',
            'content': 'yyyyyyyyyyyyy',
            'order': '1',
        }
        response = self.client.post('/campaign/{}/chapter/{}/section/create/'.format(self.campaign.pk, self.chapter.pk), data)

        section = models.Section.objects.get(title='test section title')
        self.assertRedirects(response, '/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, section.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, section.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test section title')

    def test_section_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/edit/'.format(self.campaign.pk, self.chapter.pk, self.section.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.section.content)
        self.assertContains(response, self.section.order)

    def test_section_edit(self):
        self.client.force_login(self.users[0])
        data = {
            'title': 'test section title EDIT',
            'content': 'xxxxxxxxxxxxx EDIT',
            'order': '2',
        }
        response = self.client.post('/campaign/{}/chapter/{}/section/{}/edit/'.format(self.campaign.pk, self.chapter.pk, self.section.pk), data)
        self.assertRedirects(response, '/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, self.section.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, self.section.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test section title EDIT')

    def test_section_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/chapter/{}/section/{}/delete/'.format(self.campaign.pk, self.chapter.pk, self.section.pk), {})
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaign.pk, self.chapter.pk), 302, 200)

        sections = models.Section.objects.all()
        self.assertNotIn(self.section, sections)
        self.assertEqual(sections.count(), 1)

    def test_campaign_party_page(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/party/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[1].player_name)
        self.assertContains(response, self.players[1].character_name)
        self.assertContains(response, self.players[2].player_name)
        self.assertContains(response, self.players[2].character_name)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)

    def test_campaign_party_invite_page_players(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/party/invite/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.campaign.public_url)

    def test_campaign_party_invite_accept_page_players(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/'.format(self.campaign.public_url))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)

    def test_campaign_party_invite_accept_page_no_players(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/'.format(self.campaign.public_url))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, "You haven't created any Players")

    def test_campaign_party_invite_accept_page_no_auth_no_invite(self):
        response = self.client.get('/campaign/{}/'.format(self.campaign.public_url))
        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/'.format(self.campaign.public_url), 302, 200)

    def test_campaign_party_invite(self):
        self.client.force_login(self.users[1])
        response = self.client.post('/campaign/{}/'.format(self.campaign.public_url), {'player': self.players[0].pk})
        self.assertRedirects(response, '/campaign/{}/party/'.format(self.campaign.pk), 302, 200)

        players = self.campaign.player_set.all()
        self.assertEqual(players.count(), 3)

        response = self.client.get('/campaign/{}/party/'.format(self.campaign.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)

    def test_campaign_party_remove_page_players(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/party/remove/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[1].player_name)
        self.assertContains(response, self.players[1].character_name)
        self.assertContains(response, self.players[2].player_name)
        self.assertContains(response, self.players[2].character_name)

    def test_campaign_party_remove_page_no_players(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/party/remove/'.format(self.campaign2.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Campaign doesn't have any Players")

    def test_campaign_party_remove_page_auth_no_perms(self):
        self.client.force_login(self.users[2])
        response = self.client.get('/campaign/{}/party/remove/'.format(self.campaign2.pk))

        self.assertEqual(response.status_code, 404)

    def test_campaign_party_remove_page_no_auth(self):
        response = self.client.get('/campaign/{}/party/remove/'.format(self.campaign2.pk))
        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/remove/'.format(self.campaign2.pk), 302, 200)

    def test_campaign_party_remove(self):
        players = self.campaign.player_set.all()
        self.assertEqual(players.count(), 2)

        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/party/remove/'.format(self.campaign.pk), {'players': [self.players[1].pk, self.players[2].pk]})
        self.assertRedirects(response, '/campaign/{}/party/'.format(self.campaign.pk), 302, 200)

        players = self.campaign.player_set.all()
        self.assertEqual(players.count(), 0)

        response = self.client.get('/campaign/{}/party/'.format(self.campaign.pk))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)
        self.assertNotContains(response, self.players[2].player_name)
        self.assertNotContains(response, self.players[2].character_name)
        self.assertContains(response, "You haven't invited anyone to your party")

    def test_campaign_party_player_detail_owner(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/party/players/{}/'.format(self.campaign.pk, self.players[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)

    def test_campaign_party_player_detail_player(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/party/players/{}/'.format(self.campaign.pk, self.players[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)

    def test_campaign_party_player_detail_auth_no_perms(self):
        self.client.force_login(self.users[2])
        response = self.client.get('/campaign/{}/party/players/{}/'.format(self.campaign.pk, self.players[0].pk))

        self.assertEqual(response.status_code, 404)

    def test_campaign_party_player_detail_no_auth(self):
        response = self.client.get('/campaign/{}/party/players/{}/'.format(self.campaign.pk, self.players[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/players/{}/'.format(self.campaign.pk, self.players[0].pk), 302, 200)

