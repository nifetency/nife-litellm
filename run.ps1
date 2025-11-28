# LiteLLM Docker Application - PowerShell Build and Run Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LiteLLM Docker Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    docker --version | Out-Null
} catch {
    Write-Host "ERROR: Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

# Menu
Write-Host "[1] Build Docker Image" -ForegroundColor Green
Write-Host "[2] Run with OpenAI (GPT-3.5-turbo)" -ForegroundColor Green
Write-Host "[3] Run with Anthropic (Claude)" -ForegroundColor Green
Write-Host "[4] Run with Google (Gemini)" -ForegroundColor Green
Write-Host "[5] Run Docker Compose" -ForegroundColor Green
Write-Host "[6] View Docker Images" -ForegroundColor Green
Write-Host "[7] Exit" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "Enter your choice [1-7]"

switch ($choice) {
    "1" {
        Write-Host "Building Docker image..." -ForegroundColor Yellow
        docker build -t litellm-app:latest .
        Write-Host "Build complete!" -ForegroundColor Green
    }
    "2" {
        $api_key = Read-Host "Enter your OpenAI API Key"
        $prompts = Read-Host "Enter your prompt(s)"
        Write-Host "Running with OpenAI..." -ForegroundColor Yellow
        docker run --rm `
          -e MODEL_ID=gpt-3.5-turbo `
          -e API_KEY=$api_key `
          -e PROMPTS=$prompts `
          -e VERBOSE=true `
          litellm-app:latest
    }
    "3" {
        $api_key = Read-Host "Enter your Anthropic API Key"
        $prompts = Read-Host "Enter your prompt(s)"
        Write-Host "Running with Anthropic Claude..." -ForegroundColor Yellow
        docker run --rm `
          -e MODEL_ID=claude-3-sonnet-20240229 `
          -e API_KEY=$api_key `
          -e PROMPTS=$prompts `
          -e VERBOSE=true `
          litellm-app:latest
    }
    "4" {
        $api_key = Read-Host "Enter your Google API Key"
        $prompts = Read-Host "Enter your prompt(s)"
        Write-Host "Running with Google Gemini..." -ForegroundColor Yellow
        docker run --rm `
          -e MODEL_ID=gemini-pro `
          -e API_KEY=$api_key `
          -e PROMPTS=$prompts `
          -e VERBOSE=true `
          litellm-app:latest
    }
    "5" {
        if (!(Test-Path ".env")) {
            Write-Host ".env file not found!" -ForegroundColor Red
            Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
            Copy-Item ".env.example" ".env"
            Write-Host "Please edit .env with your API key and try again" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "Starting Docker Compose..." -ForegroundColor Yellow
        docker-compose up --build
    }
    "6" {
        Write-Host "Docker Images:" -ForegroundColor Yellow
        docker images
    }
    "7" {
        exit 0
    }
    default {
        Write-Host "Invalid choice. Please try again." -ForegroundColor Red
    }
}

Write-Host ""
Read-Host "Press Enter to exit"
