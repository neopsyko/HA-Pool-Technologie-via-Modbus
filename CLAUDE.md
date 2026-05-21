# CLAUDE.md

Ce fichier fournit des indications à Claude Code (claude.ai/code) lors du travail dans ce dépôt.

## Description

Intégration Home Assistant personnalisée (`domain: pool_technologie`) pour les électrolyseurs Pool Technologie (ex. Ibiza iBasel Duo, WaterAir Salt Gold Duo, Just Salt Pro) connectés via Modbus TCP/IP. L'installation se fait via HACS (dépôt personnalisé) ou en copiant le dossier dans `config/custom_components/pool_technologie/` de l'instance HA.

## Installation pour le développement / les tests

Aucun build, suite de tests ni linter n'est configuré. Workflow de développement :

1. Copier les fichiers de l'intégration dans `config/custom_components/pool_technologie/` sur une instance Home Assistant.
2. Redémarrer Home Assistant.
3. Ajouter l'intégration via **Paramètres > Appareils & services > Ajouter une intégration > Pool Technologie**.

Dépendance : `pymodbus>=3.9.2` (déclarée dans `manifest.json`, installée automatiquement par HA).

**Installation via HACS (utilisateur final) :**
HACS > ⋮ > Dépôts personnalisés → ajouter l'URL du dépôt, catégorie *Intégration*. Le `hacs.json` à la racine avec `content_in_root: true` indique à HACS que les fichiers ne sont pas dans un sous-dossier `custom_components/`.

## Architecture

L'intégration suit la structure standard des custom components HA :

- **`models.py`** — source de données centrale : associe les clés de modèle (ex. `ibasel_duo`) à leurs définitions de capteurs (adresse de registre Modbus, facteur d'échelle, unité, précision). Ajouter un nouveau modèle d'appareil se fait ici.
- **`modbus_handler.py`** — fine couche synchrone autour de `pymodbus.ModbusTcpClient`. Ouvre et ferme la connexion TCP à chaque lecture/écriture.
- **`controller.py`** — gère la boucle de polling HA via `async_track_time_interval`. Compte les échecs Modbus consécutifs et passe `modbus_ok` à `False` après 5 échecs. `should_skip_poll()` bloque les lectures quand l'appareil est déconnecté (sonde de reconnexion toutes les `_PROBE_INTERVAL` = 5 itérations).
- **`hacs.json`** — métadonnées HACS. `content_in_root: true` car les fichiers sont à la racine du dépôt.
- **`__init__.py`** — setup de l'entrée : instancie `ModbusHandler` et `PoolController`, les stocke dans `hass.data[DOMAIN][entry_id]`, délègue le setup aux trois plateformes.
- **`sensor.py`** — capteurs en lecture seule. `PoolSensor.update()` est synchrone et appelé depuis le callback de polling du controller. La valeur brute du registre est multipliée par `scale` et arrondie à `precision`.
- **`number.py`** — consignes modifiables pour le pH (registre 4207, échelle `0.000390625`) et l'ORP (registre 4235, échelle 1 mV). Chemin d'écriture : `async_set_native_value` → `handler.write_register`.
- **`binary_sensor.py`** — `ModbusStatusSensor` reflète `controller.modbus_ok`. Vérifie optionnellement l'état d'une entité de filtration avant de reporter l'état OK.
- **`config_flow.py`** — flux de configuration UI (host, port, unit_id, sélecteur de modèle). Le flux d'options existe mais est un stub (retourne des données vides).
- **`translations/fr.json`** — chaînes UI en français pour le flux de configuration et les noms d'entités.

## Conventions importantes

- `hass.data[DOMAIN][entry_id]` contient `{"host", "port", "unit_id", "model", "controller", "scan_interval"}`. Les plateformes `sensor` et `number` créent chacune leur propre instance `ModbusHandler` à partir de ces données, plutôt que de partager celle du controller.
- Mise à l'échelle des capteurs : `valeur_brute * scale`, arrondie à `precision` décimales. La consigne pH utilise une échelle particulière (`0.000390625 ≈ 1/2560`) qui doit être inversée à l'écriture : `raw = round(valeur / scale)`.
- `SCAN_INTERVAL = 60` secondes (défini dans `const.py`).
- Le `_update_callback` du controller est initialisé à un lambda no-op à la construction, puis remplacé par `sensor.py` dans `async_setup_entry` une fois les entités créées.
- Gestion de la déconnexion : après `_modbus_fail_threshold` (5) échecs consécutifs, `should_skip_poll()` retourne `True` et bloque les lectures. Une sonde est autorisée toutes les `_PROBE_INTERVAL` (5) itérations. Un succès remet `_modbus_fail_count` et `_probe_counter` à zéro.

## Ajouter un nouveau modèle

1. Ajouter une entrée dans `MODELS` dans `models.py` avec la clé du modèle, son nom d'affichage et la liste des capteurs (adresse, scale, unit, precision, icon).
2. Si le nouveau modèle a des consignes modifiables différentes, ajouter les sous-classes `NumberEntity` correspondantes dans `number.py`.
3. Ajouter les traductions dans `translations/fr.json`.
4. Incrémenter la `version` dans `manifest.json`.
