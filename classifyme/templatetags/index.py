from django import template

from classifyme.models import Word

register = template.Library()

@register.filter
def index(indexable, i):
    try:
        return indexable[i]
    except:
        print(i)


@register.filter
def custom_slice(value: str, word: Word):
    end = word.position + len(word.word)
    return value[0:word.position], value[word.position: end], value[end:]
