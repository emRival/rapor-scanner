#!/bin/bash
#
# Rapor Scanner - One-Click Installation Script
# For Ubuntu/Debian (LXC, VPS, Server)
#
# Usage:
#   Sebagai root:
#     curl -sSL https://raw.githubusercontent.com/emRival/rapor-scanner/main/install.sh | bash
#
#   Sebagai user biasa:
#     curl -sSL https://raw.githubusercontent.com/emRival/rapor-scanner/main/install.sh | sudo bash
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="rapor-scanner"
APP_DIR="/opt/$APP_NAME"
REPO_URL="https://github.com/emRival/rapor-scanner.git"
SERVICE_NAME="rapor-scanner"
SERVICE_PORT=8501

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║      📊 Rapor Scanner Installation Script         ║"
echo "║         For Ubuntu/Debian LXC/Server              ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ Script ini harus dijalankan sebagai root${NC}"
   echo "   Jalankan: sudo bash install.sh"
   exit 1
fi

echo -e "${YELLOW}📋 Step 1/6: Update system packages...${NC}"
apt update -qq
apt upgrade -y -qq

echo -e "${YELLOW}📋 Step 2/6: Install system dependencies...${NC}"
apt install -y -qq \
    python3 \
    python3-pip \
    python3-venv \
    git \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    curl \
    wget \
    || apt install -y -qq \
    python3 \
    python3-pip \
    python3-venv \
    git \
    poppler-utils \
    curl \
    wget

echo -e "${YELLOW}📋 Step 3/6: Create application directory...${NC}"
mkdir -p $APP_DIR
cd $APP_DIR

# Clone or pull repository
if [ -d ".git" ]; then
    echo -e "${BLUE}   Updating existing installation...${NC}"
    git pull origin main
else
    echo -e "${BLUE}   Cloning repository...${NC}"
    git clone $REPO_URL .
fi

echo -e "${YELLOW}📋 Step 4/6: Create Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${YELLOW}📋 Step 5/6: Install Python dependencies...${NC}"
echo -e "${BLUE}   (Ini mungkin memakan waktu 5-15 menit untuk download ~1GB packages)${NC}"
pip install --upgrade pip
pip install -r requirements.txt --progress-bar on

echo -e "${YELLOW}📋 Step 6/6: Create systemd service...${NC}"
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Rapor Scanner - Rekap Nilai Rapor K13
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$APP_DIR/venv/bin/streamlit run app.py --server.port $SERVICE_PORT --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload and enable service
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

# Install CLI tool
echo -e "${YELLOW}📋 Installing CLI tool...${NC}"
cp $APP_DIR/rapor-scanner /usr/local/bin/rapor-scanner
chmod +x /usr/local/bin/rapor-scanner

# Create MOTD
cat > /etc/update-motd.d/99-rapor-scanner << 'MOTD'
#!/bin/bash
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      📊 Rapor Scanner                             ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"
if systemctl is-active --quiet rapor-scanner; then
    echo -e "   Status: ${GREEN}● Running${NC}"
else
    echo -e "   Status: ${RED}● Stopped${NC}"
fi
IP=$(hostname -I | awk '{print $1}')
echo -e "   URL:    http://$IP:8501"
echo -e "   CLI:    rapor-scanner [status|start|stop|restart|logs|update]"
echo ""
MOTD
chmod +x /etc/update-motd.d/99-rapor-scanner

# Get IP address
IP=$(hostname -I | awk '{print $1}')

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║      ✅ Installation Complete!                    ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📍 Access URL:${NC}"
echo -e "   Local:   http://localhost:$SERVICE_PORT"
echo -e "   Network: http://$IP:$SERVICE_PORT"
echo ""
echo -e "${BLUE}🔧 CLI Commands:${NC}"
echo -e "   rapor-scanner status   - Show status"
echo -e "   rapor-scanner start    - Start service"
echo -e "   rapor-scanner stop     - Stop service"
echo -e "   rapor-scanner restart  - Restart service"
echo -e "   rapor-scanner logs     - View logs"
echo -e "   rapor-scanner update   - Update from GitHub"
echo ""
echo -e "${BLUE}📁 Directory: $APP_DIR${NC}"
echo ""

# Run MOTD to show status
run-parts /etc/update-motd.d/ 2>/dev/null || bash /etc/update-motd.d/99-rapor-scanner
