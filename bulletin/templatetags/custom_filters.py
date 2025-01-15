from django import template
register = template.Library()

@register.filter
def get_note_for_student_and_subject(notes, student_id, codemat):
    try:
        return notes.get(ance__id_eleve=student_id, id_matiere=codemat)
    except Note.DoesNotExist:
        return None
@register.filter
def get_matieres_for_classe(idclasse):
    """
    Custom filter to get matieres for a given class ID.
    """
    return Matiere.objects.filter(id_classe_id=idclasse)

register = template.Library()

@register.filter
def get_grade(grades_dict, matiere_id):
    # Retourne la note si elle existe, sinon 'N/A'
    return grades_dict.get(matiere_id, 'N/A')