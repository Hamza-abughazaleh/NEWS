from django.conf import settings

from main.models import WebsiteInfo


def get_websites(request):
    if request.LANGUAGE_CODE == 'en':
        websites = WebsiteInfo.objects.filter(website_type=request.LANGUAGE_CODE)
    else:
        websites = WebsiteInfo.objects.filter(website_type=request.LANGUAGE_CODE)
    return {'websites': websites}



def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {'debug': settings.DEBUG,
           }