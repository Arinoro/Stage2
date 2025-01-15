from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UtilisateurManager(BaseUserManager):
    """Gestionnaire personnalisé pour le modèle Utilisateur."""

    def create_user(self, pseudoutilisateur, motdepasse=None, **extra_fields):
        if not pseudoutilisateur:
            raise ValueError("Le pseudonyme est requis.")
        
        # Création d'un utilisateur avec les champs extra
        user = self.model(
            pseudoutilisateur=pseudoutilisateur,
            **extra_fields
        )
        user.set_password(motdepasse)  # Hachage du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, pseudoutilisateur, motdepasse=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Permission de staff
        extra_fields.setdefault('is_superuser', True)  # Permission de superutilisateur

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")
        
        return self.create_user(pseudoutilisateur, motdepasse, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """Modèle personnalisé pour les utilisateurs."""

    idutilisateur = models.AutoField(db_column='IDUTILISATEUR', primary_key=True)
    nomutilisateur = models.CharField(db_column='NOMUTILISATEUR', max_length=50, blank=True, null=True)
    pseudoutilisateur = models.CharField(db_column='PSEUDOUTILISATEUR', max_length=50, unique=True)
    typeutilisateur = models.CharField(db_column='TYPEUTILISATEUR', max_length=50, blank=True, null=True)
    valide = models.BooleanField(db_column='VALIDE', default=True)
    statut = models.BooleanField(db_column='STATUT', default=True)
    imguser = models.ImageField(upload_to='user_images/', null=True, blank=True)  # Ajoutez ce champ

    # Champs de gestion Django
    is_staff = models.BooleanField(default=False)  # Requis pour l'administration
    is_active = models.BooleanField(default=True)  # Utilisateur actif/inactif

    # Déclaration du gestionnaire
    objects = UtilisateurManager()

    # Champs nécessaires pour le système d'authentification Django
    USERNAME_FIELD = 'pseudoutilisateur'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'utilisateura'

    def __str__(self):
        return self.pseudoutilisateur or "Utilisateur sans pseudo"






class Annee(models.Model):
    idannee = models.AutoField(db_column='IDANNEE', primary_key=True)
    anneescolaire = models.CharField(db_column='ANNEESCOLAIRE', max_length=128, blank=True, null=True)
    datedebut = models.DateField(db_column='DATEDEBUT', blank=True, null=True)
    datefin = models.DateField(db_column='DATEFIN', blank=True, null=True)
    encours = models.IntegerField(db_column='ENCOURS', default=0)  # 1 pour activé, 0 pour désactivé

    class Meta:
        managed = True
        db_table = 'annee'

    def __str__(self):
        return f'Année {self.anneescolaire}'

    def activer(self):
        """
        Désactive toutes les autres années et active l'année scolaire actuelle.
        """
        # Désactive toutes les autres années scolaires
        Annee.objects.all().update(encours=0)
        # Active cette année scolaire
        self.encours = 1
        self.save()

    @staticmethod
    def annee_active():
        """
        Retourne l'année scolaire actuellement activée (encours=1).
        """
        return Annee.objects.filter(encours=1).first()  # Renvoie la première année active.

class Eleve(models.Model):
    nummatricule = models.AutoField(db_column='NUMMATRICULE', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='NOM', max_length=100)  # Field name made lowercase.
    prenom = models.CharField(db_column='PRENOM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    datenaissance = models.DateField(db_column='DATENAISSANCE', blank=True, null=True)  # Field name made lowercase.
    lieunaissance = models.CharField(db_column='LIEUNAISSANCE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    adresseeleve = models.CharField(db_column='ADRESSEELEVE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ecoleorigine = models.CharField(db_column='ECOLEORIGINE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    niveauetude = models.CharField(db_column='NIVEAUETUDE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nompere = models.CharField(db_column='NOMPERE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    professionpere = models.CharField(db_column='PROFESSIONPERE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nommere = models.CharField(db_column='NOMMERE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    professionmere = models.CharField(db_column='PROFESSIONMERE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nomtuteur = models.CharField(db_column='NOMTUTEUR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    professiontuteur = models.CharField(db_column='PROFESSIONTUTEUR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='CONTACT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    motpasse = models.CharField(db_column='MOTPASSE', max_length=20)  # Field name made lowercase.
    observation = models.CharField(db_column='OBSERVATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sexe = models.CharField(db_column='SEXE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dateinscription = models.DateField(db_column='DATEINSCRIPTION', blank=True, null=True)  # Field name made lowercase.
    volet1 = models.IntegerField(db_column='VOLET1', blank=True, null=True)  # Field name made lowercase.
    volet2 = models.IntegerField(db_column='VOLET2', blank=True, null=True)  # Field name made lowercase.
    volet3 = models.IntegerField(db_column='VOLET3', blank=True, null=True)  # Field name made lowercase.
    estquite = models.IntegerField(db_column='ESTQUITE', blank=True, null=True)  # Field name made lowercase.
    reduction = models.IntegerField(db_column='REDUCTION', blank=True, null=True)  # Field name made lowercase.
    imgeleve = models.CharField(db_column='IMGELEVE', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eleve'

    def __str__(self):
        return f'{self.nom} {self.prenom}'

class Niveau(models.Model):
    idniveau = models.AutoField(db_column='IDNIVEAU', primary_key=True)  # Field name made lowercase.
    nomniveau = models.CharField(db_column='NOMNIVEAU', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tauxniveau = models.FloatField(db_column='TAUXNIVEAU', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'niveau'
    
class Classe(models.Model):
    idclasse = models.AutoField(db_column='IDCLASSE', primary_key=True)  # Field name made lowercase.
    idniveau = models.ForeignKey(Niveau, models.DO_NOTHING, db_column='IDNIVEAU')  # Field name made lowercase.
    libelleclasse = models.CharField(db_column='LIBELLECLASSE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ecolage = models.DecimalField(db_column='ECOLAGE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    nbremax = models.IntegerField(db_column='NBREMAX', blank=True, null=True)  # Field name made lowercase.
    libellecarnet = models.CharField(db_column='LIBELLECARNET', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'classe'
    def __str__(self):
        return f'{self.libelleclasse}'
    def get_moyenne(self):
        # Assurez-vous que 'ance' est le bon champ ForeignKey dans le modèle Note
        notes = Note.objects.filter(ance__id_classe=self.idclasse)  # Filtrer les notes par id_classe dans l'instance de Ance
        if notes:
            return sum(note.note for note in notes) / len(notes)  # Moyenne des notes
        return 0  # Retourne 0 si aucune note n'est trouvée
    
        
class Coefficient(models.Model):
    idcoeff = models.AutoField(primary_key=True)
    coeff = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'coefficient'


    def __str__(self):
        return f' {self.coeff}'

class MatierePropre(models.Model):
    idmatiere = models.AutoField(primary_key=True)  # ID unique de la matière
    nommatiere = models.CharField(max_length=255)  # Nom de la matière

    class Meta:
        managed = False
        db_table = 'matiere_propre'  # Nom exact de la table

    def __str__(self):
        return self.nommatiere
    
class Matiere(models.Model):
    codemat = models.AutoField(primary_key=True)  # Explicit ID field   id_matiere_propre = models.ForeignKey('MatierePropre', on_delete=models.CASCADE, db_column='idmatiere')  # Lien vers la table MatierePropre
    nommatiere = models.CharField(max_length=255)  # Nom de la matière
    id_coeff  = models.IntegerField() # Référence au coefficient
    idclasse = models.ForeignKey(Classe, models.CASCADE, db_column='IDCLASSE')  # Suppression en cascade si nécessaire


    class Meta:
        managed = False
        db_table = 'matieres'  # Utilisation du nom exact de la table

    def __str__(self):
        return self.nommatiere 
class Note(models.Model):
    idnote = models.AutoField(primary_key=True, db_column='idnote')
    note = models.FloatField(verbose_name="Note")  # Permettre des décimales pour les notes
    periode = models.IntegerField(verbose_name="Période")

    # Relation avec la table Ance
    ance = models.ForeignKey(
        'Ance',
        on_delete=models.CASCADE,
        db_column='idnace',
        related_name='notes',
        verbose_name="Association Élève-Classe"
    )

    # Relation avec Matière
    codemat = models.ForeignKey(
        'Matiere',
        on_delete=models.CASCADE,
        db_column='codemat',
        related_name='notes',
        verbose_name="Matière"
    )

    class Meta:
        managed = False  # Passez à True si vous gérez les migrations avec Django
        db_table = 'notes'
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        eleve_nom = (
            f"{self.ance.nummatricule.nom} {self.ance.nummatricule.prenom}"
            if self.ance and self.ance.nummatricule else "Élève inconnu"
        )
        classe_libelle = (
            self.ance.idclasse.libelleclasse
            if self.ance and self.ance.idclasse else "Classe inconnue"
        )
        matiere_nom = (
            self.codemat.nommatiere
            if self.codemat else "Matière inconnue"
        )
        return f"Note de {eleve_nom} pour {matiere_nom} en {classe_libelle}"

    @property
    def eleve(self):
        if self.ance and self.ance.nummatricule:
            return self.ance.nummatricule
        return None

    @property
    def classe(self):
        if self.ance and self.ance.idclasse:
            return self.ance.idclasse
        return None

    @classmethod
    def ajouter_note(cls, ance, codemat, note_value, periode_value):
        """
        Méthode pour ajouter une note à la base de données.
        """
        # Crée une instance de Note avec les données fournies
        new_note = cls(
            ance=ance,
            codemat=codemat,
            note=note_value,
            periode=periode_value
        )
        # Enregistrer dans la base de données
        new_note.save()
        return new_note



class Numero(models.Model):
    numero = models.AutoField(primary_key=True)  # Définir un champ clé primaire

    class Meta:
        managed = False
        db_table = 'numero'  # Utilise la table 'numero' existante dans la base de données.

    def __str__(self):
        return str(self.numero)


class RelationGlobale(models.Model):
    idrelation = models.AutoField(primary_key=True)  # Identifiant unique de la relation
    annee = models.ForeignKey(Annee, on_delete=models.CASCADE, db_column='idannee')  # Lien vers l'année
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, db_column='idclasse')  # Lien vers la classe
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, db_column='nummatricule')  # Lien vers l'élève
    numero = models.ForeignKey(Numero, on_delete=models.CASCADE, db_column='numero')  # Lien vers le numéro
    matiere_propre = models.ForeignKey(MatierePropre, on_delete=models.CASCADE, db_column='idmatiere')  # Lien vers MatierePropre
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, db_column='codemat')  # Lien vers Matieredelete=models.CASCADE, db_column='idnote')  # Lien vers Note

    class Meta:
        managed = False
        db_table = 'relation_globale'  # Nom exact de la table dans la base

    def __str__(self):
        return f'Relation {self.idrelation} entre Annee {self.annee}, Classe {self.classe}, Eleve {self.eleve}'
    
   

class Bulletin(models.Model):
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE)
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE)
    trimester = models.IntegerField(
        choices=[
            (1, '1er Trimestre'),
            (2, '2ème Trimestre'),
            (3, '3ème Trimestre')
        ]
    )
    total_coefficients = models.FloatField(default=0)
    total_definitive_periode = models.FloatField(default=0)
    moyenne_periode = models.FloatField(default=0)
    moyenne_classe = models.FloatField(default=0)
    appreciation = models.CharField(max_length=20)
    rang = models.IntegerField(null=True, blank=True)  # Rang dans la classe pour le trimestre

    # Pour suivre chaque note par matière
    matieres_notes = models.JSONField(default=list)  # Stocke les notes pour chaque matière

    class Meta:
        managed = False
        db_table = 'bulletin'

    def __str__(self):
        return f"Bulletin de {self.eleve.nom} - {self.get_trimester_display()}"

    def save(self, *args, **kwargs):
        """
        Calculer automatiquement les champs dérivés avant la sauvegarde.
        """
        # Récupérer les notes associées à l'élève, la classe et le trimestre
        notes = Note.objects.filter(
            relationglobale__eleve=self.eleve,
            relationglobale__classe=self.classe,
            periode=self.trimester
        )

        # Calcul des totaux et moyennes
        self.total_coefficients = sum(note.codemat.coefficient for note in notes)
        self.total_definitive_periode = sum(note.note * note.codemat.coefficient for note in notes)
        self.moyenne_periode = (
            self.total_definitive_periode / self.total_coefficients
            if self.total_coefficients > 0 else 0
        )

        # Ajout des données calculées au JSON `matieres_notes`
        self.matieres_notes = [
            {
                "matiere": note.codemat.nom,
                "note": note.note,
                "coefficient": note.codemat.coefficient
            } for note in notes
        ]

        # Calcul du rang dans la classe (optionnel)
        # Exemple de logique de calcul pour le rang (à personnaliser)
        bulletins_classe = Bulletin.objects.filter(
            classe=self.classe, trimester=self.trimester
        ).exclude(pk=self.pk)  # Exclure l'actuel bulletin
        all_moyennes = [bulletin.moyenne_periode for bulletin in bulletins_classe]
        all_moyennes.append(self.moyenne_periode)
        sorted_moyennes = sorted(all_moyennes, reverse=True)
        self.rang = sorted_moyennes.index(self.moyenne_periode) + 1

        # Appeler la méthode `save` du parent
        super().save(*args, **kwargs)


class Ance(models.Model):
    idnace = models.BigAutoField(db_column='IDNACE', primary_key=True)  # Field name made lowercase.
    idannee = models.ForeignKey(Annee, models.DO_NOTHING, db_column='IDANNEE')  # Field name made lowercase.
    nummatricule = models.ForeignKey(Eleve, models.DO_NOTHING, db_column='NUMMATRICULE')  # Field name made lowercase.
    idclasse = models.ForeignKey(Classe, models.DO_NOTHING, db_column='IDCLASSE')  # Field name made lowercase.
    numero = models.ForeignKey(Numero, models.DO_NOTHING, db_column='NUMERO')  # Field name made lowercase.
    aquite = models.IntegerField(db_column='AQUITTE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ance'
    def __str__(self):
        return f'Ance {self.nummatricule} for {self.idclasse}'

