|               |               |               |               |               |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| ![Hack the planet](https://img.shields.io/badge/Hack-The%20Planet-orange) | [![Discord](https://img.shields.io/discord/667340023829626920?logo=discord)](https://discord.gg/ahVq54p) | [![@4Xsample@mastodon.social](https://img.shields.io/badge/Mastodon-@4Xsample-blueviolet?style=for-the-badge&logo=mastodon)](https://mastodon.social/@4Xsample) | [![4Xsample](https://img.shields.io/badge/Twitch-4Xsample-6441A4?style=for-the-badge&logo=twitch)](https://twitch.tv/4Xsample) | [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=EFVMSRHVBNJP4) |

# LIRA - Agent de Raonament Intel·ligent Lleuger

LIRA és un framework lleuger i extensible per a crear i gestionar agents d'IA. Està dissenyat per a ser un sistema simple i autocontingut que es pot desplegar i gestionar fàcilment en una màquina local.

## Característiques

*   **API Simple:** Una API bàsica per a interactuar amb el nucli de LIRA.
*   **Servei Systemd:** S'executa com un servei de systemd per a una gestió fàcil.
*   **Extensible:** Dissenyat per a ser fàcilment estès amb nous agents i capacitats.

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