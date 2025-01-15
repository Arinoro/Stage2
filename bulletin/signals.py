# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Annee, Ance

# @receiver(post_save, sender=Annee)
# def mettre_a_jour_annee_active(sender, instance, **kwargs):
#     # Si l'année est activée (encours = 1), mettre à jour l'année dans la table Ance
#     if instance.encours == 1:
#         Ance.objects.all().update(idannee=instance)
# # 