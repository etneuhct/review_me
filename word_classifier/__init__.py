import os

import gspread
from django.conf import settings

gsheet_client = gspread.service_account(os.environ.get('REVIEWME_GOOGLE_KEYFILE', os.path.join(settings.BASE_DIR, 'googlesheets_key.json')))