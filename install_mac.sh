#!/bin/bash
#
# Rapor Scanner - Installation Script for macOS
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/emRival/rapor-scanner/main/install_mac.sh | bash
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║      📊 Rapor Scanner - macOS Installation         ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"

APP_DIR="$HOME/rapor-scanner"
REPO_URL="https://github.com/emRival/rapor-scanner.git"

# Check Homebrew
echo -e "${YELLOW}📋 Step 1/5: Checking Homebrew...${NC}"
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew already installed"
fi

# Install dependencies
echo -e "${YELLOW}📋 Step 2/5: Installing dependencies...${NC}"
brew install python poppler git 2>/dev/null || true

# Clone repository
echo -e "${YELLOW}📋 Step 3/5: Cloning repository...${NC}"
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR"
    git pull origin main
else
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

# Create virtual environment
echo -e "${YELLOW}📋 Step 4/5: Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Create run script
echo -e "${YELLOW}📋 Step 5/5: Creating run script...${NC}"
cat > "$APP_DIR/run.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
streamlit run app.py --server.port 8501
EOF
chmod +x "$APP_DIR/run.sh"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║      ✅ Installation Complete!                    ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📁 Location: $APP_DIR${NC}"
echo ""
echo -e "${BLUE}🚀 To Run:${NC}"
echo "   cd $APP_DIR && ./run.sh"
echo ""
echo -e "${BLUE}📍 Access: http://localhost:8501${NC}"
echo ""
