# 📋 Rapport de Test - Projet Python\_Testing\_Gudlft

---

## **📊 Métriques globales**


| Métrique                   | Valeur                                                                                                                           | Statut     |
| -------------------------- |----------------------------------------------------------------------------------------------------------------------------------| ---------- |
| **Couverture des tests**   | 99% (server.py)                                                                                                                  | ✅ **Pass** |
| **Nombre total de tests**  | **38** dont:<br/>- tests unitaires :12 (dont 2 suppl.) <br/>- tests integrations:16(dont 5 suppl.)<br/>- tests fonctionnels : 10 | ✅ **Pass** |
| **Tous les tests passent** | Oui                                                                                                                              | ✅ **Pass** |


---

## **🔍 Outils utilisés**

- **Framework de test** : `pytest`
- **Couverture** : `pytest-cov`
- **Mocking** : `pytest-mock`
- **Intégration continue** : GitHub Actions (si applicable)

---

## **📌 Détail des Tests par Phase**

---

### **Phase 1 : Correction des Bugs**

**Objectif** : Corriger les bugs initiaux pour stabiliser l'application.

| **Bug**     | **Description**                                                 | **Tests unitaires**                     | **Tests d'intégration**                                    | **Tests fonctionnels**                                           | **Statut** | **Couverture** |
| ----------- |-----------------------------------------------------------------|-----------------------------------------|------------------------------------------------------------|------------------------------------------------------------------| ---------- | -------------- |
| **Bug 1**   | Crash avec un email inconnu                                     | ✅ `test_club_not_found_by_email`        | ✅ `test_show_summary_with_unknown_client`                  | ✅ `test_user_journey_with_unknown_email`                         | ✅ Pass     | 100%           |
| **Bug 2**   | Empêcher les clubs de dépenser plus de points qu'ils ont        | ✅ `test_club_not_enough_points`         | ✅ `test_purchase_places_without_enough_point`              | ✅ `test_user_journey_purchase_without_enough_points`             | ✅ Pass     | 100%           |
| **Bug 4**   | Limiter à 12 places max par compétition par club                | ✅ `test_club_reservations_exceed_limit` | ✅ `test_purchase_places_exceed_12_places`                  | ✅ `test_user_journey_exceed_12_places`                           | ✅ Pass     | 100%           |
| **Bug 5**   | Empêcher la réservation de places pour des compétitions passées | ✅ `test_competition_is_closed`          | ✅ `test_purchase_places_past_competition`                  | ✅ `test_user_journey_purchase_past_competition`                  | ✅ Pass     | 100%           |
| **Bug 282** | Empêcher la réservation de plus de places que disponibles       | ✅ `test_competition_not_enough_places`  | ✅ `test_purchase_places_without_enough_competition_places` | ✅ `test_user_journey_purchase_without_enough_competition_places` | ✅ Pass     | 100%           |
| **Bug 6**   | Sauvegarder les mises à jour des points dans `clubs.json`       | ✅ `test_save_competitions_to_json`      | ✅ `test_purchase_places_saves_club_points`                 | ✅ `test_user_journey_purchase_saves_points`                      | ✅ Pass     | 100%           |


---

### **Phase 2 : Tableau Public des Points**

**Objectif** : Ajouter un tableau public des points des clubs.

| **Fonctionnalité**         | **Description**                | **Tests unitaires**                 | **Tests d'intégration**    | **Tests fonctionnels**            | **Statut** | **Couverture** |
| -------------------------- | ------------------------------ |-------------------------------------|----------------------------|-----------------------------------| ---------- | -------------- |
| **Tri des clubs**          | Trier les clubs par points     | ✅ `test_get_clubs_sorted_by_points` | ✅ `test_show_points_route` | ✅ `test_user_journey_view_points` | ✅ Pass     | 100%           |
| **Route `/points`**        | Afficher le tableau des points | -                                   | ✅ `test_show_points_route` | ✅ `test_user_journey_view_points` | ✅ Pass     | 100%           |
| **Template `points.html`** | Affichage du tableau           | -                                   | -                          | ✅ `test_user_journey_view_points` | ✅ Pass     | 100%           |


---

## **Structure des tests**

### **Tests unitaires**

- **Dossier** : `/tests/unit/`
- **Fichiers** :
  - `test_club_lookup.py` : test email
  - `test_purchases_places.py` : tests liés aux bogs points/places.
  - `test_is_competition_open.py` : tests liés aux reservations de compétitions passées.
  - `test_get_clubs_sorted_by_points.py` : test rangement des clubs par nombre de points (décroissant pour affichage public des points)
  - `test_additional_increase_cov.py` : tests additionnels pour augmenter la couverture de server.py

### **Tests d'intégration**

- **Dossier** : `/tests/integration/`
- **Fichiers** :
  - `test_show_summary.py` : test pour la route flask `/showSummary`
  - `test_purchase_places.py` et `test_is_competition_open.py`  : test pour la route flask `/purchasePlaces`.
  - `test_show_points_route`: test pour la route `/points`
  - `test_additional_increase_cov.py` : Tests supplémentaires pour augmenter la couverture.

### **Tests fonctionnels**

- **Dossier** : `/tests/functional/`
- **Fichiers** :
  - `test_user_journey.py`: test pour les parcours utilisateurs avec un email inconnu et connu
  - `test_purchase_places.py` et : tests pour les parcours utilisateurs complets liés à la reservation.
  - `test_is_competition_open.py`  : test pour les parcours utilisateurs tentative d'inscription d'une compétition passée
  - `test_points.py` : Tests pour le tableau des points.

---

## **📝 Détail des scénarios testés**

### **Phase 1 : Bugs**

#### **Bug 1 : crash avec un email inconnu**

- **Test unitaire** : vérifie que `find_club_by_email` retourne `None` si le club n'existe pas.
- **Test d'intégration** : vérifie que `/showSummary` gère un email inconnu sans crash.
- **Test fonctionnel** : simule un parcours utilisateur avec un email inconnu.

#### **Bug 2 : limite de points**

- **Test unitaire** : vérifie que `can_club_afford_places` retourne `False` si le club n'a pas assez de points.
- **Test d'intégration** : vérifie que `/purchasePlaces` bloque les réservations si les points sont insuffisants.
- **Test fonctionnel** : simule une réservation avec des points insuffisants.

#### **Bug 4 : limite de 12 places par compétition**

- **Test unitaire** : vérifie que `can_club_book_places` retourne `False` si le club dépasse 12 places.
- **Test d'intégration** : vérifie que `/purchasePlaces` bloque les réservations au-delà de 12 places.
- **Test fonctionnel** : simule une réservation dépassant 12 places.

#### **Bug 5 : Compétitions passées**

- **Test unitaire** : vérifie que `is_competition_open` retourne `False` pour une compétition passée.
- **Test d'intégration** : vérifie que `/purchasePlaces` bloque les réservations pour des compétitions passées.
- **Test fonctionnel** : simule une réservation pour une compétition passée.

#### **Bug 282 : Places disponibles**

- **Test unitaire** : vérifie que `has_competition_enough_places` retourne `False` si la compétition n'a pas assez de places.
- **Test d'intégration** : vérifie que `/purchasePlaces` bloque les réservations si les places sont insuffisantes.
- **Test fonctionnel** : simule une réservation avec des places insuffisantes.

#### **Bug 6 : Sauvegarde des points**

- **Test unitaire** : vérifie que `save_clubs_to_json` sauvegarde correctement les clubs.
- **Test d'intégration** : vérifie que `/purchasePlaces` sauvegarde les points après une réservation.
- **Test fonctionnel** : simule une réservation et vérifie que les points sont mis à jour dans `clubs.json`.

---

### **Phase 2 : Tableau des points**

#### **Tri des clubs**

- **Test unitaire** : vérifie que `get_clubs_sorted_by_points` trie correctement les clubs par points.
- **Test d'intégration** : vérifie que `/points` affiche le tableau des clubs.
- **Test fonctionnel** : simule un parcours utilisateur pour accéder au tableau des points.

---

## **Résultats des tests**

### **Couverture des tests**

- **`server.py`** : **99%** (objectif : 60% ✅)
- **`server_utils.py`** : **100%**

### **Statut global**

- **Tous les tests passent** : ✅
- **Aucun test n'échoue** : ✅
- **Couverture &gt; 60%** : ✅ (99% pour `server.py`)

---

## **Commandes utilisées**

### **Exécuter les tests**

```bash
pytest tests/ -v --cov=server --cov=server_utils --cov-report=term-missing
```

### **Exécuter les tests Unitaires**

```bash
pytest tests/unit/ -v
```

### **Exécuter les tests d'Intégration**

```bash
pytest tests/integration/ -v
```

### **Exécuter les Tests fonctionnels**

```bash
pytest tests/functional/ -v
```

---

## **📌 Conclusion**

- **Tous les bugs de la Phase 1** ont été corrigés et testés.
- **La Phase 2** (tableau des points) a été implémentée et testée.
- **Couverture des tests** : **99% pour `server.py`** (objectif de 60% dépassé).
- **Tous les tests passent** sans erreur.

---

**Date du rapport** : 14 septembre 2026  
Janushan CHRISTY