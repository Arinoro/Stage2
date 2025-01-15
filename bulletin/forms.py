from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Utilisateur
from .models import Coefficient ,Classe , Matiere, Note, Ance, Eleve, MatierePropre
from .models import Annee
from .models import RelationGlobale
from .models import Bulletin


class LoginForm(AuthenticationForm):
    """
    Formulaire pour gérer la connexion des utilisateurs.
    Hérite de `AuthenticationForm` pour fonctionner avec le système d'authentification de Django.
    """
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre pseudonyme'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )


class SignUpForm(forms.ModelForm):
    """
    Formulaire pour gérer l'inscription des utilisateurs avec photo de profil.
    """
    motdepasse = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'}),
    )
    confirm_password = forms.CharField(
        label="Confirmez le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'}),
    )
    
    TYPE_UTILISATEUR_CHOICES = [
        ('Directeur', 'Directeur'),
        ('Responsable', 'Responsable'),
    ]
    
    typeutilisateur = forms.ChoiceField(
        choices=TYPE_UTILISATEUR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Type d'utilisateur",
    )

    class Meta:
        model = Utilisateur
        fields = ['pseudoutilisateur', 'nomutilisateur', 'typeutilisateur', 'imguser']

        widgets = {
            'pseudoutilisateur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre pseudonyme'}),
            'nomutilisateur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom complet'}),
            'imguser': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """
        Vérifie si les mots de passe correspondent.
        """
        cleaned_data = super().clean()
        motdepasse = cleaned_data.get("motdepasse")
        confirm_password = cleaned_data.get("confirm_password")

        if motdepasse and confirm_password and motdepasse != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        """
        Sauvegarde le nouvel utilisateur avec un mot de passe hashé.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['motdepasse'])  # Hashage du mot de passe
        if commit:
            user.save()
        return user

    
class AnneeForm(forms.ModelForm):
    class Meta:
        model = Annee
        fields = ['anneescolaire', 'datedebut', 'datefin', 'encours']  # Champs du modèle
        labels = {
            'anneescolaire': 'Année scolaire',  # Nouveau texte du label
            'datedebut': 'Date de début',
            'datefin': 'Date de fin',
            'encours': 'En cours',
        }
        widgets = {
            'anneescolaire': forms.TextInput(attrs={
                'class': 'form-control', 
                'style': 'background-color: #f0f8ff; color: #333;',  # Couleur de fond et couleur du texte
                'placeholder': 'Saisissez l\'année scolaire (ex : 2024-2025)'
            }),
            'datedebut': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',  # Type date pour le champ
                'style': 'background-color: #f0f8ff; color: #333;',
                'placeholder': 'Sélectionnez la date de début'
            }),
            'datefin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Type date pour le champ
                'style': 'background-color: #f0f8ff; color: #333;',
                'placeholder': 'Sélectionnez la date de fin'
            }),
          'encours': forms.NumberInput(attrs={
    'class': 'form-control',  # Classe Bootstrap pour un champ de saisie stylé
    'style': 'width: 120px; text-align: center;',  # Ajustement pour une meilleure présentation
    'placeholder': '0 ou 1',  # Indication pour l'utilisateur
    'min': '0',  # Valeur minimale (par exemple, 0)
    'max': '1',  # Valeur maximale (par exemple, 1)
    'step': '1',  # Incrément par défaut
    'aria-label': 'Encours',  # Description pour l'accessibilité
})

        }

        
        
class CoefficientForm(forms.ModelForm):
    class Meta:
        model = Coefficient
        fields = ['coeff']
        widgets = {
            'coeff': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
# Formulaire pour MatierePropre
class MatierePropreForm(forms.ModelForm):
    class Meta:
        model = MatierePropre
        fields = ['nommatiere']  # Champs de la matière propre
        labels = {
            'nommatiere': 'Nom de la matière',  # Nouveau texte du label
        }
        widgets = {
            'nommatiere': forms.TextInput(attrs={
                'class': 'form-control', 
                'style': 'background-color: #f0f8ff; color: #333;',  # Couleur de fond et couleur du texte
                'placeholder': 'Saisissez le nom de la matière'
            }),
        }


# Formulaire pour Matiere
class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nommatiere', 'id_coeff', 'idclasse']  # Champs pour la relation intermédiaire
        widgets = {
            'nommatiere': forms.TextInput(attrs={'class': 'form-control'}),
            'id_coeff': forms.TextInput(attrs={'class': 'form-control'}),
            'idclasse': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MatiereForm, self).__init__(*args, **kwargs)
        self.fields['nommatiere'].label = "Nom matière"  # Légende personnalisée
        self.fields['id_coeff'].label = "Coefficient"  # Légende personnalisée
        self.fields['idclasse'].label = "Sélectionner la classe"  # Légende personnalisée

    # Ajout de la validation personnalisée
    def clean(self):
        cleaned_data = super().clean()
        idclasse = cleaned_data.get('idclasse')
        nommatiere = cleaned_data.get('nommatiere')  # Utilisation de 'nommatiere' à la place de 'id_matiere_propre'

        # Vérifier si une matière avec la même classe et le même nom existe déjà
        if Matiere.objects.filter(idclasse=idclasse, nommatiere=nommatiere).exists():
            raise forms.ValidationError(
                f"La matière '{nommatiere}' que vous essayez d'entrer est déjà enregistrée pour la classe '{idclasse.libelleclasse}'."
            )
        return cleaned_data


class AnceForm(forms.ModelForm):
    class Meta:
        model = Ance
        fields = ['idannee', 'nummatricule', 'aquite', 'numero', 'idclasse']


class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nummatricule', 'nom', 'prenom', 'datenaissance', 'lieunaissance', 'adresseeleve',
                  'sexe', 'nompere', 'professionpere', 'nommere', 'professionmere', 'nomtuteur',
                  'professiontuteur', 'dateinscription', 'ecoleorigine', 'niveauetude', 'contact',
                  'imgeleve', 'observation', 'estquite', 'reduction', 'volet1', 'volet2', 'volet3']
        


class NoteForm(forms.ModelForm):
    # Champs pour sélectionner un élève, une classe et une matière
    eleve = forms.ModelChoiceField(
        queryset=Eleve.objects.all(),
        empty_label="Sélectionnez un élève",
        label="Élève"
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        empty_label="Sélectionnez une classe",
        label="Classe"
    )
    codemat = forms.ModelChoiceField(
        queryset=Matiere.objects.all(),
        empty_label="Sélectionnez une matière",
        label="Matière"
    )

    class Meta:
        model = Note
        fields = ['note', 'periode', 'codemat', 'eleve', 'classe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configuration des attributs HTML pour les champs
        self.fields['note'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Entrez la note'})
        self.fields['periode'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Entrez la période'})
        self.fields['codemat'].widget.attrs.update({'class': 'form-select'})
        self.fields['eleve'].widget.attrs.update({'class': 'form-select'})
        self.fields['classe'].widget.attrs.update({'class': 'form-select'})

        # Si une instance de Note est fournie et que la relation ance existe, pré-remplir les champs
        if self.instance.pk and hasattr(self.instance, 'ance') and self.instance.ance:
            self.fields['eleve'].initial = self.instance.ance.nummatricule
            self.fields['classe'].initial = self.instance.ance.idclasse
            self.fields['codemat'].initial = self.instance.codemat
        
class AnceForm(forms.ModelForm):
    class Meta:
        model = Ance
        fields = ['idannee', 'nummatricule', 'idclasse', 'numero', 'aquite']
        widgets = {
            'idannee': forms.Select(attrs={'class': 'form-control'}),
            'nummatricule': forms.Select(attrs={'class': 'form-control'}),
            'idclasse': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.Select(attrs={'class': 'form-control'}),
            'aquite': forms.NumberInput(attrs={'class': 'form-control'}),
        }        
        
class RelationGlobaleForm(forms.ModelForm):
    class Meta:
        model = RelationGlobale
        fields = ['annee', 'classe', 'eleve', 'numero', 'matiere_propre', 'matiere']
        widgets = {
            'annee': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.Select(attrs={'class': 'form-control'}),
            'matiere_propre': forms.Select(attrs={'class': 'form-control'}),
            'matiere': forms.Select(attrs={'class': 'form-control'}),
        }

    # Optionnel: Personnalisez des validations supplémentaires si nécessaire
    def clean(self):
        cleaned_data = super().clean()
        # Vous pouvez ajouter des validations personnalisées ici si besoin
        return cleaned_data        
    
    
class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ['eleve', 'classe', 'trimester', 'total_coefficients', 'total_definitive_periode', 
                  'moyenne_periode', 'moyenne_classe', 'appreciation', 'rang', 'matieres_notes']    