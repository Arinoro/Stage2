# bulletin/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import logout_view
from .views import AnneeListView, activer_annee, AnneeUpdateView
from .views import matiere_propre_create_ajax
from .views import matiere_propre_delete
from .views import matiere_delete
from .views import bulletin_par_eleve
from .views import note_list, students_grades, bulletin_pdf, check_matiere_exists
from .views import supprimer_annee_ajax
from .views import note_affichage
from .views import ajouter_note
from .views import (
    AnceListView,
    AnceCreateView,
    AnceUpdateView,
    AnceDeleteView,
)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL pour la page de connexion
    path('index/', views.index_view, name='index'),  # URL pour la page d'accueil
    path('signup/', views.signup_view, name='signup'),  # URL pour la page d'accueil
    path('logout/', logout_view, name='logout'),
    path('', views.tableau_de_bord_chart, name='tableau_de_bord_chart'),  # Tableau de bord avec graphique
    path('profil/', views.profil_utilisateur, name='profil_utilisateur'),
    path('/', views.tableau_de_bord_chart, name='tableau_de_bord_chart'),
    
    path('annees/', AnneeListView.as_view(), name='annee_list'),
    path('annees/ajouter/', views.ajouter_annee, name='ajouter_annee'),  # Nouvelle URL pour ajouter une année
    path('annees/activer/<int:pk>/', activer_annee, name='activer_annee'),
    path('annees/update/<int:pk>/', AnneeUpdateView.as_view(), name='annee_update'),
    path('supprimer_annee_ajax/<int:pk>/', supprimer_annee_ajax, name='supprimer_annee_ajax'),
    # path('etudiants/<int:annee_id>/', views.etudiants_par_annee, name='etudiants_par_annee'),
    
    path('bulletins/classe/<int:class_id>/', views.tous_les_bulletins, name='tous_les_bulletins'),
    path('bulletin_pdf/<int:nummatricule>/<int:trimester>/', views.bulletin_pdf, name='bulletin_pdf'),
    path('bulletin/', views.bulletin_par_classe, name='bulletin_par_classe'),
    path('bulletin/<int:id_matricule>/', views.bulletin_par_eleve, name='bulletin_par_eleve'),
    path('tableau_notes/', views.tableau_notes, name='tableau_notes'),  # URL pour la vue tableau_notes
    path('students-grades/', students_grades, name='students_grades'),
    path('add_note/<int:student_id>/<int:matiere_id>/', views.add_note, name='add_note'),
    # Coefficient URLs
    path('coefficients/', views.coefficient_list, name='coefficient_list'),
    path('coefficient/add/', views.coefficient_create, name='coefficient_create'),
    path('coefficient/<int:pk>/edit/', views.coefficient_update, name='coefficient_update'),
    path('coefficient/<int:pk>/delete/', views.coefficient_delete, name='coefficient_delete'),
    # Matiere URLs
    path('matieres/', views.matiere_list, name='matiere_list'),
    path('matiere/add/', views.matiere_create, name='matiere_create'),
    path('matiere/<int:pk>/edit/', views.matiere_update, name='matiere_update'),
    path('matiere/delete/<int:pk>/', views.matiere_delete, name='matiere_delete'),
    
    # MatierePropre URLs
    path('matieres_propres/', views.matiere_propre_list, name='matiere_propre_list'),
    path('matiere_propre/add/', views.matiere_propre_create, name='matiere_propre_create'),
    path('matiere_propre/<int:pk>/edit/', views.matiere_propre_update, name='matiere_propre_update'),
    path('matiere_propre_delete/<int:pk>/', matiere_propre_delete, name='matiere_propre_delete'),
    path('matiere/create/', views.matiere_propre_create_update_ajax, name='matiere_propre_create_ajax'),
    path('matiere/update/<int:pk>/', views.matiere_propre_create_update_ajax, name='matiere_propre_update_ajax'),  
    
    # Note URLs
    path('note/add/', views.note_create, name='note_create'),
    path('note/<int:pk>/edit/', views.note_update, name='note_update'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('note/', note_affichage, name='note_affichage'),
        path('notes/', views.note_list, name='note_list'),
    
    path('ajax_get_eleves_par_classe/', views.ajax_get_eleves_par_classe, name='ajax_get_eleves_par_classe'),
    path('note/<int:pk>/edit/', views.note_update, name='note_update'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('ajouter_note/', views.ajouter_note, name='ajouter_note'),
    path('ajouter-note/', views.ajouter_note, name='ajouter_note'),

    # Ajout de la vérification de la matière
    path('check-matiere-exists/', check_matiere_exists, name='check_matiere_exists'),
    path('matiere_propre_create_ajax/', matiere_propre_create_ajax, name='matiere_propre_create_ajax'),

    path('eleves-par-classe/', views.eleves_par_classe, name='eleves_par_classe'),

    path('ances/', AnceListView.as_view(), name='ance_list'),
    path('ances/new/', AnceCreateView.as_view(), name='ance_create'),
    path('ances/<int:pk>/edit/', AnceUpdateView.as_view(), name='ance_update'),
    path('ances/<int:pk>/delete/', AnceDeleteView.as_view(), name='ance_delete'),
    path('relations/', views.relation_list, name='relation_list'),
    path('create/', views.relation_create, name='relation_create'),  # Créer une nouvelle relation
    path('<int:pk>/update/', views.relation_update, name='relation_update'),  # Mettre à jour une relation
    path('<int:pk>/delete/', views.relation_delete, name='relation_delete'),  # Supprimer une relation
    path('gerer-relation/', views.gerer_relation, name='gerer_relation'),
    path('bulletins/', views.bulletin_list, name='bulletin_list'),
    path('bulletin/create/', views.bulletin_create, name='bulletin_create'),
    path('bulletin/delete/<int:pk>/', views.bulletin_delete, name='bulletin_delete'),
    path('bulletin/update/<int:pk>/', views.bulletin_update, name='bulletin_update'),  # Ajout de l'URL
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)