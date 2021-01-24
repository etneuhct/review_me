from django.contrib import admin

# Register your models here.
from classifyme.models import *

admin.site.register(Sentence)
admin.site.register(Text)
admin.site.register(Word)
admin.site.register(Review)
