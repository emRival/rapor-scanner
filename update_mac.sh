#!/bin/bash
#
# Rapor Scanner - Update Script for macOS
# Usage: ./update.sh
#

APP_DIR="$HOME/rapor-scanner"

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║      📊 Rapor Scanner - Update                     ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

cd "$APP_DIR" || { echo "❌ Directory not found: $APP_DIR"; exit 1; }

echo "📥 Pulling from GitHub..."
git pull origin main

echo "📦 Updating dependencies..."
source venv/bin/activate
pip install -r requirements.txt -q

echo ""
echo "✅ Update complete!"
echo ""
echo "🚀 To run: cd $APP_DIR && ./run.sh"
echo ""
