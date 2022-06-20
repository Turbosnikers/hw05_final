from django.core.paginator import Paginator

from yatube.settings import PAGINATOR_LIST


def paginator_func(request, post_list):
    paginator = Paginator(post_list, PAGINATOR_LIST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
