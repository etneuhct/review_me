import csv
import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'word_classifier.settings'
django.setup()

from classifyme.models import *


def feed():
    # [i.delete() for i in Word.objects.all()]

    with open("classifyme/data.csv", "r", encoding="utf-8") as f:

        f = csv.reader(f, delimiter=',')
        line_count = 0
        for element in f:
            if line_count > 0:
                file_name = element[0]
                word = element[1]
                sentence = element[2]
                position = element[4]

                text, _ = Text.objects.get_or_create(file_name=file_name)
                sentence, _ = Sentence.objects.get_or_create(text=text, sentence=sentence)
                word = Word.objects.get_or_create(word=word, position=position, sentence=sentence)
            line_count += 1

for i in Word.objects.filter(word__iexact='institution'):
    i.verdict = 'conflict'
    i.save()
