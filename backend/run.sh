#!/bin/bash
# Contract Analyzer Backend - Quick Start Script (Unix/Linux/Mac)

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Contract Analyzer - Backend Setup & Run                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "▶ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "▶ Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "▶ Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "▶ Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Download spaCy model
echo ""
echo "▶ Downloading spaCy English model..."
python -m spacy download -q en_core_web_sm
echo "✓ spaCy model downloaded"

# Create directories
echo ""
echo "▶ Creating necessary directories..."
mkdir -p uploads
echo "✓ Directories created"

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo ""
    echo "▶ Creating .env from template..."
    cp .env.example .env
    echo "✓ .env created (review and update if needed)"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Setup Complete! ✓                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next: Start the backend with:"
echo "  python -m app.main"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
