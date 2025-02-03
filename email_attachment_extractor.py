import imaplib
import email
import os
import logging
from email.header import decode_header
from getpass import getpass

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_attachment.log'),
        logging.StreamHandler()
    ]
)


def recuperer_fichier_joint(
        IMAP_SERVER: str,
        EMAIL_USER: str,
        EMAIL_PASSWORD: str,
        dossier: str = 'INBOX',
        SUBJECT_FILTER: str = None,
        OUTPUT_DIR: str = 'pieces_jointes',
        test_mode: bool = False
):
    """
    Version et gestion complète des erreurs et logging
    """
    try:
        # Vérification/Création du répertoire
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        logging.info(f"Répertoire de sortie : {os.path.abspath(OUTPUT_DIR)}")

        # Connexion IMAP
        logging.info(f"Connexion à {IMAP_SERVER}...")
        with imaplib.IMAP4_SSL(IMAP_SERVER, timeout=10) as mail:
            logging.info("Connexion SSL établie")

            # Authentification
            logging.info(f"Authentification pour {EMAIL_USER}")
            mail.login(EMAIL_USER, EMAIL_PASSWORD)
            logging.info("Authentification réussie")

            # Sélection du dossier
            status, [data] = mail.select(dossier)
            if status != 'OK':
                raise RuntimeError(f"Échec sélection dossier : {status}")
            logging.info(f"Dossier sélectionné : {dossier} ({data.decode()} messages)")

            # Construction de la requête
            criteres = f'(SUBJECT "{SUBJECT_FILTER}")' if SUBJECT_FILTER else 'ALL'
            logging.debug(f"Critères de recherche : {criteres}")

            # Recherche des messages
            status, numeros_messages = mail.search(None, criteres)
            if status != 'OK':
                raise RuntimeError(f"Échec recherche : {status}")

            messages = numeros_messages[0].split()
            if not messages:
                logging.warning("Aucun message trouvé")
                return

            logging.info(f"{len(messages)} message(s) trouvé(s)")

            # Traitement des messages
            for i, num_message in enumerate(messages, 1):
                try:
                    num_str = num_message.decode()
                    logging.info(f"\nTraitement message {i}/{len(messages)} (n°{num_str})")

                    # Récupération du message
                    status, msg_data = mail.fetch(num_message, '(RFC822)')
                    if status != 'OK':
                        logging.error(f"Échec fetch message {num_str} : {status}")
                        continue

                    # Parsing du message
                    email_message = email.message_from_bytes(msg_data[0][1])
                    logging.debug(f"De : {email_message.get('From')}")
                    logging.debug(f"Sujet : {email_message.get('Subject')}")

                    # Traitement des pièces jointes
                    pieces_jointes = 0
                    for part in email_message.walk():
                        content_disposition = part.get_content_disposition()
                        if content_disposition != 'attachment':
                            continue

                        # Décodage du nom de fichier
                        filename = part.get_filename()
                        if not filename:
                            continue

                        # Décodage de l'encodage MIME
                        decoded_filename, encoding = decode_header(filename)[0]
                        if isinstance(decoded_filename, bytes):
                            filename = decoded_filename.decode(encoding or 'utf-8', errors='replace')
                        else:
                            filename = decoded_filename

                        # Nettoyage du nom de fichier
                        filename = filename.replace('\n', '_').replace('\r', '_')
                        logging.info(f"Pièce jointe trouvée : {filename}")

                        # Gestion des doublons
                        base, ext = os.path.splitext(filename)
                        compteur = 1
                        while os.path.exists(os.path.join(OUTPUT_DIR, filename)):
                            filename = f"{base}_{compteur}{ext}"
                            compteur += 1

                        # Sauvegarde
                        filepath = os.path.join(OUTPUT_DIR, filename)
                        try:
                            with open(filepath, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                            pieces_jointes += 1
                            logging.info(f"Sauvegardé → {filepath}")
                        except Exception as save_error:
                            logging.error(f"Échec sauvegarde {filename} : {save_error}")

                    if pieces_jointes == 0:
                        logging.info("Aucune pièce jointe trouvée dans ce message")

                except Exception as msg_error:
                    logging.error(f"Erreur traitement message {num_str} : {msg_error}", exc_info=test_mode)

        logging.info("Déconnexion réussie")

    except imaplib.IMAP4.error as imap_error:
        logging.error(f"Erreur IMAP : {imap_error}")
        if "Invalid credentials" in str(imap_error):
            logging.error("Erreur d'authentification : Vérifiez le mot de passe/app password")
    except Exception as global_error:
        logging.error(f"Erreur globale : {global_error}", exc_info=test_mode)


if __name__ == "__main__":
    # Configuration
    CONFIG = {
        'IMAP_SERVER': 'imap.gmail.com',
        'dossier': 'INBOX',
        'OUTPUT_DIR': 'pieces_jointes',
        'test_mode': True  # Active les détails d'erreurs complets
    }

    # Saisie utilisateur sécurisée
    print("=== Configuration de la récupération ===")
    CONFIG['EMAIL_USER'] = input("Adresse email : ").strip()
    CONFIG['EMAIL_PASSWORD'] = getpass("Mot de passe/app password : ").strip()
    CONFIG['SUBJECT_FILTER'] = input("Filtre par sujet (laisser vide pour tous) : ").strip() or None

    # Exécution
    recuperer_fichier_joint(**CONFIG)

    # Vérification finale
    print("\n=== Vérification finale ===")
    print(f"Répertoire : {os.path.abspath(CONFIG['OUTPUT_DIR'])}")
    print(
        f"Fichiers trouvés : {len(os.listdir(CONFIG['OUTPUT_DIR'])) if os.path.exists(CONFIG['OUTPUT_DIR']) else 0}")