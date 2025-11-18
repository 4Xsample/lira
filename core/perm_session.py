"""
Mòdul per a la gestió de permisos a nivell de sessió.
Defineix la classe `PermissionSession` per emmagatzemar i verificar permisos de comandes en memòria.
És segur per a entorns multithread.
"""
import threading

class PermissionSession:
    """
    Gestor simple de permisos en memòria per a una sessió.
    Permet marcar comandes com a 'permeses permanentment' durant la vida del procés.
    Utilitza un `threading.Lock` per garantir la seguretat en entorns concurrents.
    """
    def __init__(self):
        """
        Inicialitza una nova instància de PermissionSession.
        """
        self._lock = threading.Lock()
        self._allowed = set()

    def allow_session(self, cmd_key: str):
        """
        Afegeix una clau de comanda al conjunt de comandes permeses per a la sessió.
        """
        with self._lock:
            self._allowed.add(cmd_key)

    def revoke_session(self, cmd_key: str):
        """
        Elimina una clau de comanda del conjunt de comandes permeses per a la sessió.
        """
        with self._lock:
            self._allowed.discard(cmd_key)

    def is_allowed(self, cmd_key: str) -> bool:
        """
        Comprova si una comanda específica està permesa en la sessió actual.
        """
        with self._lock:
            return cmd_key in self._allowed

    def clear(self):
        """
        Neteja totes les comandes permeses de la sessió.
        """
        with self._lock:
            self._allowed.clear()
