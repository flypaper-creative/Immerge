#!/bin/bash
# Quick start script for Immerge

echo "========================================="
echo "Immerge Quick Start"
echo "========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY before running Immerge"
    echo ""
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create test images if no directory specified
if [ -z "$1" ]; then
    echo ""
    echo "Creating test images for demonstration..."
    python3 setup_example.py -n 8
    
    echo ""
    echo "========================================="
    echo "Ready to run Immerge!"
    echo "========================================="
    echo ""
    echo "To run with test images:"
    echo "  python3 immerge.py test_images --max-iterations 3 --delay 5"
    echo ""
    echo "To run with your own images:"
    echo "  python3 immerge.py /path/to/your/images"
    echo ""
else
    echo ""
    echo "========================================="
    echo "Ready to run Immerge!"
    echo "========================================="
    echo ""
    echo "To run:"
    echo "  python3 immerge.py $1"
    echo ""
fi
