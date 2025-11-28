# Quick Start Guide - LiteLLM Docker Application

## 30-Second Setup

### Step 1: Navigate to Project Directory
```bash
cd C:\Users\Varun S\Desktop\LiteLLM\litellm-docker-app
```

### Step 2: Build Docker Image
```bash
docker build -t litellm-app:latest .
```

### Step 3: Run Container
Replace `YOUR_API_KEY` and `YOUR_PROMPT` with your actual values:

**For OpenAI:**
```bash
docker run --rm `
  -e MODEL_ID=gpt-3.5-turbo `
  -e API_KEY=YOUR_API_KEY `
  -e PROMPTS="YOUR_PROMPT" `
  litellm-app:latest
```

**For Anthropic Claude:**
```bash
docker run --rm `
  -e MODEL_ID=claude-3-sonnet-20240229 `
  -e API_KEY=YOUR_API_KEY `
  -e PROMPTS="YOUR_PROMPT" `
  litellm-app:latest
```

## Using the Interactive Scripts

### Option A: Windows Command Prompt
```bash
run.bat
```

### Option B: PowerShell
```powershell
.\run.ps1
```

## Real-World Examples

### Example 1: Single Prompt with OpenAI
```bash
docker run --rm `
  -e MODEL_ID=gpt-3.5-turbo `
  -e API_KEY=sk-your-actual-key `
  -e PROMPTS="What is artificial intelligence?" `
  litellm-app:latest
```

### Example 2: Multiple Prompts (Pipe-Separated)
```bash
docker run --rm `
  -e MODEL_ID=gpt-3.5-turbo `
  -e API_KEY=sk-your-actual-key `
  -e PROMPTS="What is AI? | Explain Machine Learning | Tell me about Python" `
  litellm-app:latest
```

### Example 3: Multiple Prompts (JSON Array)
```bash
docker run --rm `
  -e MODEL_ID=gpt-3.5-turbo `
  -e API_KEY=sk-your-actual-key `
  -e PROMPTS='["What is cloud computing?", "Explain microservices", "What is DevOps?"]' `
  litellm-app:latest
```

### Example 4: Using .env File with Docker Compose
1. Edit `.env.example` with your credentials
2. Save as `.env`
3. Run:
```bash
docker-compose up --build
```

## Output Example

```
================================================================================
LiteLLM Docker Application Results
================================================================================
Timestamp: 2024-01-15T10:30:45.123456
Model: gpt-3.5-turbo

Summary:
  Total Prompts: 2
  Successful: 2
  Failed: 0

Detailed Results:
--------------------------------------------------------------------------------

Prompt 1:
  Input: What is artificial intelligence?
  Response: Artificial Intelligence (AI) is the simulation of human intelligence...

Prompt 2:
  Input: Explain Machine Learning
  Response: Machine Learning is a subset of AI that enables systems to learn...

================================================================================
Raw JSON Output:
================================================================================
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "model": "gpt-3.5-turbo",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "What is artificial intelligence?",
      "response": "Artificial Intelligence (AI) is...",
      "status": "success"
    },
    {
      "prompt_id": 2,
      "prompt": "Explain Machine Learning",
      "response": "Machine Learning is a subset...",
      "status": "success"
    }
  ],
  "summary": {
    "total_prompts": 2,
    "successful": 2,
    "failed": 0
  }
}
```

## Troubleshooting

### Problem: "Docker command not found"
**Solution:** Install Docker Desktop from https://www.docker.com/products/docker-desktop

### Problem: "Missing required environment variables"
**Solution:** Ensure you're setting MODEL_ID, API_KEY, and PROMPTS:
```bash
docker run --rm -e MODEL_ID="..." -e API_KEY="..." -e PROMPTS="..." litellm-app:latest
```

### Problem: "Invalid API Key"
**Solution:** Double-check your API key is correct:
- For OpenAI: Starts with `sk-`
- For Anthropic: Starts with `sk-ant-`
- For Google: Usually a long string

### Problem: Build fails
**Solution:** 
1. Ensure internet connection is active
2. Ensure Docker daemon is running
3. Try: `docker builder prune` to clear cache

## Next Steps

1. **Explore Advanced Features**: Check `README.md` for advanced configurations
2. **Customize**: Edit `app.py` to add custom parameters or models
3. **Production Ready**: See README.md section on production deployment
4. **Error Handling**: The app gracefully handles errors and returns appropriate exit codes

## Supported Models

- **OpenAI**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Anthropic**: `claude-3-opus`, `claude-3-sonnet-20240229`, `claude-3-haiku`
- **Google**: `gemini-pro`, `gemini-1.5-pro`
- **Cohere**: `command`, `command-light`
- **And 50+ more via LiteLLM!**

## File Structure

```
litellm-docker-app/
├── app.py                 # Main application logic
├── requirements.txt       # Dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Environment template
├── run.bat              # Windows batch script
├── run.ps1              # PowerShell script
├── README.md            # Full documentation
└── QUICKSTART.md        # This file
```

## Additional Resources

- LiteLLM Docs: https://docs.litellm.ai/
- Docker Docs: https://docs.docker.com/
- Supported Models: https://docs.litellm.ai/docs/providers


