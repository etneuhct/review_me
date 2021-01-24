from django.forms import ModelForm, IntegerField
from django.forms import formset_factory

from classifyme.models import Review, Word


class WordForm(ModelForm):
    pk = IntegerField(
    )

    class Meta:
        model = Word
        fields = ['verdict', 'pk']


class WordReviewerCreateForm(ModelForm):

    class Meta:
        model = Review
        fields = ['word', 'category']


def get_word_reviewer_create_form(extra):
    return formset_factory(WordReviewerCreateForm, extra=extra)


WordReviewerCreateFormset = formset_factory(WordReviewerCreateForm)
WordFormset = formset_factory(WordForm, extra=0)
