#!/bin/bash
# Test script for nife-llmlite API

set -e

API_URL="${API_URL:-http://localhost:8080}"

echo "=========================================="
echo "Testing nife-llmlite API"
echo "=========================================="

# Test 1: Health Check
echo -e "\n[1/4] Testing health endpoint..."
response=$(curl -s -w "\n%{http_code}" $API_URL/health)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Health check passed"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    echo "❌ Health check failed (HTTP $http_code)"
    exit 1
fi

# Test 2: Root Info
echo -e "\n[2/4] Testing root endpoint..."
response=$(curl -s -w "\n%{http_code}" $API_URL/)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Root endpoint passed"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    echo "❌ Root endpoint failed (HTTP $http_code)"
    exit 1
fi

# Test 3: Models List
echo -e "\n[3/4] Testing models endpoint..."
response=$(curl -s -w "\n%{http_code}" $API_URL/api/models)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Models endpoint passed"
    echo "$body" | jq '.providers | keys' 2>/dev/null || echo "$body"
else
    echo "❌ Models endpoint failed (HTTP $http_code)"
    exit 1
fi

# Test 4: Completion (if API key provided)
echo -e "\n[4/4] Testing completion endpoint..."
if [ -n "$OPENAI_API_KEY" ]; then
    response=$(curl -s -w "\n%{http_code}" -X POST $API_URL/api/completion \
      -H "Content-Type: application/json" \
      -d '{
        "model_id": "gpt-3.5-turbo",
        "api_key": "'"$OPENAI_API_KEY"'",
        "prompts": ["Say hello"],
        "max_tokens": 50
      }')
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "207" ]; then
        echo "✅ Completion endpoint passed"
        echo "$body" | jq '.summary' 2>/dev/null || echo "$body"
    else
        echo "❌ Completion endpoint failed (HTTP $http_code)"
        echo "$body"
        exit 1
    fi
else
    echo "⚠️  Skipping completion test (OPENAI_API_KEY not set)"
fi

echo -e "\n=========================================="
echo "✅ All tests passed!"
echo "=========================================="
