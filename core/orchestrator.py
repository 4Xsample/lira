"""
Mòdul Orchestrator de LIRA.
Punt d'integració principal per a la gestió i execució segura de comandes.
Carrega la configuració, inicialitza gestors de permisos i execució,
i processa comandes d'agents amb control de permisos.
"""
from core.perm_session import PermissionSession
from core.exec import Executor, CommandRejected, CommandCancelled
import yaml
import logging
import os

logger = logging.getLogger(__name__)

CONFIG_PATH = os.environ.get("LIRA_CONFIG_PATH", "config/lira.yaml")

def load_config(path: str):
    """
    Carrega la configuració des d'un fitxer YAML especificat.
    Retorna un diccionari buit si el fitxer no es troba.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.warning(f"Fitxer de configuració no trobat a: {path}. Utilitzant configuració per defecte.")
        return {}

cfg = load_config(CONFIG_PATH)

whitelist = cfg.get("commands", {}).get("whitelist", [
    r"^ls(\s|$)",
    r"^cat\s+/etc/.*",
    r"^apt\s+update$",
    r"^apt\s+install\s+[-\w]+$"
])
execution_timeout = cfg.get("commands", {}).get("execution_timeout_seconds", 60)

perm = PermissionSession()
executor = Executor(whitelist, perm, timeout=execution_timeout)

def handle_agent_command(cmd_list: list, ui_payload: dict = None) -> dict:
    """
    Gestiona l'execució d'una comanda sol·licitada per un agent.
    Utilitza l'Executor per validar i executar la comanda amb el sistema de permisos.
    """
    try:
        rc, out, err = executor.execute_with_permission(cmd_list, ui_payload)
        return {"status": "ok", "rc": rc, "stdout": out, "stderr": err}
    except CommandRejected as e:
        logger.warning("Comanda rebutjada: %s - Raó: %s", cmd_list, str(e))
        return {"status": "rejected", "reason": str(e)}
    except CommandCancelled as e:
        logger.info("Comanda cancel·lada per l'usuari: %s - Raó: %s", cmd_list, str(e))
        return {"status": "cancelled", "reason": str(e)}
    except Exception as e:
        logger.exception("Error inesperat en gestionar la comanda de l'agent: %s", cmd_list)
        return {"status": "error", "reason": f"Error inesperat: {str(e)}"}
