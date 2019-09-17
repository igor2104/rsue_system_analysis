from django import template
from ..matrix_name import matrix_name

register = template.Library()

@register.simple_tag
def vardump(var):
    return vars(var)


@register.simple_tag
def dirdump(var):
    return dir(var)


@register.filter
def get_name_matrix(key):
    return matrix_name[key]


@register.filter
def get_indicator(group, key):

    string = '<p style="line-height: 20px;">Пороговое значение <span class="epsil">&epsilon;</span><sub>{0}</sub> = {1}</p>'

    if key == 'P0Matrix':
        return string.format('P', get_indicator_value(group, key))
    elif key == 'S0Matrix':
        return string.format('S', get_indicator_value(group, key))
    elif key == 'H0Matrix':
        return string.format('H', get_indicator_value(group, key))
    elif key == 'G0Matrix':
        return string.format('G', get_indicator_value(group, key))

    return ''


def get_indicator_value(group, key):
    if key == 'P0Matrix':
        return group.e_p
    elif key == 'S0Matrix':
        return group.e_s
    elif key == 'H0Matrix':
        return group.e_h
    elif key == 'G0Matrix':
        return group.e_g
    return None


@register.simple_tag
def get_nodes(group):

    nodes = []

    for i, obj in enumerate(group.objects_list.all(), 1):
        nodes.append({'id': i, 'label': '{1}(Q{0})'.format(obj.pk, i)})

    return nodes

@register.simple_tag
def get_edges(matrix):

    edges = []

    elements = {}

    for i, row in enumerate(matrix, 1):
        for j, col in enumerate(row, 1):
            if col == 1 and i != j:
                if str(j)+ ' to ' + str(i) in elements:
                    elements[str(j)+ ' to ' + str(i)] = {'from': i, 'to': j, 'arrows': 'to, from'}
                else:
                    elements[str(i)+ ' to ' + str(j)] = {'from': i, 'to': j, 'arrows': 'to'}

    for k, v in elements.items():
        edges.append(v)

    return edges