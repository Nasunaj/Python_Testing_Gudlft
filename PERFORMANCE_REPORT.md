# Rapport de performance - Güdlft

---

## ** Date du test**
15 septembre 2026

---

## **🔧 Configuration du test**
- **Outil** : Locust 2.20.0
- **Environnement** : local (machine de développement)
- **Application testée** : Flask (Python_Testing_Gudlft)
- **URL de l'application** : `http://localhost:5000`

---

## **📌 Scénarios Testés**
| Scénario | Description | Endpoint | Méthode |
|----------|-------------|----------|---------|
| Accès à la page d'accueil | Affiche la page d'accueil | `/` | GET |
| Accès au tableau des points | Affiche le tableau des points des clubs | `/points` | GET |
| Réservation de places | Simule une réservation de places | `/purchasePlaces` | POST |

---

## **Résultats**

### **Configuration du test**
- **Nombre total d'utilisateurs** : 100
- **Taux de montée en charge** : 10 utilisateurs/seconde
- **Durée du test** : ~2 minutes

---

### **Métriques globales**
| Métrique | Valeur | Statut |
|----------|--------|--------|
| **Requêtes totales** | 10451 | ✅ |
| **Temps de réponse moyen** | 6.74 ms | ✅ |
| **Requêtes réussies** | 10451 (100%) | ✅ |
| **Requêtes échouées** | 0 (0%) | ✅ |
| **Temps de réponse max** | 758.98 ms | ✅ |

---

### **Détail par Endpoint**
| Endpoint | Requêtes | Succès | Échecs | Temps de Réponse Moyen (ms) | Temps de Réponse Médian (ms) | Temps Max (ms) | Taille Moyenne (octets) |
|----------|----------|--------|--------|--------------------------------|----------------------------------|---------------------|-----------------------------|
| `/` | 3454 | 3454 | 0 | 6.32 | 6.32 | 564 | 16.09 |
| `/points` | 3484 | 3484 | 0 | 6.27 | 6.27 | 518 | 16.23 |
| `/purchasePlaces` | 3513 | 3513 | 0 | 7.60 | 7.60 | 758.98 | 16.36 |

---

## **🔍 Analyse**
- **Performances globales** : bons, avec un temps de réponse moyen de **6.74 ms** pour l'ensemble des endpoints.
- **Points forts** :
  - **100% de succès** : aucune requête n'a échoué.
  - **Temps de réponse bas** : tous les endpoints ont des temps de réponse moyens **inférieurs à 10 ms**.
  - **Stabilité** : les temps de réponse médians et moyens sont très proches, ce qui indique une **latence stable**.
- **Points à améliorer** :
  - Le **temps de réponse maximum** pour `/purchasePlaces` (758.98 ms) est **beaucoup plus élevé** que la moyenne. Cela peut indiquer des **pics de charge** ou des **requêtes complexes** à optimiser.

---

## **📌 Pistes d'amélioration**
1. **Optimiser `/purchasePlaces`** :
   - les requêtes lentes (celles qui prennent jusqu'à 758 ms) .
2. **Tester avec plus d'utilisateurs** : exemple 500 utilisateurs (pour voir le comportement)
---

## **📁 Fichiers Associés**
- **Fichier de configuration Locust** : [locustfile.py](locustfile.py)
- **Résultats bruts** : [locust_results.csv](locust_results.csv)

---

Janushan CHRISTY