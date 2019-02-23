import django

django.setup()

from main.tasks import single_crawl_without_scheduling

from django.contrib import messages

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


from django.views.generic import TemplateView, ListView, DetailView

from main.models import News, WebsiteInfo


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


class NewsListView(ListView):
    model = News
    template_name = 'main/news_list.html'

    def get_queryset(self, **kwargs):
        try:
            website = WebsiteInfo.objects.get(pk=self.kwargs['pk'])
            return News.objects.filter(news_website__name__contains=website.key)
        except:
            pass


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
                    data_news += News.objects.filter(title__icontains=text, news_website__name__icontains=website)
                if data_news:
                    return render(request, 'main/news_list.html', {'news_list': data_news})
                else:
                    there_have_news = single_crawl_without_scheduling.apply_async(args=[text, websites_list])
                    if there_have_news.get()[0]:
                        for website in websites_list:
                            website_news_name = website + "_" + text.replace(" ", "_")
                            data_news += News.objects.filter(title__icontains=text,
                                                             news_website__name=website_news_name)
                    return render(request, 'main/news_list.html', {'news_list': data_news})
            else:
                data_news = News.objects.filter(title__icontains=text)
                if data_news:
                    return render(request, 'main/news_list.html', {'news_list': data_news})
                else:
                    return render(request, 'main/news_list.html', {})

        else:
            messages.error(request, "Invalid Text, please try again!")
            return redirect(reverse('home'))


def main():
    print("python main function")
    text = "israel"
    website = ["Al-Jazeera English"]
    single_crawl_without_scheduling.apply_async(text, website)


if __name__ == '__main__':
    main()

# def search(request):
#     if request.method == "POST":
#         text = request.POST.get('search_text')
#         website = request.POST.getlist('check')
#         if text:
#             if website:
#                 pass
#             else:
#                 news = News.objects.filter(title__contains=text)
#
#             for data in news:
#                 data.title
#         if news:
#             return render(request, 'main/index.html', {})
#         else:
#             if website:
#                 new_website = NewsWebsite()
#                 new_website.name = text + "search"
#                 new_website.url = "www.www"
#                 new_website.scraper = "sdfs"
#                 new_website.scraper_runtime = "asdasd"
#             return render(request, 'main/index.html', {})
