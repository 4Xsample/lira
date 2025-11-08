|               |               |               |               |               |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| ![Hack the planet](https://img.shields.io/badge/Hack-The%20Planet-orange) | [![Discord](https://img.shields.io/discord/667340023829626920?logo=discord)](https://discord.gg/ahVq54p) | [![@4Xsample@mastodon.social](https://img.shields.io/badge/Mastodon-@4Xsample-blueviolet?style=for-the-badge&logo=mastodon)](https://mastodon.social/@4Xsample) | [![4Xsample](https://img.shields.io/badge/Twitch-4Xsample-6441A4?style=for-the-badge&logo=twitch)](https://twitch.tv/4Xsample) | [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=EFVMSRHVBNJP4) |

# LIRA - Agent de Raonament Intel·ligent Lleuger

LIRA és un framework lleuger i extensible per a crear i gestionar agents d'IA, dissenyat per a funcionar amb models de llenguatge locals a través d'Ollama.

## Concepte i Arquitectura

LIRA neix amb l'objectiu de crear un sistema d'agents intel·ligents que operi de manera local, aprofitant la potència dels models de llenguatge moderns sense dependre de serveis al núvol.

L'arquitectura es basa en un agent principal (orquestrador) que actua com a cervell del sistema. Aquest agent, impulsat pel model `gemma2:9b` a través d'Ollama, s'encarrega de:
1.  **Interactuar amb l'usuari:** Rep les peticions a través de diferents interfícies (OpenWebUI, CLI, API).
2.  **Processar la petició:** Analitza la tasca sol·licitada.
3.  **Delegar a agents especialitzats:** Si la tasca requereix una habilitat específica (p. ex., accés a fitxers, execució de codi), l'orquestrador delega la feina a un agent més capacitat.

Aquest disseny modular permet una gran flexibilitat i la possibilitat d'ampliar les capacitats del sistema simplement afegint nous agents.

## Característiques

*   **Integració amb Ollama:** Dissenyat per a funcionar amb models de llenguatge locals a través d'Ollama, amb `gemma2:9b` com a model principal recomanat.
*   **Múltiples Interfícies:**
    *   **OpenWebUI:** Pensat per a ser integrat com a backend a OpenWebUI per a una interacció visual.
    *   **CLI Opcional:** Una interfície de línia de comandes per a un ús més directe i automatitzat.
    *   **API REST:** Una API bàsica per a interactuar amb el nucli de LIRA des d'altres plataformes.
*   **Sistema d'Agents Extensible:** Arquitectura basada en agents especialitzats que poden ser afegits o modificats fàcilment.
*   **Servei Systemd:** S'executa com un servei de systemd per a una gestió fàcil i persistent.

## Instal·lació

Per a instal·lar LIRA, executa l'script d'instal·lació des del directori `scripts`:

```bash
./scripts/install.sh
```

Això instal·larà LIRA a `~/.lira` i configurarà un servei de systemd per a executar l'API de LIRA.

També pots utilitzar la bandera `--yes` per a executar la instal·lació en mode silenciós:

```bash
./scripts/install.sh --yes
```

## Ús

Un cop instal·lat, l'API de LIRA s'executarà a `http://localhost:1312`. Pots comprovar l'estat del servei amb:

```bash
sudo systemctl status lira.service
```

## Contribucions

Les contribucions són benvingudes! Si us plau, no dubtis a enviar un "pull request" o obrir un "issue".

## Llicència

Aquest projecte es distribueix sota una llicència MIT modificada. Consulta el fitxer `LICENSE` per a més detalls.

## Disclaimer

Aquest codi s'ofereix tal com és i no es garanteix que funcioni correctament en totes les condicions. No em faig responsable dels danys que puguin resultar de l'ús d'aquesta informació. Utilitzeu-lo sota la vostra pròpia responsabilitat. Si teniu dubtes, pregunteu.
