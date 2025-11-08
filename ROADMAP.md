# Full de Ruta de LIRA

Aquest document descriu les característiques i millores planificades per a LIRA.

## Objectius a Curt Termini (v0.2)

*   [ ] **Orquestrador Principal:** Desenvolupar l'agent orquestrador principal que interactua amb `gemma2:9b` via Ollama.
*   [ ] **Sistema de Delegació Bàsic:** Implementar la lògica per a que l'orquestrador pugui delegar tasques a altres agents.
*   [ ] **Integració amb OpenWebUI:** Desenvolupar els endpoints de l'API necessaris per a la integració com a backend a OpenWebUI.
*   [ ] **CLI Bàsica:** Crear una interfície de línia de comandes (CLI) funcional per a la interacció directa amb LIRA.
*   [ ] **Gestor d'Agents:** Implementar un gestor d'agents per carregar i descarregar agents dinàmicament.
*   [ ] **Autenticació de l'API:** Afegir un mecanisme d'autenticació simple amb clau d'API.

## Objectius a Mitjà Termini (v0.5)

*   [ ] **Comunicació Multi-Agent:** Implementar un bus de missatges o un mecanisme similar perquè els agents es comuniquin entre ells de manera més avançada.
*   [ ] **Interfície Web de Gestió:** Crear una interfície web senzilla per gestionar agents, veure logs i configurar LIRA.
*   [ ] **Més Tipus d'Agents:** Desenvolupar una gamma més àmplia d'agents predefinits per a tasques comunes (p. ex., accés a fitxers, execució de codi, cerca web).
*   [ ] **Sistema de Plugins:** Desenvolupar un sistema de plugins per permetre una fàcil extensió de la funcionalitat principal de LIRA.
*   [ ] **Recàrrega de la Configuració:** Permetre que la configuració es pugui recarregar sense reiniciar el servei.
*   [ ] **Registre Millorat:** Implementar un registre més estructurat i permetre la configuració del nivell de registre.

## Objectius a Llarg Termini (v1.0)

*   [ ] **Orquestrador Complet:** Desenvolupar LIRA com un orquestrador d'IA complet amb un ric conjunt de característiques per gestionar fluxos de treball complexos.
*   [ ] **Arquitectura Distribuïda:** Permetre que LIRA s'executi en un entorn distribuït amb múltiples nodes.
*   [ ] **Imatge Oficial de Docker:** Proporcionar una imatge oficial de Docker per a un desplegament fàcil.
*   [ ] **Mercat Comunitari:** Crear un mercat per compartir i descobrir agents i plugins creats per la comunitat.
