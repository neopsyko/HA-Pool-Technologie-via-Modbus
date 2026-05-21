
MODELS = {
    "ibasel_duo": {
        "name": "Ibiza iBasel Duo",
        "sensors": [
            {
                "name": "Taille du bassin",
                "translation_key": "taille_bassin",
                "unique_id": "taille_bassin",
                "address": 4111,
                "unit": "m³",
                "scale": 1,
                "precision": 0,
                "icon": "mdi:texture-box"
            },
            {
                "name": "pH",
                "translation_key": "ph",
                "unique_id": "ph",
                "address": 259,
                "unit": "pH",
                "scale": 0.001,
                "precision": 1,
                "icon": "mdi:test-tube"
            },
            {
                "name": "Température de l'eau",
                "translation_key": "temperature_eau",
                "unique_id": "temperature_eau",
                "address": 260,
                "unit": "°C",
                "scale": 0.1,
                "precision": 1,
                "icon": "mdi:thermometer-water",
                "device_class": "temperature"
            },
            {
                "name": "Taux de sel",
                "translation_key": "taux_sel",
                "unique_id": "taux_sel",
                "address": 261,
                "unit": "g/L",
                "scale": 0.1,
                "precision": 1,
                "icon": "mdi:shaker-outline"
            },
            {
                "name": "ORP",
                "translation_key": "orp",
                "unique_id": "orp",
                "address": 262,
                "unit": "mV",
                "scale": 1,
                "precision": 0,
                "icon": "mdi:lightning-bolt"
            },
            {
                "name": "Consigne pH",
                "translation_key": "consigne_ph",
                "unique_id": "consigne_ph",
                "address": 4207,
                "unit": "pH",
                "scale": 0.000390625,
                "precision": 1,
                "icon": "mdi:cog"
            },
            {
                "name": "Consigne ORP",
                "translation_key": "consigne_orp",
                "unique_id": "consigne_orp",
                "address": 4235,
                "unit": "mV",
                "scale": 1,
                "precision": 0,
                "icon": "mdi:cog"
            }
        ]
    },
    "just_salt_pro": {
        "name": "Just Salt Pro",
        "sensors": [
            {
                "name": "Taille du bassin",
                "translation_key": "taille_bassin",
                "unique_id": "taille_bassin",
                "address": 4111,
                "unit": "m³",
                "scale": 1,
                "precision": 0,
                "icon": "mdi:texture-box"
            },
            {
                "name": "pH",
                "translation_key": "ph",
                "unique_id": "ph",
                "address": 259,
                "unit": "pH",
                "scale": 0.001,
                "precision": 1,
                "icon": "mdi:test-tube"
            },
            {
                "name": "Température de l'eau",
                "translation_key": "temperature_eau",
                "unique_id": "temperature_eau",
                "address": 260,
                "unit": "°C",
                "scale": 0.1,
                "precision": 1,
                "icon": "mdi:thermometer-water",
                "device_class": "temperature"
            },
            {
                "name": "Taux de sel",
                "translation_key": "taux_sel",
                "unique_id": "taux_sel",
                "address": 261,
                "unit": "g/L",
                "scale": 0.1,
                "precision": 1,
                "icon": "mdi:shaker-outline"
            },
            {
                "name": "ORP",
                "translation_key": "orp",
                "unique_id": "orp",
                "address": 262,
                "unit": "mV",
                "scale": 1,
                "precision": 0,
                "icon": "mdi:lightning-bolt"
            },
            {
                "name": "Consigne pH",
                "translation_key": "consigne_ph",
                "unique_id": "consigne_ph",
                "address": 4207,
                "unit": "pH",
                "scale": 0.000390625,
                "precision": 1,
                "icon": "mdi:cog"
            },
            {
                "name": "Consigne ORP",
                "translation_key": "consigne_orp",
                "unique_id": "consigne_orp",
                "address": 4235,
                "unit": "mV",
                "scale": 1,
                "precision": 0,
                "icon": "mdi:cog"
            }
        ]
    }
}

