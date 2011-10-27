# Create your views here.
from annoying.decorators import render_to

from corecontent.models import ContentItem

@render_to('corecontent/view.item.html')
def viewitem(request, slug):
    item = ContentItem.objects.get(slug=slug)
    item._views_count += 1
    item.save()
    return {'item': item}
    
