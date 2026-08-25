# 🚀 Bot Envoie CV

Une application web locale permettant d'automatiser vos envois de candidatures par mail, de classer vos CVs et lettres de motivation par catégories de poste, et de détecter automatiquement les réponses des recruteurs !

---

## 🛠️ Configuration et Installation

Avant de lancer l'application pour la première fois, vous devez configurer vos identifiants d'email pour que le bot puisse envoyer et lire vos messages (via Gmail).

### Étape 1 : Créer le fichier de configuration
1. Dans le dossier du projet, repérez le fichier nommé **`.env.example`**.
2. Renommez-le simplement en **`.env`** (Assurez-vous qu'il n'y ait rien avant le point).

### Étape 2 : Configurer l'email (Gmail)
Ouvrez le fichier `.env` avec un éditeur de texte. Vous y trouverez ces 3 lignes :
```env
EMAIL_USER=votre_email@gmail.com
EMAIL_PASS=votre_mot_de_passe_d_application
SECRET_KEY=cle_secrete_securisee
```

- **`EMAIL_USER`** : Remplacez par votre adresse Gmail complète (ex: `jean.dupont@gmail.com`).
- **`EMAIL_PASS`** : **N'utilisez pas votre mot de passe habituel !** Vous devez générer un "Mot de passe d'application" Google.
  - Allez sur votre Compte Google > Sécurité.
  - Activez la "Validation en deux étapes" (si ce n'est pas déjà fait).
  - Cherchez "Mots de passe des applications" (dans la barre de recherche des paramètres de sécurité).
  - Créez un mot de passe pour "Autre application" et nommez-le "Bot CV".
  - Copiez les 16 lettres générées (sans espaces) et collez-les ici.
- **`SECRET_KEY`** : Remplacez par une phrase ou une suite de caractères complexe aléatoire (ex: `SuperCleSecrete2026!`). C'est utilisé pour sécuriser les sessions de l'application Flask.

### Étape 3 : Lancer l'application

Le bot est conçu pour être lancé très facilement sans ligne de commande.

- **Sur Windows** : Double-cliquez sur le fichier **`start.bat`**.
- **Sur Mac** : Double-cliquez sur le fichier **`start.command`** (Il faudra peut-être l'autoriser la première fois en ouvrant le terminal et en tapant `chmod +x start.command`).

Le script s'occupe de tout : il installe les dépendances nécessaires et ouvre automatiquement votre navigateur sur **http://127.0.0.1:5000**.

---

## 💡 Utilisation rapide

1. **Catégories** : Allez dans "Admin", créez une catégorie (ex: "Développeur Web"), définissez un corps de mail et joignez votre CV et Lettre de motivation.
2. **Candidature** : Allez dans "Nouvelle Candidature", choisissez votre catégorie, ajoutez autant de lignes "Entreprise" que nécessaire et envoyez la salve.
3. **Réponses** : Sur le "Dashboard", cliquez sur "🔄 Rafraîchir les réponses" pour scanner votre boîte mail et voir si une entreprise vous a répondu !
