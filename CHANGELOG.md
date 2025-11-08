# Changelog

Tots els canvis notables en aquest projecte seran documentats en aquest fitxer.

El format es basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
i aquest projecte s'adhereix a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-11-08

### ✨ Noves Característiques

-   **Model de Llenguatge Configurable:** El model de llenguatge principal ara es pot configurar a través del fitxer `config/lira.yaml`. Això permet canviar fàcilment el model utilitzat per l'orquestrador sense modificar el codi.
-   S'ha afegit `PyYAML` a `requirements.txt` per a la gestió de la configuració.

### ♻️ Canvis i Millores

-   El script `core/lira_api.py` ara carrega la configuració a l'inici per obtenir el port de l'API i el nom del model.

## [0.1.0] - 2025-11-08

### 🎉 Versió Inicial

-   Creació de l'estructura inicial del projecte LIRA.
-   Configuració d'un repositori Git amb `.gitignore`.
-   Creació de la documentació inicial, incloent:
    -   `README.md` amb la visió del projecte, arquitectura i instruccions.
    -   `ROADMAP.md` amb el full de ruta a curt, mitjà i llarg termini.
    -   `LICENSE` amb la llicència MIT modificada.
    -   `docs/index.md` com a base per a la documentació detallada.
-   Creació d'un script d'instal·lació (`scripts/install.sh`) que configura LIRA com un servei de systemd.
-   Afegit un fitxer de finançament `FUNDING.yml`.
-   Creació d'un espai de treball `.gemini_work` per a notes de context.
