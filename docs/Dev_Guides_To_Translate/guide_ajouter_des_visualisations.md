# Ajouter des visualisations

Ce document explique comment ajouter des **visualisations descriptives** au projet, sans modifier les analyses ni introduire d’interprétation.

La visualisation est :
- **optionnelle**,
- **non intrusive**,
- strictement basée sur des données déjà calculées.

---

## Principe fondamental

Les analyses calculent des données.
Les visualisations **les représentent**.

Aucun calcul analytique ne doit être déplacé dans la couche graphique.

---

## Fichiers concernés

- `audio_toolkit/visualization/plots.py` → implémentation de tous les graphes
- `audio_toolkit/engine/runner.py` → déclenchement des visualisations
- `audio_toolkit/engine/results.py` → transport des données

⚠️ Toute implémentation de plot doit se faire **uniquement** dans `plots.py`.

---

## Où les données de visu sont produites

Les données utilisées pour tracer proviennent de :
- `visualization_data` dans `AnalysisResult`, ou
- exceptionnellement de `measurements` (si léger et déjà sérialisable).

Si les données nécessaires n’existent pas :
➡️ les ajouter **dans l’analyse**, pas dans le plot.

---

## Étape 1 — Identifier le type de graphique

Types courants :
- série temporelle
- spectre fréquentiel
- représentation temps-fréquence
- histogramme
- matrice / heatmap

Chaque type correspond à un **pattern de données** clair.

---

## Étape 2 — Ajouter une fonction de plot dans `plots.py`

Créer une fonction `plot_<nom>` qui :
- reçoit uniquement des données prêtes à tracer,
- crée la figure matplotlib,
- sauvegarde via le helper existant,
- ferme explicitement la figure.

Aucune dépendance au runner ou à l’analyse.

---

## Étape 3 — Exposer le plot via `Visualizer`

Dans `plots.py`, ajouter une méthode correspondante dans la classe `Visualizer`.

Rôle du wrapper :
- injecter `dpi`, `formats`, `figsize` depuis la configuration,
- simplifier le code du runner.

---

## Étape 4 — Déclencher la visu dans le runner

Dans `engine/runner.py` :

- détecter la présence de `visualization_data`,
- identifier la méthode (`method identifier`),
- appeler la bonne méthode de `Visualizer`.

Le runner ne fait **aucun calcul**, seulement de l’orchestration.

---

## Gestion des canaux

- Si `visualization_data` est indexé par canal :
  - boucler sur les canaux
- Si la donnée est globale :
  - produire un seul graphe

Le choix est fait **dans l’analyse**, pas dans le plot.

---

## Organisation des fichiers générés

Bonnes pratiques :
- un dossier par méthode
- un fichier par canal et par type de graphique

Exemples :
- `spectral/fft_global_left.png`
- `time_frequency/stft_right.png`

---

## Règles de conception des graphes

- titres descriptifs uniquement
- axes explicitement nommés
- pas de couleur ou annotation suggérant une conclusion
- pas de seuils interprétatifs codés en dur

---

## Checklist avant validation

- le plot fonctionne même si `visualization.enabled = false`
- aucune donnée n’est modifiée pendant le tracé
- toutes les figures sont fermées (`plt.close`)
- le code ne dépend que de `plots.py`

---

## Résumé

| Action | Fichier |
|------|--------|
| Ajouter un plot | `plots.py` |
| Configurer l’apparence | YAML → `Visualizer` |
| Déclencher | `runner.py` |

---

Ce guide définit **la seule façon valide** d’ajouter des visualisations au projet.

