"""
Mòdul de proves unitàries per a la classe `PermissionSession` del mòdul `core.perm_session`.
Assegura que la gestió de permisos a nivell de sessió funciona correctament.
"""
import threading
from core.perm_session import PermissionSession

def test_allow_revoke_is_allowed():
    """
    Verifica la funcionalitat bàsica d'habilitar, comprovar i revocar permisos.
    """
    s = PermissionSession()
    assert not s.is_allowed("cmd a")
    s.allow_session("cmd a")
    assert s.is_allowed("cmd a")
    s.revoke_session("cmd a")
    assert not s.is_allowed("cmd a")

def test_concurrent_allow():
    """
    Verifica que la classe `PermissionSession` gestiona correctament
    les operacions `allow_session` en un entorn concurrent amb múltiples fils.
    """
    s = PermissionSession()
    def worker():
        for i in range(100):
            s.allow_session(f"cmd-{i}")
            assert s.is_allowed(f"cmd-{i}")
    
    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert s.is_allowed("cmd-0")
