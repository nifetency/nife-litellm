@echo off
REM LiteLLM Docker Application - Build and Run Script for Windows

echo ========================================
echo LiteLLM Docker Application
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    exit /b 1
)

echo [1] Build Docker Image
echo [2] Run with OpenAI (GPT-3.5-turbo)
echo [3] Run with Anthropic (Claude)
echo [4] Run with Google (Gemini)
echo [5] Run Docker Compose
echo [6] View Docker Images
echo [7] Exit
echo.

set /p choice="Enter your choice [1-7]: "

if "%choice%"=="1" (
    echo.
    echo Building Docker image...
    docker build -t litellm-app:latest .
    echo Build complete!
    goto end
)

if "%choice%"=="2" (
    echo.
    set /p api_key="Enter your OpenAI API Key: "
    set /p prompts="Enter your prompt(s): "
    echo Running with OpenAI...
    docker run --rm ^
      -e MODEL_ID=gpt-3.5-turbo ^
      -e API_KEY=%api_key% ^
      -e PROMPTS=%prompts% ^
      -e VERBOSE=true ^
      litellm-app:latest
    goto end
)

if "%choice%"=="3" (
    echo.
    set /p api_key="Enter your Anthropic API Key: "
    set /p prompts="Enter your prompt(s): "
    echo Running with Anthropic Claude...
    docker run --rm ^
      -e MODEL_ID=claude-3-sonnet-20240229 ^
      -e API_KEY=%api_key% ^
      -e PROMPTS=%prompts% ^
      -e VERBOSE=true ^
      litellm-app:latest
    goto end
)

if "%choice%"=="4" (
    echo.
    set /p api_key="Enter your Google API Key: "
    set /p prompts="Enter your prompt(s): "
    echo Running with Google Gemini...
    docker run --rm ^
      -e MODEL_ID=gemini-pro ^
      -e API_KEY=%api_key% ^
      -e PROMPTS=%prompts% ^
      -e VERBOSE=true ^
      litellm-app:latest
    goto end
)

if "%choice%"=="5" (
    echo.
    echo Checking for .env file...
    if not exist .env (
        echo .env file not found!
        echo Creating .env from .env.example...
        copy .env.example .env
        echo Please edit .env with your API key and try again
        exit /b 1
    )
    echo Starting Docker Compose...
    docker-compose up --build
    goto end
)

if "%choice%"=="6" (
    echo.
    docker images
    goto end
)

if "%choice%"=="7" (
    exit /b 0
)

echo Invalid choice. Please try again.

:end
echo.
pause
