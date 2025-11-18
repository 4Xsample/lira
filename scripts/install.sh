#!/bin/bash
set -e

# --- Configuració de Logs ---
LOGFILE="/tmp/lira_install_$(date +%s).log"
exec > >(tee -a "$LOGFILE") 2>&1
echo "Inici de la instal·lació de LIRA - Log complet a $LOGFILE"

# --- Determinar directori de l'script ---
# Això assegura que totes les rutes són relatives a la ubicació de l'script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIRA_SOURCE_DIR="$(dirname "$SCRIPT_DIR")"

# --- Directori d'instal·lació ---
INSTALL_DIR="$HOME/.lira"

echo "Directori d'origen de LIRA: $LIRA_SOURCE_DIR"
echo "Directori d'instal·lació: $INSTALL_DIR"

# --- Mode silenciós / Interacció amb l'usuari ---
if [ "$1" = "--yes" ]; then
    REPLY="y"
    echo "Executant en mode silenciós (--yes). S'acceptaran totes les preguntes."
else
    REPLY=""
fi

# --- Comprovar i gestionar instal·lació existent ---
if [ -d "$INSTALL_DIR" ]; then
    if [ -z "$REPLY" ]; then
        read -p "Ja existeix una instal·lació a $INSTALL_DIR. Vols sobreescriure-la? (y/n): " REPLY
    fi

    if [[ "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Eliminant instal·lació anterior..."
        # Aturar i desactivar el servei abans d'esborrar els fitxers
        sudo systemctl stop lira.service || echo "No s'ha pogut aturar el servei (potser no estava en marxa)."
        sudo systemctl disable lira.service || echo "No s'ha pogut desactivar el servei."
        rm -rf "$INSTALL_DIR"
        echo "Instal·lació anterior eliminada."
    else
        echo "Cancel·lant instal·lació."
        exit 1
    fi
fi

# --- Instal·lació ---
echo "Creant directori d'instal·lació..."
mkdir -p "$INSTALL_DIR"

echo "Copiant fitxers de LIRA..."
# Copia tot el contingut de la carpeta font a la destinació
cp -r "$LIRA_SOURCE_DIR"/* "$INSTALL_DIR"/
echo "Fitxers copiats correctament."

# --- Configuració de l'entorn virtual i dependències (ABANS del servei) ---
echo "✅ Creant l'entorn virtual i instal·lant les dependències de LIRA..."
# Naveguem al directori d'instal·lació per crear el venv allí
cd "$INSTALL_DIR" || exit 1
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
echo "✅ Entorn virtual i dependències instal·lades correctament."

# --- Configuració del servei systemd (DESPRÉS del venv) ---
echo "Configurant el servei systemd..."
SERVICE_PATH="/etc/systemd/system/lira.service"

# Creació del fitxer de servei amb sudo
sudo bash -c "cat > $SERVICE_PATH" <<EOL
[Unit]
Description=LIRA Orchestrator Service
After=network.target

[Service]
ExecStart=$INSTALL_DIR/.venv/bin/python $INSTALL_DIR/core/lira_api.py
WorkingDirectory=$INSTALL_DIR
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOL
echo "Fitxer de servei creat a $SERVICE_PATH."

# --- Activació del servei ---
echo "Recarregant, activant i iniciant el servei LIRA..."
sudo systemctl daemon-reload
sudo systemctl enable lira.service
sudo systemctl start lira.service

echo "Servei LIRA iniciat."

# --- Crear enllaç a la TUI ---
echo "✅ Creant un enllaç a l'executable 'lira-tui'..."
# L'enllaç es crearà a /usr/local/bin, que normalment ja és al PATH de l'usuari
sudo ln -sf "$INSTALL_DIR/scripts/lira-tui.sh" /usr/local/bin/lira-tui
echo "✅ Pots executar la TUI des de qualsevol lloc amb la comanda: lira-tui"

echo "✅ Instal·lació completada! LIRA ja està activa."
echo "Pots comprovar l'estat amb: sudo systemctl status lira.service"