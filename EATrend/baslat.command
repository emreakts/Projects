#!/bin/bash
# Mac'te çift tıkla: stüdyoyu başlatır ve tarayıcıda açar.
cd "$(dirname "$0")"
[ -d node_modules ] || npm install
(sleep 1.5; open http://localhost:3000) &
node server.js
