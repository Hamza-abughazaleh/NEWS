from main.tasks import single_crawl_without_scheduling
from django.http import Http404

from django.contrib import messages

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.views.generic import TemplateView, ListView, DetailView

from main.models import News, WebsiteInfo
from random import sample

# Create your views here.
from main.utils import get_news_distinct


class Home(TemplateView):
    home = True
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['home'] = self.home
        # count = News.objects.all().count()
        # rand_ids = sample(range(1, count), 10)
        # context['news_list'] = News.objects.filter(id__in=rand_ids).distinct()
        context['news_list'] = get_news_distinct()
        return context


class NewsListView(ListView):
    model = News
    template_name = 'main/news_list.html'
    news_list = True

    def get_queryset(self, **kwargs):
        try:
            website = WebsiteInfo.objects.get(pk=self.kwargs['pk'])
            return News.objects.filter(news_website__name__contains=website.key).order_by('-created_date')
        except:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['news_list_view'] = self.news_list
        return context


class NewsDetailView(DetailView):
    template_name = 'main/news_detail.html'
    model = News
    context_object_name = 'news_detail'


class SerchForm(TemplateView):

    def get(self, request, *args, **kwargs):
        text = request.GET['search_text']
        websites_list = request.GET.getlist('check')
        if text:
            if websites_list:
                data_news = []
                for website in websites_list:
                    data_news += News.objects.filter(title__icontains=text, description__icontains=text,
                                                     news_website__name__icontains=website)
                if data_news:
                    return render(request, 'main/news_list.html', {'news_list': data_news})
                else:
                    there_have_news = single_crawl_without_scheduling.apply_async(args=[text, websites_list])
                    if there_have_news.get()[0]:
                        for website in websites_list:
                            website_news_name = website + "_" + text.replace(" ", "_")
                            data_news += News.objects.filter(title__icontains=text, description__icontains=text,
                                                             news_website__name=website_news_name)
                    return render(request, 'main/news_list.html', {'news_list': data_news})
            else:
                data_news = News.objects.filter(title__icontains=text, description__icontains=text, )
                if data_news:
                    return render(request, 'main/news_list.html', {'news_list': data_news})
                else:
                    return render(request, 'main/news_list.html', {})

        else:
            messages.error(request, "Invalid Text, please try again!")
            return redirect(reverse('home'))


class PermissionDenied(TemplateView):
    template_name = 'main/403.html'


def single_crawl_without_scheduling_celery(search_term, websites_keys, scheduled=True):
    result = single_crawl_without_scheduling.apply_async(args=[search_term, websites_keys, scheduled])
    return result.get()[0]
