#!/bin/bash
# CUSTOMER SUPPORT CHATBOT - STARTUP SCRIPT (Linux/Mac)

set -e

echo "=================================="
echo "CUSTOMER SUPPORT CHATBOT - STARTUP"
echo "=================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "X Python 3 not found"
    exit 1
fi

echo "OK $(python3 --version)"
echo ""

# Check .env
if [ ! -f ".env" ]; then
    echo "! No .env file"
    if [ -f ".env.template" ]; then
        cp .env.template .env
        echo "OK Created .env (edit if PDF filename is different)"
        echo ""
    fi
fi

# Check PDF
PDF_FILE=$(grep "^FILE_PATH=" .env | cut -d'=' -f2 | xargs)
if [ -z "$PDF_FILE" ]; then
    PDF_FILE="Egyptian_ERP_System_Comprehensive_Manual.pdf"
fi

echo "Checking PDF: $PDF_FILE"
if [ ! -f "$PDF_FILE" ]; then
    echo "X PDF NOT FOUND: $PDF_FILE"
    echo "Please ensure the PDF exists in this folder"
    exit 1
fi
echo "OK PDF found"
echo ""

# Virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "OK venv created"
    echo ""
fi

source venv/bin/activate

# Install
echo "Installing packages..."
pip install -q -r requirements.txt
echo "OK Dependencies ready"
echo ""

# Start
echo "=================================="
echo "Starting HR Chatbot API"
echo "=================================="
echo "Server: http://localhost:5000"
echo "Test:   python test_api.py"
echo "Press Ctrl+C to stop"
echo "=================================="
echo ""

python3 main_app.py
