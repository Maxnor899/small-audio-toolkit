# Ajouter une nouvelle analyse

Ce document décrit **pas à pas** comment ajouter une nouvelle méthode d’analyse au projet, de façon compatible avec l’architecture existante, exploitable par la configuration **et** optionnellement visualisable.

L’objectif est de garantir :
- des **mesures objectives** uniquement (pas d’interprétation automatique),
- une intégration complète dans le pipeline,
- des résultats exploitables par la couche de visualisation **sans couplage fort**.

---

## Vue d’ensemble du pipeline

```
Configuration YAML
   ↓
Registry (identifier → fonction)
   ↓
Runner (orchestration)
   ↓
Méthode d’analyse
   ↓
AnalysisResult
   ↓
Export JSON  (+ visualisation optionnelle)
```

---

## Fichiers concernés

Pour une nouvelle analyse, les fichiers potentiellement impliqués sont :

- `audio_toolkit/analyses/<categorie>.py` → implémentation de la méthode
- `audio_toolkit/engine/registry.py` → enregistrement de la méthode
- `audio_toolkit/engine/context.py` → structure des données d’entrée
- `audio_toolkit/engine/results.py` → structure du résultat
- `audio_toolkit/engine/runner.py` → exécution + déclenchement des visus
- `audio_toolkit/visualization/plots.py` → génération des graphes (si besoin)

---

## Étape 1 — Choisir la catégorie

La catégorie détermine :
- le fichier Python à modifier,
- la clé utilisée dans la configuration YAML.

Catégories existantes :
- `temporal`
- `spectral`
- `time_frequency`
- `modulation`
- `information`
- `inter_channel`
- `steganography`
- `meta_analysis`

Implémenter la méthode dans le fichier correspondant.

---

## Étape 2 — Implémenter la fonction d’analyse

### Signature attendue

```python
def my_analysis(context, params) -> AnalysisResult:
    ...
```

- `context` est **immutable**
- `params` provient de la configuration (fusion defaults + overrides)

### Bonnes pratiques

- Valider explicitement les paramètres en entrée
- Traiter tous les canaux présents dans `context.audio_data`
- Ne jamais appeler une autre méthode d’analyse
- Ne jamais produire de conclusion ou de label automatique

---

## Étape 3 — Construire l’AnalysisResult

### Champs disponibles

- `method` : identifiant de la méthode
- `measurements` : données **brutes et sérialisables**
- `metrics` : scalaires dérivés (optionnel)
- `anomaly_score` : indicateur numérique optionnel
- `visualization_data` : données dédiées aux graphes (optionnel)

### Règles importantes

- Les informations **critiques** doivent toujours être dans `measurements`
- `visualization_data` peut être supprimé à l’export
- Éviter les booléens du type `detected / encoded / in_phase`

---

## Étape 4 — Ajouter des données de visualisation (optionnel)

### Principe

`visualization_data` contient uniquement des structures **prêtes à être tracées** :
- axes
- séries
- matrices

Aucun calcul ne doit être refait dans la couche de visualisation.

### Exemples de structures

#### Série temporelle
```python
visualization_data[channel] = {
    "time": t,
    "value": y
}
```

#### Spectre
```python
visualization_data[channel] = {
    "frequencies": freqs,
    "magnitudes": mags
}
```

#### Représentation temps-fréquence
```python
visualization_data[channel] = {
    "times": times,
    "frequencies": freqs,
    "matrix": tf
}
```

---

## Étape 5 — Enregistrer la méthode

Dans le registry :

- `identifier` : chaîne unique (utilisée dans le YAML)
- `category`
- `function`
- `default_params`

Sans cette étape, la méthode **n’est pas appelable**.

---

## Étape 6 — Activer via la configuration

```yaml
analyses:
  <categorie>:
    enabled: true
    methods:
      - name: "my_analysis"
        params:
          ...
```

---

## Étape 7 — Vérifier l’intégration complète

Checklist :
- la méthode s’exécute sans visualisation
- la méthode s’exécute avec `visualization.enabled = true`
- les résultats sont présents dans `results.json`
- aucune information critique n’est perdue

---

## Résumé

| Élément | Où |
|------|----|
| Calcul | `analyses/*.py` |
| Activation | `registry.py` + YAML |
| Données | `AnalysisResult` |
| Graphes | `plots.py` via le runner |

---

Ce guide décrit **le contrat à respecter** pour toute nouvelle analyse.