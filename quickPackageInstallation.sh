#!/bin/bash

set -e

sudo apt install -y \
    git \
    curl \
    gnupg \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates

echo "Installing Node.js via NVM..."

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

nvm install 18.18.0
nvm use 18.18.0

echo "Creating Python virtual environment..."

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip
pip install numpy pandas scikit-learn flask pymongo

echo "Updating package lists..."
sudo apt update


echo "Installing base packages..."

echo "Installing Redis..."

sudo apt install -y redis-server

sudo systemctl enable redis-server
sudo systemctl start redis-server

echo
echo "=================================="
echo "Installation Complete"
echo "=================================="
echo

echo "Node:"
node --version

echo
echo "Python:"
python3 --version

echo
echo "MongoDB Shell:"
mongosh --version

echo
echo "Redis:"
redis-cli ping

echo
echo "Git:"
git --version

echo
echo "Python virtual environment:"
echo "source venv/bin/activate"