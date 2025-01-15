from django import template

register = template.Library()

@register.filter
def get_item(notes, id_eleve):
    return notes.filter(eleve_id=id_eleve).first()
