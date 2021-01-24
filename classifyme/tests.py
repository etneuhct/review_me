from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import Client
from classifyme.models import Word, Text, Sentence, Review, WordCategory
# Create your tests here.
from classifyme.views import WordReviewerCreateView


class ViewTestCase(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        user_model = get_user_model()
        self.user, _ =user_model.objects.get_or_create(username="babar", password="azerty")
        text, _ = Text.objects.get_or_create(file_name="filename")
        sentence, _ = Sentence.objects.get_or_create(sentence="phrase", text=text)
        word, _ = Word.objects.get_or_create(sentence=sentence, word="bonjour", position=0)

    def test_clientGetReviewCreateRefuseAnonymousView(self):
        result = self.client.get(reverse('review_words_create'))
        assert result.status_code == 302

    def test_clientGetReviewCreateAllowConnectedView(self):
        request = self.factory.get(reverse('review_words_create'))
        request.user = self.user
        response = WordReviewerCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_clientGetWordReviewerConflictiew(self):
        result = self.client.get(reverse('review_words_conflict'))
        assert result.status_code == 302

    def test_clientGetWordReviewerConflictView(self):
        request = self.factory.get(reverse('review_words_conflict'))
        request.user = self.user
        response = WordReviewerCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
