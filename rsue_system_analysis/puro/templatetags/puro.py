from django import template

register = template.Library()

@register.simple_tag
def get_nodes(tour):

    nodes = []

    for i, obj in enumerate(tour.get_experts(), 1):
        nodes.append({'id': i, 'label': '{1}({0})'.format(obj['expert__name'][:2], i)})

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