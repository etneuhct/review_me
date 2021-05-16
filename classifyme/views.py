from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.generic import ListView

from classifyme.forms import get_word_reviewer_create_form, WordReviewerCreateFormset, WordFormset
from classifyme.models import Review, Word, WordCategory


class WordReviewerCreateView(LoginRequiredMixin, ListView):

    model = Word
    template_name = "classify/create.html"

    def get_queryset(self):
        user = self.request.user
        query = Word.objects.filter(verdict=None).exclude(review__reviewer=user)
        return query[0:15]

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=None, **kwargs)
        queryset = self.object_list
        initial_formset = []
        for i in queryset:
            initial_formset.append({'word': i.pk})
        formset = get_word_reviewer_create_form(extra=0)(initial=initial_formset)
        context_data['formset'] = formset
        return context_data

    def post(self, request, *args, **kwargs):
        word_reviewer_formset = WordReviewerCreateFormset(request.POST)
        user = request.user
        for form in word_reviewer_formset:
            if form.is_valid():
                word = Word.objects.get(pk=form['word'].value())
                category = form['category'].value()
                try:
                    Review.objects.create(word=word, reviewer=user, category=category)
                except IntegrityError:
                    pass
                word.set_verdict()
        return redirect("review_words_create")


class WordReviewerConflictView(LoginRequiredMixin, ListView):

    model = Word
    template_name = "classify/word.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(WordReviewerConflictView, self).get(request, *args, **kwargs)
        return redirect('login')

    def get_queryset(self):
        query = Word.objects.filter(verdict='conflict')
        return query[0:150]

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=None, **kwargs)
        queryset = self.object_list
        initial_formset = []
        for i in queryset:
            initial_formset.append({'verdict': i.verdict, 'pk': i.pk})
        formset = WordFormset(initial=initial_formset)
        context_data['formset'] = formset
        return context_data

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            word_formset = WordFormset(request.POST)
            for form in word_formset:
                if form.is_valid():
                    word_pk = form['pk'].value()
                    verdict = form['verdict'].value()
                    word = Word.objects.get(pk=word_pk)
                    word.verdict = verdict
                    word.save()
                    if verdict == WordCategory.na:
                        word.set_na()
                    elif verdict == WordCategory.epicene:
                        word.set_epicene()
            return redirect("review_words_conflict")
        return redirect('login')


class WordReviewerListView(LoginRequiredMixin, ListView):

    model = Word
    template_name = "classify/list.html"
    paginate_by = 100
    ordering = 'word'
