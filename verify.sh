#!/bin/bash
# Verification script - confirms API-only mode is properly set up

set -e

echo "================================================"
echo "nife-llmlite - API-Only Verification"
echo "================================================"
echo ""

cd "$(dirname "$0")"

echo "🔍 Checking files..."
echo ""

# Check required files exist
echo "✅ Required files:"
required_files=("app.py" "Dockerfile" "docker-compose.yml" "requirements.txt" "test.sh" "README.md" ".gitignore")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING!)"
        exit 1
    fi
done

echo ""
echo "🗑️  Files that should be removed:"
unwanted_files=("api_app.py" "entrypoint.sh" "run.bat" "run.ps1" "test_api.sh")
unwanted_found=0
for file in "${unwanted_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ⚠️  $file (still exists - run cleanup.sh)"
        unwanted_found=1
    else
        echo "  ✓ $file (removed)"
    fi
done

echo ""
echo "📝 Checking app.py..."
if grep -q "RUN_MODE" app.py 2>/dev/null; then
    echo "  ✗ app.py still contains batch mode logic (RUN_MODE)"
    exit 1
else
    echo "  ✓ app.py is API-only"
fi

if grep -q "entrypoint.sh" Dockerfile 2>/dev/null; then
    echo "  ✗ Dockerfile references entrypoint.sh"
    exit 1
else
    echo "  ✓ Dockerfile uses direct gunicorn CMD"
fi

echo ""
echo "📦 Checking requirements.txt..."
req_count=$(cat requirements.txt | grep -v '^#' | grep -v '^$' | wc -l)
if [ "$req_count" -le 5 ]; then
    echo "  ✓ Minimal dependencies ($req_count packages)"
else
    echo "  ⚠️  More than 5 dependencies ($req_count packages)"
fi

echo ""
echo "================================================"
if [ $unwanted_found -eq 0 ]; then
    echo "✅ API-ONLY MODE VERIFIED!"
    echo "================================================"
    echo ""
    echo "Your project is clean and ready for production."
    echo ""
    echo "Next steps:"
    echo "  1. docker-compose build"
    echo "  2. docker-compose up -d"
    echo "  3. ./test.sh"
else
    echo "⚠️  CLEANUP NEEDED!"
    echo "================================================"
    echo ""
    echo "Run: ./cleanup.sh"
    echo ""
    echo "This will remove unnecessary batch mode files."
fi
echo ""
