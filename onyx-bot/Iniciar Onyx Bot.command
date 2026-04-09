#!/bin/bash
cd "$(dirname "$0")"

# Matar TODAS las instancias anteriores y esperar que mueran
pkill -9 -f "python3 bot.py" 2>/dev/null
pkill -9 -f "Python bot.py" 2>/dev/null
sleep 2

# Verificar que no quede ninguna
if pgrep -f "bot.py" > /dev/null; then
    osascript -e 'display notification "No se pudo cerrar instancia anterior. Reiniciá manualmente." with title "Onyx Error"'
    exit 1
fi

# Instalar dependencias si faltan
pip3 install -r requirements.txt -q

# Cargar variables de entorno
set -a
source .env
set +a

# Arrancar bot en background, logs en bot.log
nohup python3 bot.py > bot.log 2>&1 &
disown

sleep 2

# Verificar que arrancó
if pgrep -f "bot.py" > /dev/null; then
    osascript -e 'display notification "Onyx Bot iniciado 🤖" with title "Onyx"'
else
    osascript -e 'display notification "Error al iniciar el bot. Revisá bot.log" with title "Onyx Error"'
fi
