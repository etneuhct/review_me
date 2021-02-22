import csv
import os
import time

import django
import gspread

os.environ['DJANGO_SETTINGS_MODULE'] = 'word_classifier.settings'
django.setup()

from django.conf import settings

from classifyme.models import *


def feed_to_db(element):
    file_name = element[0]
    word = element[1]
    sentence = element[2]
    position = element[4]

    text, _ = Text.objects.get_or_create(file_name=file_name)
    sentence, _ = Sentence.objects.get_or_create(text=text, sentence=sentence, sentenceId=int(element[3]))
    Word.objects.get_or_create(word=word, position=position, sentence=sentence)

def feed_from_csv():
    with open("classifyme/data.csv", "r", encoding="utf-8") as f:
        f = csv.reader(f, delimiter=',')
        line_count = 0
        for element in f:
            if line_count > 0:
                feed_to_db(element)
            line_count += 1

def feed_from_sheets():
    gsheet_client = gspread.service_account(os.environ.get('REVIEWME_GOOGLE_KEYFILE', os.path.join(settings.BASE_DIR, 'googlesheets_key.json')))
    sheet = gsheet_client.open_by_key('1jj2Ha1PliKgJbrjgX65rroVU8118AzZ-DcbJLox-WCI').sheet1
    i = 2
    t0 = time.monotonic()
    n0 = 0
    while True:
        try:
            if not sheet.cell(i, 1).value:
                # arrêter dès qu'une ligne est vide
                break
            values = sheet.row_values(i)
        except gspread.exceptions.APIError as e:
            print(e)
            print('Nombre de requêtes depuis le début: ', n0)
            time.sleep(105 - (time.monotonic() - t0))
            t0 = time.monotonic()
            continue
        else:
            print('COUCOU row_values: ', values[:3])
            feed_to_db(values)
        i = i + 1
        n0 = n0 + 2
