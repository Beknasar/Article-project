from django import template


register = template.Library()


@register.filter
def page_query_string(request, page_number):
    query_args = request.GET.copy()
    print(query_args)
    query_args['page'] = page_number
    return query_args.urlencode()
