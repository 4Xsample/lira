# Changelog

# Etiquetes per a fine-tuning: #changelog #documentation #project_history

Tots els canvis notables en aquest projecte seran documentats en aquest fitxer.

El format es basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
i aquest projecte s'adhereix a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-11-12

Afegit:
- Execució segura de comandes del sistema amb whitelist i flux de permisos interactiu (1=una vegada, 2=sessió, 0=cancel·lar).
- Nous mòduls: `core/perm_session.py`, `core/exec.py`.
- Addicions de configuració d'exemple a `config/lira.yaml`.
- Esquelet de tests: `tests/test_exec.py`, `tests/test_perm_session.py`.
- Fitxer de canvis: `changes/lira-0.1.2-changes.json`.
- API funcional per a la interacció amb models d'Ollama, compatible amb l'API d'OpenAI.
- Models exposats per LIRA ara inclouen el prefix "Lira-" per a una identificació clara en interfícies com Open WebUI.

Notes:
- Denegació per defecte en mode no interactiu.
- Consulteu el README per a la guia d'ús i seguretat.

## [0.1.1] - 2025-11-08

### ✨ Noves Característiques

-   **Model de Llenguatge Configurable:** El model de llenguatge principal ara es pot configurar a través del fitxer `config/lira.yaml`. Això permet canviar fàcilment el model utilitzat per l'orquestrador sense modificar el codi.
-   S'ha afegit `PyYAML` a `requirements.txt` per a la gestió de la configuració.

### ♻️ Canvis i Millores

-   El script `core/lira_api.py` ara carrega la configuració a l'inici per obtenir el port de l'API i el nom del model.
-   **Documentació Actualitzada:** `README.md` i `ROADMAP.md` actualitzats amb els conceptes clau del projecte (integració amb Ollama, OpenWebUI, CLI opcional, arquitectura d'agents).
-   **Llicència i Estil:** `LICENSE` i `README.md` actualitzats per coincidir amb les convencions del projecte (llicència MIT modificada en català, capçalera i peu de pàgina del README).
-   **Documentació Traduïda:** `ROADMAP.md` i `docs/index.md` traduïts al català.
-   **Finançament i Context:** Afegit `FUNDING.yml` i el directori `.gemini_work` per a notes de context, amb `.gemini_work` afegit a `.gitignore`.

## [0.1.0] - 2025-11-08

### 🎉 Versió Inicial

-   Creació de l'estructura inicial del projecte LIRA.
-   Configuració d'un repositori Git amb `.gitignore` bàsic.
-   Creació de la documentació inicial (en anglès):
    -   `README.md` amb una descripció bàsica.
    -   `ROADMAP.md` amb un full de ruta inicial.
    -   `LICENSE` amb la llicència MIT estàndard.
    -   `docs/index.md` com a base per a la documentació detallada.
-   Creació d'un script d'instal·lació (`scripts/install.sh`) que configura LIRA com un servei de systemd, amb mode silenciós i registre.
-   Implementació d'un `core/lira_api.py` placeholder.
-   Configuració inicial de `config/lira.yaml`.