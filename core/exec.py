"""
Mòdul per a l'execució segura de comandes externes.
Defineix la classe `Executor` per validar i gestionar comandes amb whitelist i permisos de sessió.
# Etiqueta per a fine-tuning: command_execution_security
"""
import subprocess
import shlex
import re
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)

class CommandRejected(Exception):
    """Excepció per a comandes rebutjades per no complir les polítiques de seguretat."""
    pass

class CommandCancelled(Exception):
    """Excepció per a comandes cancel·lades per l'usuari o el sistema."""
    pass

# --- Classe principal per a la gestió de l'execució de comandes ---
class Executor:
    """
    Gestiona l'execució segura de comandes externes.
    Valida comandes amb una whitelist i gestiona permisos de sessió.
    # Etiqueta per a fine-tuning: executor_core_logic
    """
    def __init__(self, whitelist_patterns: List[str], perm_session: object, timeout: int = 30):
        """
        Inicialitza l'Executor.

        Args:
            whitelist_patterns: Llista de patrons (expressions regulars) per validar comandes.
            perm_session: Instància de PermissionSession per a la gestió de permisos.
            timeout: Temps màxim en segons per a l'execució d'una comanda.
        """
        self.whitelist = [re.compile(p) for p in whitelist_patterns]
        self.session = perm_session
        self.timeout = timeout

    def _normalize_key(self, cmd_list: List[str]) -> str:
        """
        Normalitza una clau per al seguiment de permisos de sessió.
        Utilitza el binari de la comanda i el primer argument (si n'hi ha).
        # Etiqueta per a fine-tuning: normalize_command_key
        """
        if not cmd_list:
            return ""
        key_parts = [cmd_list[0]]
        if len(cmd_list) > 1:
            key_parts.append(cmd_list[1])
        return " ".join(key_parts)

    def _match_whitelist(self, cmd_list: List[str]) -> bool:
        """
        Comprova si la comanda coincideix amb algun patró de la whitelist.
        """
        cmd_str = " ".join(cmd_list)
        return any(p.match(cmd_str) for p in self.whitelist)

    def _prompt_console(self, cmd_list: List[str]) -> str:
        """
        Mostra un prompt a la consola per obtenir la decisió de l'usuari sobre l'execució.
        """
        cmd_display = " ".join(shlex.quote(a) for a in cmd_list)
        prompt = (
            f"Comanda sol·licitada: {cmd_display}\n"
            "Tria una opció:\n"
            "1 - Sí, només una vegada\n"
            "2 - Sí, permanent aquesta sessió\n"
            "0 - - Cancel·la i atura\n"
            "> "
        )
        try:
            resp = input(prompt)
        except KeyboardInterrupt:
            logger.warning("Execució de comanda cancel·lada per Ctrl-C: %s", cmd_display)
            raise CommandCancelled("Cancel·lat per Ctrl-C")
        if resp is None:
            logger.warning("Execució de comanda cancel·lada per no-resposta: %s", cmd_display)
            raise CommandCancelled("Cancel·lat per no-resposta")
        resp = resp.strip()
        if resp == '1':
            return 'once'
        if resp == '2':
            return 'session'
        if resp == '0':
            logger.info("Execució de comanda cancel·lada per usuari (0): %s", cmd_display)
            raise CommandCancelled("Cancel·lat per usuari (0)")
        logger.warning("Execució de comanda cancel·lada per resposta invàlida: %s", cmd_display)
        raise CommandCancelled("Cancel·lat per resposta invàlida")

    def decision_from_payload(self, payload: dict) -> str:
        """
        Converteix un payload HTTP/UI en una decisió interna d'execució.
        """
        if not isinstance(payload, dict):
            logger.warning("Payload invàlid rebut per a la decisió de comanda.")
            raise CommandCancelled("Payload invàlid")
        d = str(payload.get("decision", "")).lower()
        if d in ("once", "1"):
            return "once"
        if d in ("session", "2"):
            return "session"
        if d in ("cancel", "0"):
            logger.info("Comanda cancel·lada via payload.")
            raise CommandCancelled("Cancel·lat via payload")
        logger.warning("Decisió invàlida via payload: %s", payload)
        raise CommandCancelled("Decisió invàlida via payload")

    def execute_with_permission(self, cmd_list: List[str], ui_decision_payload: Optional[dict] = None) -> Tuple[int, str, str]:
        """
        Executa una comanda externa amb un sistema de permisos.
        Valida la comanda, comprova permisos de sessió i sol·licita decisió si cal.

        Args:
            cmd_list: Llista de strings que representen la comanda i els seus arguments.
            ui_decision_payload: Opcional. Diccionari amb la decisió si es crida des d'una UI/REST.

        Returns:
            Una tupla amb el codi de retorn, la sortida estàndard (stdout) i l'error estàndard (stderr).

        Raises:
            CommandRejected: Si la comanda no està permesa per la whitelist.
            CommandCancelled: Si l'usuari o el sistema cancel·la l'execució.
        """
        # Validació de la comanda contra la whitelist
        if not self._match_whitelist(cmd_list):
            logger.warning("Comanda no a la whitelist: %s", cmd_list)
            raise CommandRejected("Comanda no permesa per la whitelist")

        cmd_key = self._normalize_key(cmd_list)
        decision = None

        # Comprovació de permisos de sessió
        if self.session.is_allowed(cmd_key):
            decision = 'session'
        else:
            # Sol·licitud de decisió (consola o UI)
            if ui_decision_payload is not None:
                decision = self.decision_from_payload(ui_decision_payload)
            else:
                decision = self._prompt_console(cmd_list)

        # Aplicació de la decisió
        if decision == 'session':
            self.session.allow_session(cmd_key)

        # Execució de la comanda
        try:
            proc = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  timeout=self.timeout, text=True, check=False)
            stdout = proc.stdout or ""
            stderr = proc.stderr or ""
            logger.info("Execució: %s; rc=%s", cmd_list, proc.returncode)
            return proc.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            logger.error("Timeout en executar: %s (després de %ds)", cmd_list, self.timeout)
            return -1, "", f"Timeout after {self.timeout}s"
        except Exception as e:
            logger.exception("Error inesperat durant l'execució de la comanda: %s", cmd_list)
            return -1, "", str(e)