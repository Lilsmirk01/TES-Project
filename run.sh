#!/usr/bin/env bash
set -e
# Activate venv if present
if [ -f .venv/bin/activate ]; then
  . .venv/bin/activate
fi
# Start Streamlit
streamlit run app.py --server.headless true
