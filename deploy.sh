#!/bin/bash
# Quick deployment script for nife-llmlite

set -e

echo "🚀 nife-llmlite - Quick Deploy"
echo "=============================="
echo ""

# Step 1: Cleanup
if [ -f "cleanup.sh" ]; then
    echo "📋 Step 1: Cleanup old files"
    chmod +x cleanup.sh
    ./cleanup.sh
else
    echo "✓ Already clean"
fi

echo ""
echo "📦 Step 2: Build Docker image"
docker-compose build

echo ""
echo "🏃 Step 3: Start API"
docker-compose up -d

echo ""
echo "⏳ Waiting for API to be ready..."
sleep 5

echo ""
echo "🧪 Step 4: Run tests"
chmod +x test.sh
./test.sh

echo ""
echo "=============================="
echo "✅ Deployment Complete!"
echo "=============================="
echo ""
echo "API is running at: http://localhost:8080"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f    # View logs"
echo "  docker-compose ps         # Check status"
echo "  docker-compose down       # Stop API"
echo "  ./test.sh                 # Run tests"
echo ""
