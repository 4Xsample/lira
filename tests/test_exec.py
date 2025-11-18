"""
Mòdul de proves unitàries per a la classe `Executor` del mòdul `core.exec`.
Verifica la funcionalitat de l'executor de comandes, incloent la validació de la whitelist,
la gestió de permisos per sessió i la interacció amb l'usuari.
"""
import pytest
from core.perm_session import PermissionSession
from core.exec import Executor, CommandCancelled, CommandRejected
import subprocess

def test_whitelist_rejects():
    """
    Verifica que l'Executor rebutja comandes que no estan a la whitelist.
    S'espera que es llanci una excepció `CommandRejected`.
    """
    perm = PermissionSession()
    exe = Executor([r'^echo\s+hello$'], perm)
    with pytest.raises(CommandRejected):
        exe.execute_with_permission(['rm', '-rf', '/tmp/something'])

def test_console_once(monkeypatch, tmp_path):
    """
    Verifica l'execució d'una comanda amb permís 'once' a través de la consola.
    Simula la interacció de l'usuari introduint '1'.
    """
    perm = PermissionSession()
    exe = Executor([r'^echo\s+hello$'], perm)
    monkeypatch.setattr('builtins.input', lambda prompt='': '1')
    rc, out, err = exe.execute_with_permission(['echo', 'hello'])
    assert rc == 0
    assert "hello" in out
    assert not perm.is_allowed("echo hello")

def test_console_session(monkeypatch):
    """
    Verifica l'execució d'una comanda amb permís 'session' a través de la consola.
    Simula la interacció de l'usuari introduint '2' i comprova que el permís es manté.
    """
    perm = PermissionSession()
    exe = Executor([r'^echo\s+hello$'], perm)
    monkeypatch.setattr('builtins.input', lambda prompt='': '2')
    rc, out, err = exe.execute_with_permission(['echo', 'hello'])
    assert rc == 0
    assert "hello" in out
    assert perm.is_allowed("echo hello")

    rc2, out2, err2 = exe.execute_with_permission(['echo', 'hello'])
    assert rc2 == 0
    assert "hello" in out2

def test_console_cancel(monkeypatch):
    """
    Verifica que l'Executor cancel·la una comanda si l'usuari ho indica per consola.
    Simula la interacció de l'usuari introduint '0'.
    """
    perm = PermissionSession()
    exe = Executor([r'^echo\s+hello$'], perm)
    monkeypatch.setattr('builtins.input', lambda prompt='': '0')
    with pytest.raises(CommandCancelled):
        exe.execute_with_permission(['echo', 'hello'])

def test_ui_payload_once():
    """
    Verifica l'execució d'una comanda amb permís 'once' a través d'un payload UI.
    """
    perm = PermissionSession()
    exe = Executor([r'^echo\s+hello$'], perm)
    rc, out, err = exe.execute_with_permission(['echo', 'hello'], ui_decision_payload={"decision": "once"})
    assert rc == 0
    assert "hello" in out
    assert not perm.is_allowed("echo hello")

def test_ui_payload_session():
    """
    Verifica l'execució d'una comanda amb permís 'session' a través d'un payload UI.
    Comprova que el permís es guarda per a la sessió.
    """
    perm = PermissionSession()
    exe = Executor([r'^echo\s+hello$'], perm)
    rc, out, err = exe.execute_with_permission(['echo', 'hello'], ui_decision_payload={"decision": "session"})
    assert rc == 0
    assert "hello" in out
    assert perm.is_allowed("echo hello")

    rc2, out2, err2 = exe.execute_with_permission(['echo', 'hello'])
    assert rc2 == 0
    assert "hello" in out2

def test_ui_payload_cancel():
    """
    Verifica que l'Executor cancel·la una comanda si el payload UI ho indica.
    """
    perm = PermissionSession()
    exe = Executor([r'^echo\s+hello$'], perm)
    with pytest.raises(CommandCancelled):
        exe.execute_with_permission(['echo', 'hello'], ui_decision_payload={"decision": "cancel"})

def test_command_timeout():
    """
    Verifica que l'Executor gestiona correctament el timeout d'una comanda.
    """
    perm = PermissionSession()
    exe = Executor([r'^sleep\s+\d+$'], perm, timeout=1)
    rc, out, err = exe.execute_with_permission(['sleep', '5'], ui_decision_payload={"decision": "once"})
    assert rc == -1
    assert "Timeout" in err

