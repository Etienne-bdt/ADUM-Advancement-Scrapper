# ADUM Advancement Scrapper

L'école doctorale has validé my dossier d'inscription

## TODO
 - [ ] Export formations as an ical
 - [ ] Serve said ICAL through a proxy or smth
 - [ ] Enjoy

## Fonctionnement

Le script va query ADUM pour récupérer le status d'inscription et le sauvegarder dans un txt toutes les 30 minutes s'il a changé.
On peut le pair avec une instance gotify pour recevoir une notif.
Il faut compléter le .env avec ses identifiants et le service systemd pour set le répertoire de sauvegarde et le chemin du env.

Il faut installer les paquets spécifié dans le pyprojet aussi.

## Comment l'utiliser ?

1. Setup le venv avec uv ou autre
2. compléter le service systemd avec les chemins relatifs
3. `cp adum_scrapper.service /etc/systemd/system/ && cp adum_scrapper.timer /etc/systemd/system/`
4. `systemctl enable adum_scrapper.timer`
