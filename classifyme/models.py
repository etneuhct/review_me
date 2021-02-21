from django.conf import settings
from django.db import models


user_model = settings.AUTH_USER_MODEL


class WordCategory:
    na, not_inclusive, inclusive = [str(i) for i in range(3)]


class Text(models.Model):
    text_file = models.FileField(null=True, blank=True)
    file_name = models.CharField(max_length=200, unique=True)


class Sentence(models.Model):
    sentence = models.TextField()
    text = models.ForeignKey("Text", on_delete=models.CASCADE)
    sentenceId = models.IntegerField(default=0)


class Word(models.Model):
    sentence = models.ForeignKey("Sentence", on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    position = models.IntegerField()
    verdict = models.CharField(max_length=100, null=True, blank=True, choices=(
        ('conflict', 'conflict'),
        (WordCategory.not_inclusive, "Non Inclusif"),
        (WordCategory.inclusive, "Inclusif"),
        (WordCategory.na, 'Non Applicable'))
    )

    def __str__(self):
        return f"{self.pk} {self.word}"

    class Meta:
        unique_together = (('word', 'position', 'sentence'), )

    @property
    def review_count(self):
        return len(self.review_set.all())

    def set_verdict(self):
        reviews = self.review_set.all()
        reviews_len = len(reviews)
        if reviews_len > 1:
            categories = reviews.values_list('category').distinct()
            if len(categories) > 1:
                self.verdict = "conflict"
            else:
                self.verdict = categories[0][0]
                if self.verdict == WordCategory.na:
                    self.set_na()
            self.save()

    def set_na(self):
        Word.objects.filter(word__iexact=self.word).update(verdict=WordCategory.na)


class Review(models.Model):
    reviewer = models.ForeignKey(user_model, on_delete=models.CASCADE)
    word = models.ForeignKey("Word", on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=(
        (WordCategory.not_inclusive, "Non Inclusif"),
        (WordCategory.inclusive, "Inclusif"),
        (WordCategory.na, 'Non Applicable')))

    class Meta:
        unique_together = (('reviewer', 'word'), )
