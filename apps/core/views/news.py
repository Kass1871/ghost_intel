from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import uuid

from apps.core.forms.NewsForm import NewsForm
from apps.core.models import News


def news_view(request):
    errors = {}
    data = {}
    if request.method == "POST":
        if not request.user.is_staff:
            return redirect('news')
        data = {
            'title': request.POST.get('title'),
            'slug': request.POST.get('slug'),
            'description': request.POST.get('description'),
            'content': request.POST.get('content'),
            'category': request.POST.get('category'),
            'source': request.POST.get('source'),
            'isGameBreaking': request.POST.get('isGameBreaking') == 'on',
            'status': request.POST.get('status') or 'draft',
        }
        try:
            news = News(**data)
            news.author = request.user
            news.full_clean()
            news.save()
            
            news.tags.set(request.POST.getlist('tags'))
            news.relatedContent.set(request.POST.getlist('relatedContent'))
            
            return redirect('news')
        except ValidationError as e:
            errors = e.message_dict

    news_list = News.objects.all()

    return render(request, 'core/news.html',
                  {"category_choices": News.CATEGORY_CHOICES,
                   "errors": errors,
                   "data": data,
                   'news_list': news_list})

class NewsDetails(View):
    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news_form = NewsForm(instance=news)

        can_edit = request.user.is_staff
        if not can_edit:
            for field in news_form.fields.values():
                field.disabled = True
        return render(request,
                    'core/news_details.html',
                    {'news_form': news_form,
                    'news': news,
                     'can_edit': can_edit}
                )

    def post(self, request, pk):
        news = get_object_or_404(News, pk=pk)

        if not request.user.is_staff:
            return (redirect('news_details', pk=news.pk))

        if request.POST.get('delete'):
            news.delete()
            return redirect('news')

        news_form = NewsForm(request.POST, instance=news)
        if news_form.is_valid():
            news = news_form.save()
            return redirect('news_details', pk=news.pk)

        return render(request,
                      'core/news_details.html',
                      {"news_form": news_form,
                       'news': news,
                       'errors': news_form.errors})