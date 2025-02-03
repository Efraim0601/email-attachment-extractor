# email-attachment-extractor

# Email Attachment Extractor 📧📎

Script Python pour récupérer automatiquement les pièces jointes d'une boîte mail via IMAP avec journalisation et gestion d'erreurs.

### Fonctionnalités

- ✅ Récupération de pièces jointes via IMAP SSL
- ✅ Filtrage par sujet du mail
- ✅ Gestion des doublons de fichiers
- ✅ Journalisation détaillée (fichier + console)
- ✅ Support des encodages complexes
- ✅ Mode debug activable

### Prérequis

- Python 3.6+
- Accès IMAP activé sur votre compte email

### Installation

1. Clonez le dépôt :
```
git clone https://github.com/yourusername/email-attachment-extractor.git
cd email-attachment-extractor
```
2. Installez les dépendances
```
pip install python-dotenv  # Optionnel pour le support .env
```

# Configuration
### Methode recommandée:  Fichier .env
créez un fichier .env à la racine :
```
EMAIL_USER="votre@email.com"
EMAIL_PASSWORD="votre_mot_de_passe"
IMAP_SERVER="imap.gmail.com"
OUTPUT_DIR="pieces_jointes"
SUBJECT_FILTER="RAPPORT MENSUEL"
```

### Methode 2 : Arguments ditrects
```
CONFIG = {
    'serveur_imap': 'imap.gmail.com',
    'email_utilisateur': 'votre@email.com',
    'mot_de_passe': 'votre_app_password',
    'sujet_mail': 'RAPPORT MENSUEL',
    'repertoire_sortie': 'pieces_jointes',
    'test_mode': False
}
```

# Exécution
### Avec le fichier .env :
```
python email_attachment_extractor.py --env .env
```

### Avec la ligne de commande:
```
python email_attachment_extractor.py

```
suivez les invites pour saisir les paramètres.

# Options supplémentaires

```
# Mode debug avec stack traces
python email_attachment_extractor.py --test-mode

# Spécifier un dossier IMAP différent
python email_attachment_extractor.py --dossier "ARCHIVES"
```

# Structure des répertoires

```
.
├── email_attachment_extractor.py  # Script principal
├── pieces_jointes/                # Dossier de sortie par défaut
├── email_attachment.log           # Fichier journal
└── .env                           # Configuration (optionnel)
```



                                                 j'espère que ça ne va pas cuire
