#!/bin/bash

# Ruta fixa a la instal·lació de LIRA. Això és més robust que calcular rutes relatives.
LIRA_INSTALL_DIR="$HOME/.lira"

# Definim les rutes dels fitxers necessaris a partir de la ruta d'instal·lació
VENV_PATH="$LIRA_INSTALL_DIR/.venv"
TUI_SCRIPT="$LIRA_INSTALL_DIR/core/tui.py"

# Comprova si l'entorn virtual existeix
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Error: L'entorn virtual no s'ha trobat a $VENV_PATH."
    echo "Assegura't d'haver executat l'script d'instal·lació (./scripts/install.sh) correctament."
    exit 1
fi

# Comprova si el script de la TUI existeix
if [ ! -f "$TUI_SCRIPT" ]; then
    echo "❌ Error: El script de la TUI no s'ha trobat a $TUI_SCRIPT."
    exit 1
fi

# Activa l'entorn virtual, executa l'aplicació i desactiva el venv en sortir
echo "🚀 Iniciant la TUI de LIRA..."
source "$VENV_PATH/bin/activate"
python "$TUI_SCRIPT" "$@"
deactivate
