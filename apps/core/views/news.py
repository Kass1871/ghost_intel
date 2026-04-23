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
        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'content': request.POST.get('content'),
            'category': request.POST.get('category'),
            'source': request.POST.get('source'),
            'isGameBreaking': request.POST.get('isGameBreaking'),
        }
        try:
            news = News(**data)
            news.author = request.user if request.user.is_authenticated else None

            if not request.user.is_authenticated:
                news.anon_edit_token = uuid.uuid4()
            
            news.full_clean()
            news.save()
            
            if not request.user.is_authenticated and news.anon_edit_token:
                anon_tokens = request.session.get('anon_news_tokens', {})
                anon_tokens[str(news.id)] = str(news.anon_edit_token)
                request.session['anon_news_tokens'] = anon_tokens
            
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
        return render(request,
                      'core/news_details.html',
                      {'news_form': news_form,
                       'news': news}
                    )

    def post(self, request, pk):
        news = get_object_or_404(News, pk=pk)

        is_user_owner = request.user.is_authenticated and news.author_id == request.user.id

        anon_tokens = request.session.get("anon_news_tokens", {})
        session_token = anon_tokens.get(str(news.id))
        is_anon_owner = (
                not request.user.is_authenticated
                and news.anon_edit_token is not None
                and session_token == str(news.anon_edit_token)
        )

        if not (is_user_owner or is_anon_owner):
            return (redirect('news'))

        news_form = NewsForm(request.POST, instance=news)
        if news_form.is_valid():
            news = news_form.save(commit=False)
            news.save()
            news_form.save_m2m()
            return redirect('news_details', pk=news.pk)
        return render(request,
                      'core/news_details.html',
                      {"news_form": news_form,
                       'news': news,
                       'errors': news_form.errors})