from django import template

register = template.Library()

@register.filter(name='as_div')
def as_div(form):
    return form.as_div()

@register.simple_tag
def render_field(field):
    return field.as_widget(attrs={'class': 'form-control'})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)