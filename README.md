@echo off
cd /d "C:\Coding shi\remote"
start "http_server" python -m http.server 8080 --bind 0.0.0.0
python server.py