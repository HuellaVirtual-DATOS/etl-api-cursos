#!/bin/bash

# Activar entorno virtual (opcional)
# python3 -m venv venv
# source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar script principal
python cargar_api_en_supabase.py

