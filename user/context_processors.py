from category.models import Category,Brand

def menu_links(request):

    links=Category.objects.all()
    brands=Brand.objects.all()
    return {
        'links': links,
        'brands': brands,   
    }



