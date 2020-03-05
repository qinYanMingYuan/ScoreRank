from django import template

register = template.Library()


@register.filter
def be_int(value):
    return float(value)


@register.filter
def be_name(value, num):
    num = int(num)
    query_dic = value['all_score'][num]
    return query_dic['name']


@register.filter
def be_score(value, num):
    num = int(num)
    query_dic = value['all_score'][num]
    return query_dic['score']

