# bulletin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Annee, Ance, Bulletin
from django.urls import reverse_lazy
from .forms import AnneeForm  # Assurez-vous d'avoir créé ce formulaire dans forms.py
from .forms import AnceForm
from .models import Classe, Matiere
from django.db import transaction
from django.db.models import Prefetch

import logging
from django.shortcuts import render, get_object_or_404, redirect
from .models import Coefficient, Matiere, Note, Ance, Eleve, Classe, MatierePropre
from .models import Numero  # Import the Numero model
from .forms import CoefficientForm, MatiereForm, NoteForm, AnceForm, EleveForm, NoteForm,MatierePropreForm
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Utilisateur  # Assurez-vous que le modèle Utilisateur est bien défini
from django.contrib.auth.decorators import login_required
from .models import RelationGlobale
from .forms import RelationGlobaleForm
from .models import Bulletin
from .forms import BulletinForm  # Assure-toi que le formulaire est bien importé
import json
from django.db.models import Count


# Vue pour la connexion

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('index')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'page-login.html', {'form': form})

@login_required  # Redirige vers la page de connexion si l'utilisateur n'est pas authentifié
def index_view(request):
    """
    Vue pour la page d'accueil.

    """
    annee_active = Annee.objects.filter(encours=True).first()
    context = {
        'user': request.user,  # Informations de l'utilisateur connecté
    }
    return render(request, 'index.html', {
        'annee_active': annee_active,
    })

def logout_view(request):
    """
    Vue pour déconnecter l'utilisateur et le rediriger.
    """
    logout(request)  # Déconnexion de l'utilisateur
    return redirect('login')  # Redirection après déconnexion


@login_required
def profil_utilisateur(request):
    utilisateur = request.user  # Utilisateur actuellement connecté

    # Récupérer l'image de profil
    img_url = utilisateur.imguser.url if utilisateur.imguser else 'img/default-avatar.png'

    # Récupérer l'année scolaire active
    annee_active = Annee.objects.filter(encours=True).first()

    context = {
        'utilisateur': utilisateur,
        'img_url': img_url,
        'annee_active': annee_active  # Ajouter l'année scolaire active au contexte
    }

    return render(request, 'profil_utilisateur.html', context)


# def tableau_de_bord_chart(request):
#     # Récupérer l'année scolaire activée
#     annee_active = Annee.objects.filter(encours=True).first()

#     if not annee_active:
#         # Si aucune année scolaire active n'est trouvée
#         messages.warning(request, "Aucune année scolaire active n'a été trouvée.")
#         matieres = []  # Pas de matières à afficher
#         total_coeff = 0
#         nombre_classes = 0
#         nombre_eleves = 0
#         moyennes_classe = []
#     else:
#         # Filtrer les relations globales liées à l'année active via le modèle Ance
#         ance_relations = Ance.objects.filter(idannee=annee_active)

#         # Récupérer les classes uniques associées à cette année scolaire
#         classes_active = ance_relations.values_list('idclasse', flat=True).distinct()

#         # Filtrer les matières en fonction des classes liées à l'année active
#         matieres = Matiere.objects.filter(idclasse__in=classes_active)

#         total_coeff = sum(matiere.id_coeff for matiere in matieres)

#         # Comptage des classes
#         nombre_classes = Classe.objects.filter(idclasse__in=classes_active).distinct().count()

#         # Comptage des élèves par classe
#         nombre_eleves_par_classe = {}
#         for classe_id in classes_active:
#             # Récupérer le nombre d'élèves pour chaque classe via la relation Ance
#             nombre_eleves_par_classe[classe_id] = ance_relations.filter(idclasse_id=classe_id).count()

#         # Calcul des moyennes des classes
#         moyennes_classe = []
#         for classe_id in classes_active:
#             # Récupérer les élèves de la classe
#             eleves_classe = Eleve.objects.filter(ance__idclasse=classe_id)
#             moyennes_eleves_classe = []

#             for eleve in eleves_classe:
#                 # Récupérer les notes pour l'élève
#                 notes_eleve = Note.objects.filter(ance__eleve=eleve, ance__idannee=annee_active)
#                 total_notes_ponderees_classe = 0
#                 total_coefficients_classe = 0

#                 for matiere in matieres:
#                     note_matiere = notes_eleve.filter(codemat=matiere.codemat).first()
#                     if note_matiere:
#                         coefficient = matiere.id_coeff
#                         note = note_matiere.note
#                         total_notes_ponderees_classe += note * coefficient
#                         total_coefficients_classe += coefficient

#                 if total_coefficients_classe > 0:
#                     moyenne_eleve_classe = total_notes_ponderees_classe / total_coefficients_classe
#                     moyennes_eleves_classe.append(moyenne_eleve_classe)

#             # Calcul de la moyenne de la classe
#             if moyennes_eleves_classe:
#                 moyenne_classe = sum(moyennes_eleves_classe) / len(moyennes_eleves_classe)
#             else:
#                 moyenne_classe = 0

#             # Arrondir la moyenne à 2 décimales
#             moyenne_classe = round(moyenne_classe, 2)

#             moyennes_classe.append({
#                 'classe': Classe.objects.get(idclasse=classe_id).libelleclasse,  # Nom de la classe
#                 'moyenne_classe': moyenne_classe
#             })

#     # Préparer les données pour le graphique
#     chart_data = [
#         {
#             'nom': matiere.id_matiere_propre.nommatiere,
#             'coefficient': matiere.id_coeff,
#             'percentage': (matiere.id_coeff / total_coeff) * 100 if total_coeff > 0 else 0
#         }
#         for matiere in matieres
#     ]

#     # Préparer les données pour le graphique
#     chart_labels = [moyenne['classe'] for moyenne in moyennes_classe]
#     chart_values = [moyenne['moyenne_classe'] for moyenne in moyennes_classe]

#     # Comptage des matières et autres informations
#     nombre_matieres = Matiere.objects.filter(idclasse__in=classes_active).distinct().count()
#     nombre_numero = Numero.objects.count()

#     matiere_propres_count = Ance.objects.filter(matiere_propre__isnull=False, idannee=annee_active).count()

#     # Ajouter les données dans le contexte
#     context = {
#         'classes_active': classes_active,
#         'nombre_classes': nombre_classes,
#         'nombre_eleves': nombre_eleves_par_classe,
#         'nombre_matieres': nombre_matieres,
#         'nombre_numero': nombre_numero,
#         'matiere_propres_count': matiere_propres_count,
#         'chart_data': chart_data,
#         'chart_labels': chart_labels,  # Labels pour le graphique de moyennes
#         'chart_values': chart_values,  # Valeurs pour le graphique de moyennes
#         'annee_active': annee_active,
#         'moyennes_classe': moyennes_classe,  # Moyennes des classes
#     }

#     # Style personnalisé pour l'affichage des moyennes
#     context['style'] = {
#         'moyennes': 'font-weight: bold; color: #4CAF50;',
#         'graph': 'width: 100%; height: 500px; background-color: #f4f4f4; padding: 20px; border-radius: 10px;'
#     }

#     return render(request, 'tableau_de_bord.html', context)

def tableau_de_bord_chart(request):
    # Vérifier si une année scolaire est active
    active_annee = Annee.objects.filter(encours=True).first()

    # Calcul des informations principales (en fonction de l'année active)
    if active_annee:
        nombre_classes = Classe.objects.filter(ance__idannee=active_annee).count()
        nombre_eleves = Eleve.objects.filter(ance__idannee=active_annee).count()
        nombre_matieres = Matiere.objects.count()  # Les matières peuvent ne pas dépendre de l'année
        nombre_numeros = Ance.objects.filter(idannee=active_annee, numero__isnull=False).count()

        # Initialisation des données pour les graphiques
        chart_labels = []  # Noms des classes
        chart_values = []  # Moyennes des classes
        chart_data = []  # Coefficients des matières


        classList = Classe.objects.filter(ance__idannee=active_annee)
        alreadyExistedClass = []

        # Calcul des moyennes des classes
        for classe in classList:
            if classe.idclasse in alreadyExistedClass:
                continue

            alreadyExistedClass.append(classe.idclasse)

            notes_classe = Note.objects.filter(ance__idclasse=classe, ance__idannee=active_annee)
            total_notes_ponderees = 0
            total_coefficients = 0
            for note in notes_classe:
                matiere = note.codemat
                coefficient = matiere.id_coeff
                total_notes_ponderees += note.note * coefficient
                total_coefficients += coefficient

            if total_coefficients > 0:
                moyenne_classe = total_notes_ponderees / total_coefficients
                chart_labels.append(classe.libelleclasse)
                chart_values.append(moyenne_classe)

        # Préparation des coefficients des matières
        for matiere in Matiere.objects.all():
            chart_data.append({
                'nom': matiere.nommatiere,
                'coefficient': matiere.id_coeff
            })

    else:
        nombre_classes = 0
        nombre_eleves = 0
        nombre_matieres = 0
        nombre_numeros = 0
        chart_labels = []
        chart_values = []
        chart_data = []

    # Préparer le contexte pour la vue
    context = {
        'nombre_classes': nombre_classes,
        'nombre_eleves': nombre_eleves,
        'nombre_matieres': nombre_matieres,
        'nombre_numeros': nombre_numeros,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'chart_data': json.dumps(chart_data),
        'annee_active': active_annee,
    }

    return render(request, 'tableau_de_bord.html', context)



# Logger pour les erreurs et les actions
logger = logging.getLogger(__name__)

# Vue pour afficher la liste des années scolaires
class AnneeListView(ListView):
    model = Annee
    template_name = 'annee_list.html'
    context_object_name = 'annees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupère l'année scolaire active
        annee_active = Annee.annee_active()
        context['annee_active'] = annee_active
        return context


# Vue pour activer une année scolaire
def activer_annee(request, pk):
    # Récupère l'année scolaire avec l'ID (pk)
    annee = get_object_or_404(Annee, pk=pk)

    # Active l'année scolaire (désactive les autres années)
    annee.activer()

    # Ajouter un message de succès
    messages.success(request, f"L'année scolaire {annee.anneescolaire} a été activée avec succès.")

    # Rediriger vers la liste des années
    return redirect('annee_list')


# Vue pour afficher la liste des années scolaires et l'année active
def liste_annees(request):
    # Récupère l'année scolaire activée
    annee_active = Annee.annee_active()  # Utilise la méthode statique pour obtenir l'année active

    # Si une année active existe, filtrer les objets Ance par cette année
    if annee_active:
        annees_scolaires = Ance.objects.filter(idannee=annee_active)
    else:
        annees_scolaires = []
        messages.warning(request, "Aucune année scolaire active trouvée.")

    # Filtrer et trier les années scolaires (afficher uniquement l'année active et inactive)
    annees_inactives = Annee.objects.filter(encours=0)  # Années inactives (encours=False)

    return render(request, 'annee_list.html', {
        'annee_active': annee_active,
        'annees_scolaires': annees_scolaires,
        'annees_inactives': annees_inactives  # Vous pouvez utiliser cette variable si vous souhaitez afficher les années désactivées.
    })


# Vue pour ajouter une nouvelle année scolaire
def ajouter_annee(request):
    if request.method == 'POST':
        form = AnneeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'année scolaire a été ajoutée avec succès.")
            return redirect('annee_list')  # Rediriger vers la liste des années après l'ajout
    else:
        form = AnneeForm()

    return render(request, 'ajouter_annee.html', {'form': form})


# Vue pour mettre à jour une année scolaire
class AnneeUpdateView(UpdateView):
    model = Annee
    fields = ['anneescolaire', 'datedebut', 'datefin']  # Les champs que vous souhaitez éditer
    template_name = 'annee_update.html'
    success_url = reverse_lazy('annee_list')  # Redirige vers la liste après la mise à jour


# Vue AJAX pour supprimer une année scolaire
def supprimer_annee_ajax(request, pk):
    if request.method == 'POST':
        annee = get_object_or_404(Annee, pk=pk)

        # Assurez-vous que l'année scolaire active ne peut pas être supprimée
        if annee.encours:
            return JsonResponse({'success': False, 'error': 'Impossible de supprimer l\'année scolaire active.'})

        annee.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Requête invalide.'})


def bulletin_list(request):
    """
    Liste des bulletins par classe.
    """
    classe_id = request.GET.get('classe_id')
    if classe_id:
        try:
            classe = Classe.objects.get(id=classe_id)
            bulletins = Bulletin.objects.filter(classe=classe)
        except Classe.DoesNotExist:
            bulletins = Bulletin.objects.none()  # Si la classe n'existe pas, ne pas afficher de bulletins
    else:
        bulletins = Bulletin.objects.all()

    classes = Classe.objects.all()

    return render(request, 'bulletin_list.html', {
        'bulletins': bulletins,
        'classes': classes,
        'selected_classe': classe_id
    })

def bulletin_create(request):
    """
    Création d'un nouveau bulletin.
    """
    if request.method == 'POST':
        eleve_id = request.POST.get('eleve')
        classe_id = request.POST.get('classe')
        trimester = request.POST.get('trimester')

        if not eleve_id or not classe_id or not trimester:
            return JsonResponse({'success': False, 'message': 'Tous les champs sont requis.'})

        try:
            eleve = Eleve.objects.get(id=eleve_id)
            classe = Classe.objects.get(id=classe_id)
        except Eleve.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Élève non trouvé.'})
        except Classe.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Classe non trouvée.'})

        # Création automatique du bulletin
        bulletin = Bulletin.objects.create(
            eleve=eleve,
            classe=classe,
            trimester=trimester
        )
        bulletin.save()  # Calcul automatique dans la méthode save()

        return JsonResponse({'success': True, 'message': 'Bulletin créé avec succès.'})

    else:
        classes = Classe.objects.all()
        eleves = Eleve.objects.all()
        return render(request, 'bulletin_form.html', {
            'classes': classes,
            'eleves': eleves
        })


def bulletin_update(request, pk):
    """
    Mettre à jour un bulletin existant.
    """
    bulletin = get_object_or_404(Bulletin, pk=pk)

    if request.method == 'POST':
        eleve_id = request.POST.get('eleve')
        classe_id = request.POST.get('classe')
        trimester = request.POST.get('trimester')

        if not eleve_id or not classe_id or not trimester:
            return JsonResponse({'success': False, 'message': 'Tous les champs sont requis.'})

        try:
            bulletin.eleve = Eleve.objects.get(id=eleve_id)
            bulletin.classe = Classe.objects.get(id=classe_id)
        except Eleve.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Élève non trouvé.'})
        except Classe.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Classe non trouvée.'})

        bulletin.trimester = trimester
        bulletin.save()  # Cela déclenchera les calculs automatiques dans la méthode save()

        return JsonResponse({'success': True, 'message': 'Bulletin mis à jour avec succès.'})

    else:
        classes = Classe.objects.all()
        eleves = Eleve.objects.all()
        return render(request, 'bulletin_form.html', {
            'bulletin': bulletin,
            'classes': classes,
            'eleves': eleves
        })


def bulletin_delete(request, pk):
    """
    Suppression d'un bulletin.
    """
    try:
        bulletin = Bulletin.objects.get(pk=pk)
        bulletin.delete()
        return JsonResponse({'success': True, 'message': 'Bulletin supprimé avec succès.'})
    except Bulletin.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Bulletin non trouvé.'})




def tous_les_bulletins(request, class_id=None):
    # Récupérer toutes les classes
    classes = Classe.objects.all()

    # Si un class_id est passé, récupère la classe et les bulletins associés
    if class_id:
        selected_class = get_object_or_404(Classe, idclasse=class_id)
        # Récupérer tous les bulletins des élèves de la classe sélectionnée
        bulletins = Bulletin.objects.filter(eleve__ance__idclasse=selected_class)
    else:
        selected_class = None
        bulletins = Bulletin.objects.none()  # Si pas de classe sélectionnée, ne rien afficher

    context = {
        'classes': classes,
        'selected_class': selected_class,
        'bulletins': bulletins,  # Passer la liste des bulletins au template
    }

    # Rendre le template
    return render(request, 'tous_les_bulletins.html', context)

def bulletin_pdf(request, nummatricule, trimester):
    # Logique pour récupérer les données de l'élève et des notes
    eleve = Eleve.objects.get(nummatricule=nummatricule)
    # Récupérer les notes en fonction du trimestre
    # ... (votre logique ici)

    context = {
        'eleve': eleve,
        'selected_trimester': trimester,
        # Ajoutez d'autres données nécessaires au contexte
    }
    return render(request, 'bulletin_pdf.html', context)

def bulletin_par_classe(request):
    # Récupérer l'ID de la classe sélectionnée
    selected_class_id = request.GET.get('class_id')

    # Récupérer toutes les classes
    classes = Classe.objects.all()

    # Récupérer l'année scolaire active
    annee_active = Annee.objects.filter(encours=True).first()

    eleves = []
    selected_class = None
    eleve_data = []

    if selected_class_id and annee_active:
        # Récupérer la classe sélectionnée
        selected_class = get_object_or_404(Classe, idclasse=selected_class_id)

        # Récupérer les élèves associés à la classe et à l'année active
        eleves = Eleve.objects.filter(
            ance__idclasse=selected_class,
            ance__idannee=annee_active
        ).distinct()

        for eleve in eleves:
            ance = Ance.objects.filter(nummatricule=eleve, idclasse=selected_class).first()
            if ance:
                matieres = Matiere.objects.filter(idclasse=selected_class)
                moyennes = {}

                for trimestre in range(1, 4):
                    total_notes_ponderees = 0
                    total_coefficients = 0

                    notes = Note.objects.filter(ance=ance, periode=trimestre)
                    for matiere in matieres:
                        note = notes.filter(codemat=matiere.codemat).first()
                        if note:
                            coefficient = matiere.id_coeff
                            total_notes_ponderees += note.note * coefficient
                            total_coefficients += coefficient

                    moyenne_trimestre = total_notes_ponderees / total_coefficients if total_coefficients > 0 else None
                    moyennes[f"{trimestre}ème_trimestre"] = moyenne_trimestre

                eleve_data.append({
                    'eleve': eleve,
                    'moyennes': moyennes,
                })

    context = {
        'classes': classes,
        'selected_class': selected_class,
        'eleves': eleve_data,
        'annee_active': annee_active,
    }

    return render(request, 'bulletin_par_classe.html', context)
def bulletin_par_eleve(request, id_matricule):
    # Récupérer l'élève par son matricule
    eleve = get_object_or_404(Eleve, nummatricule=id_matricule)

    # Vérifier si l'élève est inscrit dans une classe via Ance
    ance = Ance.objects.filter(nummatricule=eleve).first()
    if not ance:
        return render(request, 'bulletin_par_eleve.html', {'error': "L'élève n'est inscrit dans aucune classe."})

    classe = ance.idclasse  # Récupérer la classe de l'élève depuis le modèle Ance
    matieres = Matiere.objects.filter(idclasse=classe)  # Récupérer les matières associées à cette classe

    # Récupérer les notes de l'élève pour chaque matière et chaque trimestre
    selected_trimester = request.GET.get('trimester', '1')  # Par défaut au premier trimestre si non spécifié
    try:
        selected_trimester = int(selected_trimester)
    except ValueError:
        selected_trimester = 1  # Par défaut au premier trimestre si invalide

    notes = Note.objects.filter(ance=ance, periode=selected_trimester)

    # Calculer les notes pondérées et les totaux
    total_notes_ponderees = 0
    total_coefficients = 0
    context_notes = []

    for matiere in matieres:
        note_matiere = notes.filter(codemat=matiere.codemat).first()
        if note_matiere:
            coefficient = matiere.id_coeff
            note = note_matiere.note
            note_ponderee = note * coefficient
            context_notes.append({
                'matiere': matiere,
                'note': note,
                'coefficient': coefficient,
                'note_ponderee': note_ponderee
            })
            total_notes_ponderees += note_ponderee
            total_coefficients += coefficient

    # Calculer la moyenne de l'élève
    moyenne_periode = total_notes_ponderees / total_coefficients if total_coefficients else 0

    # Récupérer tous les élèves de la classe
    eleves_classe = Eleve.objects.filter(ance__idclasse=classe)

    # Nombre d'élèves dans la classe
    nombre_eleves_classe = eleves_classe.count()

    # Moyenne globale de la classe
    total_notes_ponderees_classe = 0
    total_coefficients_classe = 0

    for eleve_classe in eleves_classe:
        ance_classe = Ance.objects.filter(nummatricule=eleve_classe, idclasse=classe).first()
        if ance_classe:
            notes_classe = Note.objects.filter(ance=ance_classe, periode=selected_trimester)
            for matiere in matieres:
                note_matiere_classe = notes_classe.filter(codemat=matiere.codemat).first()
                if note_matiere_classe:
                    coefficient = matiere.id_coeff
                    total_notes_ponderees_classe += note_matiere_classe.note * coefficient
                    total_coefficients_classe += coefficient

    # Calculer la moyenne pondérée de la classe
    moyenne_classe = total_notes_ponderees_classe / total_coefficients_classe if total_coefficients_classe > 0 else 0

    # Classement de l'élève basé sur sa moyenne
    rang = None
    if moyenne_periode > 0:
        # Récupérer les moyennes des autres élèves
        moyennes_classe = []
        for eleve_classe in eleves_classe:
            ance_classe = Ance.objects.filter(nummatricule=eleve_classe, idclasse=classe).first()
            if ance_classe:
                notes_classe = Note.objects.filter(ance=ance_classe, periode=selected_trimester)
                total_notes_ponderees_classe = 0
                total_coefficients_classe = 0
                for matiere in matieres:
                    note_matiere_classe = notes_classe.filter(codemat=matiere.codemat).first()
                    if note_matiere_classe:
                        coefficient = matiere.id_coeff
                        total_notes_ponderees_classe += note_matiere_classe.note * coefficient
                        total_coefficients_classe += coefficient
                moyenne_classe_eleve = total_notes_ponderees_classe / total_coefficients_classe if total_coefficients_classe else 0
                moyennes_classe.append(moyenne_classe_eleve)

        # Classement de l'élève en fonction de sa moyenne parmi les autres élèves
        rang = sorted(moyennes_classe, reverse=True).index(moyenne_periode) + 1

    # Appréciation basée sur la moyenne de l'élève
    if moyenne_periode >= 16:
        appreciation = "Très bien"
    elif moyenne_periode >= 14:
        appreciation = "Bien"
    elif moyenne_periode >= 12:
        appreciation = "Assez bien"
    elif moyenne_periode >= 10:
        appreciation = "Passable"
    else:
        appreciation = "Insuffisant"

    # Décision du Conseil de Classe
    if moyenne_periode >= 10:
        decision_conseil = "Passé(e)"
    else:
        decision_conseil = "Redoublant(e)"

    context = {
        'eleve': eleve,
        'classe': classe,
        'notes_ponderees': context_notes,
        'total_notes_ponderees': total_notes_ponderees,
        'total_coefficients': total_coefficients,
        'moyenne_periode': moyenne_periode,
        'moyenne_classe': moyenne_classe,
        'rang': rang,
        'nombre_eleves_classe': nombre_eleves_classe,
        'appreciation': appreciation,  # Ajout de l'appréciation
        'decision_conseil': decision_conseil,  # Ajout de la décision du conseil
        'selected_trimester': selected_trimester,  # Ajout pour le modèle
    }

    return render(request, 'bulletin_par_eleve.html', context)

def eleves_par_classe(request):
    # Récupérer toutes les classes
    classes = Classe.objects.all()

    # Récupérer l'année scolaire active
    annee_active = Annee.objects.filter(encours=True).first()

    # Définir une classe par défaut (première classe de la liste) si aucune n'est spécifiée
    default_class = classes.first()

    # Récupérer la classe sélectionnée depuis les paramètres GET
    selected_class_id = request.GET.get('class_id')

    # Initialisation des données
    data = []

    if selected_class_id:
        # Filtrer la classe sélectionnée
        try:
            classe = Classe.objects.get(idclasse=selected_class_id)
        except Classe.DoesNotExist:
            # Si l'ID de la classe est invalide, utiliser la classe par défaut
            classe = default_class
    else:
        # Utiliser la classe par défaut si aucune classe n'est sélectionnée
        classe = default_class

    # Vérifier si l'année scolaire active existe
    if annee_active:
        # Récupérer les élèves de la classe sélectionnée ou par défaut, mais uniquement pour l'année active
        if classe:
            eleves = Ance.objects.filter(idclasse=classe, idannee=annee_active).select_related('nummatricule')
            data = [{'classe': classe, 'eleves': eleves}]
    else:
        # Si aucune année active, ne pas afficher d'élèves
        data = []

    context = {
        'classes': classes,  # Toutes les classes pour le champ de sélection
        'data': data,  # Liste des élèves pour la classe sélectionnée
        'selected_class_id': classe.idclasse if classe else None,  # ID de la classe affichée
        'annee_active': annee_active,
    }

    return render(request, 'eleves_par_classe.html', context)



def tableau_notes(request):
    # Récupérer la classe sélectionnée depuis la requête GET
    classe_id = request.GET.get('classe', None)
    classes = Classe.objects.all()  # Récupérer toutes les classes pour le formulaire

    # Filtrer les élèves par classe si une classe est sélectionnée
    if classe_id:
        eleves = Eleve.objects.filter(classe_id=classe_id)
    else:
        eleves = Eleve.objects.all()

    resultats = []

    for eleve in eleves:
        # Récupérer les notes de l'élève en optimisant avec select_related
        notes = Note.objects.filter(relationglobale__eleve=eleve).select_related('codemat', 'relationglobale')

        total_notes = 0
        total_coefficients = 0
        details_notes = []

        for note_obj in notes:
            # Vérification de la présence de données et gestion des valeurs nulles
            note = note_obj.note if note_obj.note is not None else 0
            coefficient = note_obj.codemat.id_coeff if note_obj.codemat and note_obj.codemat.id_coeff else 0

            total_notes += note * coefficient
            total_coefficients += coefficient

            details_notes.append({
                'matiere': note_obj.codemat.id_matiere_propre.nommatiere,  # Nom de la matière via codemat
                'note': note,
                'coefficient': coefficient,
                'note_ponderee': note * coefficient
            })

        # Calcul de la moyenne
        moyenne = total_notes / total_coefficients if total_coefficients else 0

        resultats.append({
            'eleve': eleve,
            'details_notes': details_notes,
            'moyenne': round(moyenne, 2),
            'total_notes': round(total_notes, 2),
        })

    context = {
        'classes': classes,
        'selected_classe': classe_id,
        'resultats': resultats,
    }

    return render(request, 'tableau_notes.html', context)


# Coefficient CRUD
def coefficient_list(request):
    coefficients = Coefficient.objects.all()
    return render(request, 'coefficient_list.html', {'coefficients': coefficients})


def coefficient_create(request):
    if request.method == 'POST':
        form = CoefficientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'{reverse("coefficient_list")}?success=true')
    else:
        form = CoefficientForm()
    return render(request, 'coefficient_form.html', {'form': form})

def coefficient_update(request, pk):
    coefficient = get_object_or_404(Coefficient, pk=pk)
    if request.method == 'POST':
        form = CoefficientForm(request.POST, instance=coefficient)
        if form.is_valid():
            form.save()
            return redirect('coefficient_list')
    else:
        form = CoefficientForm(instance=coefficient)
    return render(request, 'coefficient_form.html', {'form': form})

def coefficient_delete(request, pk):
    coefficient = get_object_or_404(Coefficient, pk=pk)
    if request.method == 'POST':
        coefficient.delete()
        return redirect('coefficient_list')
    return render(request, 'coefficient_confirm_delete.html', {'coefficient': coefficient})
@login_required
def matiere_list(request):
    selected_class_id = request.GET.get('class_id', None)
          # Récupérer l'année scolaire active
    annee_active = Annee.objects.filter(encours=True).first()
    # Récupérer l'année scolaire active
    active_annee = Annee.objects.filter(encours=True).first()

    # Si aucune année n'est active, afficher une erreur
    if not active_annee:
        messages.error(request, "Aucune année scolaire active trouvée.")
        return redirect('annee_list')

    # Récupérer les matières
    matieres = Matiere.objects.all()

    if selected_class_id:
        try:
            selected_class = Classe.objects.get(idclasse=selected_class_id)
            ance_instances = Ance.objects.filter(idclasse=selected_class, idannee=active_annee, aquite=1)
            matieres = matieres.filter(idclasse__in=[ance.idclasse for ance in ance_instances])
        except Classe.DoesNotExist:
            matieres = Matiere.objects.none()

    # Ajouter le type d'utilisateur connecté au contexte
    typeutilisateur = request.user.typeutilisateur if hasattr(request.user, 'typeutilisateur') else None

    return render(request, 'matiere_list.html', {
        'matieres': matieres,
        'classes': Classe.objects.all(),
        'selected_class_id': selected_class_id,
        'active_annee': active_annee,
        'typeutilisateur': typeutilisateur,
        'annee_active': annee_active,
    })

def matiere_create(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Matière ajoutée avec succès.')
                return redirect('matiere_list')
            except Exception as e:
                messages.error(request, f"Une erreur s'est produite : {str(e)}")
        else:
            messages.error(request, "Le formulaire contient des erreurs. Veuillez vérifier les champs.")
    else:
        form = MatiereForm()

    return render(request, 'matiere_form.html', {'form': form})

def check_matiere_exists(request):
    if request.method == 'GET':
        idclasse = request.GET.get('idclasse')
        nommatiere = request.GET.get('nommatiere')

        # Vérifier si la matière existe déjà pour la classe donnée
        exists = Matiere.objects.filter(idclasse_id=idclasse, nommatiere=nommatiere).exists()

        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)

def matiere_update(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == 'POST':
        form = MatiereForm(request.POST, instance=matiere)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Matière mise à jour avec succès.')
                return redirect('matiere_list')
            except Exception as e:
                messages.error(request, f"Une erreur s'est produite lors de l'enregistrement : {e}")
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = MatiereForm(instance=matiere)

    return render(request, 'matiere_form.html', {'form': form, 'matiere': matiere})


@csrf_exempt
def matiere_delete(request, pk):
    if request.method == 'POST':
        matiere = get_object_or_404(Matiere, pk=pk)

        try:
            matiere.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Requête invalide."}, status=400)
# CRUD pour MatierePropre

def matiere_propre_list(request):
    # Récupère l'année scolaire activée
    annee_active = Annee.objects.filter(encours=True).first()  # L'année active est celle avec encours=True

    if annee_active:
        # Filtrer les matières propres qui sont liées à l'année scolaire active
        matieres_propres = MatierePropre.objects.filter(
            relationglobale__annee=annee_active
        ).distinct()  # Utilise distinct pour éviter les doublons dans la liste des matières
    else:
        matieres_propres = MatierePropre.objects.none()  # Si aucune année active, ne retourne aucune matière

    return render(request, 'matiere_propre_list.html', {'matieres_propres': matieres_propres})


def matiere_propre_create(request):
    if request.method == 'POST':
        form = MatierePropreForm(request.POST)
        if form.is_valid():
            form.save()
              # Ajouter un message de succès
            messages.success(request, 'Matière ajoutée avec succès.')
            return redirect('matiere_propre_list')
    else:
        form = MatierePropreForm()
    return render(request, 'matiere_propre_form.html', {'form': form})


@csrf_exempt  # Permet aux requêtes AJAX d'éviter la vérification CSRF (pour le développement uniquement)
def matiere_propre_create_ajax(request):
    if request.method == 'POST':
        form = MatierePropreForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Matière ajoutée avec succès.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})

def matiere_propre_create_update_ajax(request, pk=None):
    if request.method == 'POST':
        if pk:
            matiere_propre = get_object_or_404(MatierePropre, pk=pk)
            form = MatierePropreForm(request.POST, instance=matiere_propre)
        else:
            form = MatierePropreForm(request.POST)

        if form.is_valid():
            matiere_propre = form.save()
            return JsonResponse({'success': True, 'message': 'Matière sauvegardée avec succès!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    # Si la méthode n'est pas POST, nous voulons afficher le formulaire
    else:
        if pk:
            matiere_propre = get_object_or_404(MatierePropre, pk=pk)
            form = MatierePropreForm(instance=matiere_propre)
        else:
            form = MatierePropreForm()

    return render(request, 'matiere_propre_form.html', {'form': form, 'matiere_propre': matiere_propre})
# def etudiants_par_annee(request,id):

def matiere_propre_update(request, pk):
    matiere_propre = get_object_or_404(MatierePropre, pk=pk)

    if request.method == 'POST':
        form = MatierePropreForm(request.POST, instance=matiere_propre)
        if form.is_valid():
            # Vérifier si une autre matière avec le même nom existe
            nommatiere = form.cleaned_data['nommatiere']
            if MatierePropre.objects.filter(nommatiere=nommatiere).exclude(pk=matiere_propre.pk).exists():
                form.add_error('nommatiere', 'Une matière avec ce nom existe déjà.')
            else:
                form.save()
                return redirect('matiere_propre_list')
    else:
        form = MatierePropreForm(instance=matiere_propre)

    return render(request, 'matiere_propre_form.html', {'form': form})

def matiere_propre_delete(request, pk):
    if request.method == 'POST':
        try:
            matiere_propre = MatierePropre.objects.get(pk=pk)
            matiere_propre.delete()
            messages.success(request, 'Matière supprimée avec succès.')
            return JsonResponse({'success': True, 'message': 'Matière supprimée avec succès.'})
        except MatierePropre.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Matière introuvable.'})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})

def note_list(request):
     # Récupérer l'année scolaire active
    annee_active = Annee.objects.filter(encours=True).first()
    # Assurez-vous qu'il y a une année scolaire active
    active_annee = Annee.objects.filter(encours=True).first()
    if not active_annee:
        messages.error(request, "Aucune année scolaire active trouvée.")
        return redirect('annee_list')

    # Obtenez les classes pour l'année scolaire active
    classes = Classe.objects.filter(ance__idannee=active_annee).distinct()
    periods = [1, 2, 3]  # Supposons 3 périodes

    selected_class_id = request.GET.get('class_id')
    selected_matiere_id = request.GET.get('matiere_id')
    selected_periode = request.GET.get('periode')

    selected_class = None
    selected_matiere = None
    matieres = []
    eleves = []

    # Si une classe est sélectionnée, obtenez les matières correspondantes
    if selected_class_id:
        selected_class = get_object_or_404(Classe, idclasse=selected_class_id)
        matieres = Matiere.objects.filter(idclasse=selected_class)

        # Obtenez les élèves (Ance) dans la classe sélectionnée
        eleves = Ance.objects.filter(
            idclasse=selected_class,
            idannee=active_annee
        ).select_related('nummatricule')

    # Si une matière est sélectionnée, récupérez l'objet Matiere correspondant
    if selected_matiere_id:
        selected_matiere = get_object_or_404(Matiere, codemat=selected_matiere_id)

    # Validez la période sélectionnée
    if selected_periode and selected_periode.isdigit():
        selected_periode = int(selected_periode)
    else:
        selected_periode = None

    # Traitement de la création de notes via une requête POST (AJAX)
    if request.method == 'POST':
        data = request.POST
        notes = []
        for key, value in data.items():
            if key.startswith("note_") and value.strip():
                matricule = key.split("_")[1]
                eleve = Ance.objects.filter(
                    nummatricule=matricule,
                    idclasse=selected_class,
                    idannee=active_annee
                ).first()

                if eleve:
                    notes.append(Note(
                        ance=eleve,
                        codemat=selected_matiere,
                        note=float(value),
                        periode=selected_periode
                    ))

        if notes:
            Note.objects.bulk_create(notes)
            return JsonResponse({'status': 'success', 'message': 'Les notes ont été enregistrées avec succès.'})
        else:
            return JsonResponse({'status': 'error', 'message': "Aucune note valide à enregistrer."})

    # Rendu du template avec le contexte nécessaire
    return render(request, 'note_list.html', {
        'classes': classes,
        'matieres': matieres,
        'periods': periods,
        'selected_class': selected_class,
        'selected_matiere': selected_matiere,
        'selected_periode': selected_periode,
        'selected_class_id': selected_class_id,
        'selected_matiere_id': selected_matiere_id,
        'eleves': eleves,
        'active_annee': active_annee,
        'annee_active': annee_active,
    })
def ajouter_note(request):
    eleves_filtrés = []

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            # Créer une instance de Note sans la sauvegarder immédiatement
            note = form.save(commit=False)

            # Récupérer l'élève et la classe depuis les données du formulaire
            eleve = form.cleaned_data.get('eleve')
            classe = form.cleaned_data.get('classe')

            # Rechercher la relation Ance correspondante
            try:
                ance = Ance.objects.get(nummatricule=eleve, idclasse=classe)
                note.ance = ance  # Assigner la relation Ance
                note.save()  # Sauvegarder la note
                return redirect('note_list')  # Rediriger après succès
            except Ance.DoesNotExist:
                # Ajouter une erreur au formulaire si la relation Ance est introuvable
                form.add_error(None, "Aucune association trouvée entre l'élève et la classe sélectionnée.")
        else:
            # Gestion des erreurs de validation du formulaire
            form.add_error(None, "Veuillez corriger les erreurs ci-dessous.")
    else:
        # Instanciation du formulaire pour un accès GET
        form = NoteForm()

    # Filtrer les élèves selon la classe sélectionnée via AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        classe_id = request.GET.get('classe_id')
        if classe_id:
            # Filtrer les élèves de la classe sélectionnée via la table de liaison Ance
            eleves_filtrés = Eleve.objects.filter(ance__idclasse=classe_id)
            # Retourner la liste des élèves sous forme de JSON
            return JsonResponse({
                'eleves': [{
                    'id': eleve.nummatricule,
                    'nom': eleve.nom,
                    'prenom': eleve.prenom
                } for eleve in eleves_filtrés]
            })

    return render(request, 'ajouter_note.html', {'form': form})
@login_required
def note_affichage(request):
    # Récupérer l'année scolaire active
    annee_active = Annee.objects.filter(encours=True).first()

    anceList = Ance.objects.filter(
        idannee=annee_active.idannee
    )

    result = []

    for ance in anceList:
        matieres = Matiere.objects.filter(
            idclasse__idclasse=ance.idclasse.idclasse
        )

        notes = Note.objects.filter(
            ance__idnace=ance.idnace
        )
        
        matieres_note_list = []
        for matiere in matieres:
            noteList = list(filter(lambda note: note.codemat.codemat == matiere.codemat, notes))

            if not noteList:
                matieres_note_list.append({
                    'idnote': None,
                    'periode': None,
                    'note': None,
                    'matiere': matiere.nommatiere
                })
            else:
                for item in noteList:
                    matieres_note_list.append({
                        'idnote': item.idnote,
                        'periode': item.periode,
                        'note': item.note,
                        'matiere': matiere.nommatiere
                    })

        result.append({
            'eleve_nom': ance.nummatricule.nom,
            'classe_libelle': ance.idclasse.libelleclasse,
            'matieres_notes': matieres_note_list,
        })        

    # Ajouter le type d'utilisateur connecté au contexte
    typeutilisateur = getattr(request.user, 'typeutilisateur', None)

    # Passer les données au template
    context = {
        'doublons_avec_matiere_et_notes': result,  # Ajouter les doublons avec matières et notes
        'typeutilisateur': typeutilisateur,
        'annee_active': annee_active
    }
    return render(request, 'note_affichage.html', context)



# Vue pour supprimer une note
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        try:
            note.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_affichage')  # Redirigez après mise à jour
    else:
        form = NoteForm(instance=note)

    return render(request, 'note_update.html', {'form': form, 'note': note})
def students_grades(request):
    selected_class_id = request.GET.get('class_id')
    classes = Classe.objects.all()
    selected_class = classes.filter(idclasse=selected_class_id).first() if selected_class_id else None

    matieres = Matiere.objects.filter(idclasse=selected_class) if selected_class else Matiere.objects.none()

    if selected_class:
        students = Ance.objects.filter(idclasse=selected_class)
        grades_by_class = {}
        for student in students:
            grades = Note.objects.filter(ance=student)
            grades_dict = {grade.codemat.id_coeff: grade.note for grade in grades}

            # Créer un dictionnaire avec les matières et les notes associées (ou vide si aucune note)
            student_grades = {matiere.id_coeff: grades_dict.get(matiere.id_coeff, '') for matiere in matieres}
            grades_by_class[student] = student_grades
    else:
        grades_by_class = {}

    context = {
        'classes': classes,
        'selected_class_id': selected_class_id,
        'matieres': matieres,
        'grades_by_class': grades_by_class,
    }
    return render(request, 'students_grades.html', context)



# Vue AJAX pour récupérer les élèves d'une classe donnée
def ajax_get_eleves_par_classe(request):
    classe_id = request.GET.get('classe_id')
    if not classe_id:
        return JsonResponse({'error': 'ID de classe manquant'}, status=400)

    ance_list = Ance.objects.filter(idclasse=classe_id)
    if not ance_list.exists():
        return JsonResponse({'error': 'Aucun élève trouvé pour cette classe'}, status=404)

    data = [
        {'id': ance.nummatricule.id, 'name': f"{ance.nummatricule.nom} {ance.nummatricule.prenom}"}
        for ance in ance_list
    ]
    return JsonResponse(data, safe=False)

def add_note(request, student_id, matiere_id):
    # Récupérer l'élève et la matière correspondants
    eleve = get_object_or_404(Eleve, id=student_id)
    matiere = get_object_or_404(Matiere, idmatiere=matiere_id)

    # Vérifier si une note existe déjà pour cet élève et cette matière
    ance = get_object_or_404(Ance, id_eleve=eleve)  # Assurez-vous que cette relation est correcte
    note_instance = Note.objects.filter(ance=ance, id_matiere=matiere).first()

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note_instance)
        if form.is_valid():
            note = form.save(commit=False)
            note.ance = ance
            note.id_matiere = matiere
            note.save()
            # Redirection après soumission
            return redirect(reverse('note_list') + f'?class_id={ance.id_classe.idclasse}')
    else:
        form = NoteForm(instance=note_instance)

    context = {
        'eleve': eleve,
        'matiere': matiere,
        'form': form,
    }
    return render(request, 'add_note.html', context)

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'note_form.html', {'form': form})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_affichage')
    else:
        form = NoteForm(instance=note)
    return render(request,  'note_form.html', {'form': form})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request,'note_confirm_delete.html', {'note': note})


# Afficher la liste des relations
def relation_list(request):
    relations = RelationGlobale.objects.all()
    return render(request, 'relation_list.html', {'relations': relations})

# Créer une nouvelle relation
def relation_create(request):
    if request.method == 'POST':
        form = RelationGlobaleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Relation créée avec succès.')
            return redirect('relation_list')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = RelationGlobaleForm()
    return render(request, 'relation_form.html', {'form': form})

# Mettre à jour une relation existante
def relation_update(request, pk):
    relation = get_object_or_404(RelationGlobale, pk=pk)
    if request.method == 'POST':
        form = RelationGlobaleForm(request.POST, instance=relation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Relation mise à jour avec succès.')
            return redirect('relation_list')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = RelationGlobaleForm(instance=relation)
    return render(request, 'relation_form.html', {'form': form, 'object': relation})

# Supprimer une relation
def relation_delete(request, pk):
    relation = get_object_or_404(RelationGlobale, pk=pk)
    if request.method == 'POST':
        relation.delete()
        messages.success(request, 'Relation supprimée avec succès.')
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Requête invalide'}, status=400)
def gerer_relation(request):
    if request.method == 'POST':
        form = RelationGlobaleForm(request.POST)
        if form.is_valid():
            # Sauvegarder la relation
            relation = form.save()

            # Retourner une réponse JSON avec les données de la nouvelle relation
            data = {
                'status': 'success',
                'relation': {
                    'annee': str(relation.annee),
                    'classe': str(relation.classe),
                    'eleve': str(relation.eleve),
                    'numero': str(relation.numero),
                    'matiere_propre': str(relation.matiere_propre),
                    'matiere': str(relation.matiere),
                }
            }
            return JsonResponse(data)
        else:
            # En cas d'erreur de validation, retourner un message d'erreur
            errors = form.errors
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
    else:
        form = RelationGlobaleForm()

    # Charger les objets existants pour afficher dans les listes
    relations = RelationGlobale.objects.all()
    return render(request, 'gerer_relation.html', {'form': form, 'relations': relations})

class AnceListView(ListView):
    model = Ance
    template_name = 'ance_list.html'
    context_object_name = 'ances'

class AnceCreateView(CreateView):
    model = Ance
    form_class = AnceForm
    template_name = 'ance_form.html'
    success_url = reverse_lazy('ance_list')

class AnceUpdateView(UpdateView):
    model = Ance
    form_class = AnceForm
    template_name = 'ance_form.html'
    success_url = reverse_lazy('ance_list')

class AnceDeleteView(DeleteView):
    model = Ance
    template_name = 'ance_confirm_delete.html'
    success_url = reverse_lazy('ance_list')

def ance_list(request):
    # Récupérer l'année scolaire active
    annee_active = Annee.annee_active()

    if annee_active:
        # Filtrer les enregistrements de Ance par l'année scolaire active
        ance_records = Ance.objects.filter(idannee=annee_active)
    else:
        ance_records = Ance.objects.all()  # Vous pouvez ajouter un filtre ou un message d'erreur

    context = {
        'ance_records': ance_records,
        'annee_active': annee_active,  # Vous pouvez afficher l'année scolaire active dans le template
    }

    return render(request, 'ance_list.html', context)
