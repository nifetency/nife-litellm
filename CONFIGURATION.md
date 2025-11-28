# Configuration Guide - LiteLLM Docker Application

## Complete Configuration Reference

### Environment Variables

#### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MODEL_ID` | The LLM model to use | `gpt-3.5-turbo` |
| `API_KEY` | API key for the provider | `sk-your-key-here` |
| `PROMPTS` | Prompts to process | `"What is AI?"` |

#### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `VERBOSE` | Enable detailed logging | `false` | `true` |

---

## Model Configuration

### OpenAI Models
```bash
# GPT-3.5 Turbo (Fast, Cheap)
MODEL_ID=gpt-3.5-turbo

# GPT-4 (Most Capable)
MODEL_ID=gpt-4

# GPT-4 Turbo (Better + Faster)
MODEL_ID=gpt-4-turbo
```

**Setup:**
1. Get API key from https://platform.openai.com/api-keys
2. Set: `API_KEY=sk-your-key`

---

### Anthropic Claude Models
```bash
# Claude 3 Opus (Most Capable)
MODEL_ID=claude-3-opus-20240229

# Claude 3 Sonnet (Balanced)
MODEL_ID=claude-3-sonnet-20240229

# Claude 3 Haiku (Fast, Compact)
MODEL_ID=claude-3-haiku-20240307
```

**Setup:**
1. Get API key from https://console.anthropic.com/
2. Set: `API_KEY=sk-ant-your-key`

---

### Google Gemini Models
```bash
# Gemini Pro (General Purpose)
MODEL_ID=gemini-pro

# Gemini 1.5 Pro (Advanced)
MODEL_ID=gemini-1.5-pro

# Gemini 1.5 Flash (Fast)
MODEL_ID=gemini-1.5-flash
```

**Setup:**
1. Get API key from https://makersuite.google.com/app/apikey
2. Set: `API_KEY=your-google-api-key`

---

### Cohere Models
```bash
# Command (Versatile)
MODEL_ID=command

# Command Light (Faster)
MODEL_ID=command-light
```

**Setup:**
1. Get API key from https://dashboard.cohere.ai/
2. Set: `API_KEY=your-cohere-api-key`

---

## Prompt Configuration

### Format 1: Single Prompt
```bash
PROMPTS="What is machine learning?"
```

### Format 2: Pipe-Separated Multiple Prompts
```bash
PROMPTS="Question 1 | Question 2 | Question 3"
```

### Format 3: JSON Array Multiple Prompts
```bash
PROMPTS='["Question 1", "Question 2", "Question 3"]'
```

### Format 4: Using Special Characters
```bash
# Escape quotes properly
PROMPTS='["What\'s AI?", "Can Docker scale?"]'
```

---

## Docker Configuration Examples

### Minimal Configuration
```bash
docker run --rm \
  -e MODEL_ID=gpt-3.5-turbo \
  -e API_KEY=sk-key \
  -e PROMPTS="Hello" \
  litellm-app:latest
```

### Full Configuration with All Options
```bash
docker run --rm \
  -e MODEL_ID=gpt-3.5-turbo \
  -e API_KEY=sk-key \
  -e PROMPTS="What is AI? | Explain Python" \
  -e VERBOSE=true \
  --name litellm-container \
  --memory=2g \
  --cpus=2 \
  litellm-app:latest
```

### With Volume Mounting for Logs
```bash
docker run --rm \
  -e MODEL_ID=gpt-3.5-turbo \
  -e API_KEY=sk-key \
  -e PROMPTS="Test" \
  -v C:\logs:/app/logs \
  litellm-app:latest
```

---

## Docker Compose Configuration

### Basic docker-compose.yml
```yaml
version: '3.8'

services:
  litellm-app:
    build: .
    environment:
      - MODEL_ID=gpt-3.5-turbo
      - API_KEY=your-key
      - PROMPTS=["Q1", "Q2"]
```

### With .env File
```yaml
version: '3.8'

services:
  litellm-app:
    build: .
    env_file: .env
    networks:
      - litellm-net

networks:
  litellm-net:
    driver: bridge
```

---

## Environment Variable Security

### Best Practices

1. **Never Hardcode Keys**
   ```bash
   # ❌ BAD
   docker run -e API_KEY=sk-actual-key litellm-app

   # ✅ GOOD
   docker run --env-file .env litellm-app
   ```

2. **Use .env Files**
   ```bash
   # .env file (never commit to git)
   MODEL_ID=gpt-3.5-turbo
   API_KEY=sk-your-actual-key
   PROMPTS=["Question 1"]
   ```

3. **Use Docker Secrets (Production)**
   ```bash
   docker secret create api_key ./api_key.txt
   docker run --secret api_key litellm-app
   ```

4. **Use Environment Managers**
   - HashiCorp Vault
   - AWS Secrets Manager
   - Azure Key Vault

---

## Advanced Configuration

### Custom Model Parameters

To modify model parameters like temperature, edit `app.py`:

```python
# In app.py, find this line:
response = litellm.completion(
    model=model_id,
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,  # Adjust here
    max_tokens=500,    # Add here
    top_p=0.9,        # Add here
)
```

### Different API Endpoints

For custom LLM providers:

```bash
# Azure OpenAI
MODEL_ID=azure/your-deployment-name

# Replicate
MODEL_ID=replicate/llama-2-70b

# Ollama (Local)
MODEL_ID=ollama/neural-chat
```

---

## Debugging Configuration

### Enable Verbose Logging
```bash
docker run --rm \
  -e VERBOSE=true \
  -e MODEL_ID=gpt-3.5-turbo \
  -e API_KEY=sk-key \
  -e PROMPTS="Test" \
  litellm-app:latest
```

### Check Environment Variables Inside Container
```bash
docker run --rm \
  -e MODEL_ID=gpt-3.5-turbo \
  -e API_KEY=sk-key \
  litellm-app:latest \
  env
```

---

## Common Configurations

### Configuration 1: Simple Chat
```bash
MODEL_ID=gpt-3.5-turbo
API_KEY=sk-your-key
PROMPTS="What is Python?"
```

### Configuration 2: Batch Processing
```bash
MODEL_ID=gpt-3.5-turbo
API_KEY=sk-your-key
PROMPTS='["Question 1", "Question 2", "Question 3", "Question 4"]'
```

### Configuration 3: Budget-Conscious
```bash
MODEL_ID=gpt-3.5-turbo
API_KEY=sk-your-key
PROMPTS="Single important question"
```

### Configuration 4: High Quality
```bash
MODEL_ID=gpt-4
API_KEY=sk-your-key
PROMPTS="Complex reasoning problem"
```

### Configuration 5: Speed-Optimized
```bash
MODEL_ID=claude-3-haiku-20240307
API_KEY=sk-ant-your-key
PROMPTS="Quick classification task"
```

---

## Exit Codes Reference

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | All prompts processed |
| `1` | Failure | Missing vars or processing errors |

---

## Performance Tuning

### For Large Batch Requests
```bash
docker run --rm \
  -e MODEL_ID=gpt-3.5-turbo \
  -e API_KEY=sk-key \
  -e PROMPTS='[...100 prompts...]' \
  --memory=4g \
  --cpus=4 \
  litellm-app:latest
```

### For Low-Latency Requirements
```bash
# Use faster model
MODEL_ID=gpt-3.5-turbo  # Not gpt-4

# Use local model
MODEL_ID=ollama/neural-chat
```

---

## Troubleshooting Configuration

### Issue: Variables not being read
**Solution:** Ensure proper escaping and quoting:
```bash
# Use full path for .env
docker run --env-file C:\full\path\.env litellm-app:latest
```

### Issue: Complex prompts failing
**Solution:** Use JSON array format and proper escaping:
```bash
PROMPTS='["Question with \"quotes\"", "Question 2"]'
```

### Issue: API key not working
**Solution:** Verify key format and permissions:
- OpenAI: Starts with `sk-`
- Anthropic: Starts with `sk-ant-`
- Check API key has necessary permissions

---

For more help, see README.md and QUICKSTART.md
