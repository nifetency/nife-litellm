# LiteLLM Docker Application

A containerized Python application that uses LiteLLM to process prompts against various LLM providers (OpenAI, Anthropic, Google, Cohere, etc.) with environment variables for configuration.

## Features

- ✅ **Multi-Provider Support**: Works with OpenAI, Claude, Gemini, Cohere, and more
- ✅ **Environment Variable Configuration**: All parameters passed via env vars
- ✅ **Batch Processing**: Handle multiple prompts in a single run
- ✅ **Error Handling**: Graceful error handling with detailed error messages
- ✅ **JSON Output**: Structured JSON output for programmatic use
- ✅ **Docker Support**: Easy containerization and deployment
- ✅ **Docker Compose**: Pre-configured for quick testing

## Project Structure

```
litellm-docker-app/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Prerequisites

- Docker & Docker Compose installed
- API Key for your chosen LLM provider
- Python 3.11+ (for local development)

## Installation

### Option 1: Using Docker Compose (Recommended)

1. Clone or navigate to the project directory:
```bash
cd litellm-docker-app
```

2. Create a `.env` file with your API credentials:
```bash
cp .env.example .env
# Edit .env with your API key
```

3. Build and run:
```bash
docker-compose up --build
```

### Option 2: Manual Docker Build

1. Build the image:
```bash
docker build -t litellm-app:latest .
```

2. Run the container:
```bash
docker run --rm \
  -e MODEL_ID="gpt-3.5-turbo" \
  -e API_KEY="your-api-key-here" \
  -e PROMPTS="What is AI?" \
  litellm-app:latest
```

### Option 3: Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export MODEL_ID="gpt-3.5-turbo"
export API_KEY="your-api-key-here"
export PROMPTS="What is Docker?"
```

3. Run the application:
```bash
python app.py
```

## Environment Variables

### Required

- **MODEL_ID**: The LLM model identifier (e.g., `gpt-3.5-turbo`, `claude-3-sonnet`, `gemini-pro`)
- **API_KEY**: Your API key for the service
- **PROMPTS**: Prompts to send to the model (see formats below)

### Optional

- **VERBOSE**: Set to `true` for detailed logging (default: `false`)

## Prompt Formats

The `PROMPTS` environment variable supports multiple formats:

### Single Prompt
```bash
PROMPTS="What is machine learning?"
```

### Pipe-Separated Prompts
```bash
PROMPTS="What is AI? | Explain Docker | Tell me about Python"
```

### JSON Array Format
```bash
PROMPTS='["What is machine learning?", "Explain Docker in one sentence", "Tell me about Python"]'
```

## Usage Examples

### Example 1: OpenAI GPT-3.5-Turbo

```bash
docker run --rm \
  -e MODEL_ID="gpt-3.5-turbo" \
  -e API_KEY="sk-your-openai-key" \
  -e PROMPTS="What is artificial intelligence?" \
  litellm-app:latest
```

### Example 2: Anthropic Claude

```bash
docker run --rm \
  -e MODEL_ID="claude-3-sonnet-20240229" \
  -e API_KEY="sk-ant-your-anthropic-key" \
  -e PROMPTS="Explain quantum computing in simple terms" \
  litellm-app:latest
```

### Example 3: Google Gemini

```bash
docker run --rm \
  -e MODEL_ID="gemini-pro" \
  -e API_KEY="your-google-api-key" \
  -e PROMPTS="What are the benefits of cloud computing?" \
  litellm-app:latest
```

### Example 4: Multiple Prompts (Pipe-Separated)

```bash
docker run --rm \
  -e MODEL_ID="gpt-3.5-turbo" \
  -e API_KEY="sk-your-openai-key" \
  -e PROMPTS="What is ML? | Explain NLP | Tell me about LLMs | What is Docker?" \
  -e VERBOSE="true" \
  litellm-app:latest
```

### Example 5: Multiple Prompts (JSON Array)

```bash
docker run --rm \
  -e MODEL_ID="gpt-3.5-turbo" \
  -e API_KEY="sk-your-openai-key" \
  -e PROMPTS='["Question 1", "Question 2", "Question 3"]' \
  litellm-app:latest
```

### Example 6: Using Docker Compose with .env File

**.env file:**
```
MODEL_ID=gpt-3.5-turbo
API_KEY=sk-your-openai-key
PROMPTS=What is Docker? | Explain containerization
VERBOSE=true
```

**Run:**
```bash
docker-compose up --build
```

## Output Format

The application returns results in two formats:

### Formatted Output (Console)
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
...
```

### JSON Output (Structured)
```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "model": "gpt-3.5-turbo",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "What is AI?",
      "response": "AI (Artificial Intelligence) is...",
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

## Supported Models

### OpenAI
- `gpt-4`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

### Anthropic
- `claude-3-opus`
- `claude-3-sonnet-20240229`
- `claude-3-haiku`

### Google
- `gemini-pro`
- `gemini-1.5-pro`

### Cohere
- `command`
- `command-light`

## Exit Codes

- `0`: All prompts processed successfully
- `1`: One or more prompts failed or missing env vars

## Troubleshooting

### Issue: "Missing required environment variables"
**Solution**: Ensure MODEL_ID, API_KEY, and PROMPTS are all set
```bash
docker run --rm -e MODEL_ID="..." -e API_KEY="..." -e PROMPTS="..." litellm-app:latest
```

### Issue: "Invalid API Key"
**Solution**: Verify your API key is correct and has necessary permissions

### Issue: "Model not found"
**Solution**: Check supported models from your provider's documentation

### Issue: Docker build fails
**Solution**: Ensure Docker is running and you have internet connectivity for downloading dependencies

## Advanced Configuration

### Building for Production

```bash
docker build -t litellm-app:1.0.0 .
docker tag litellm-app:1.0.0 your-registry/litellm-app:1.0.0
docker push your-registry/litellm-app:1.0.0
```

### Running with Docker Compose and Volume Mounting

```yaml
version: '3.8'
services:
  litellm-app:
    build: .
    volumes:
      - ./logs:/app/logs
    environment:
      - MODEL_ID=gpt-3.5-turbo
      - API_KEY=${API_KEY}
      - PROMPTS=${PROMPTS}
```

## Performance Tips

1. **Batch Requests**: Process multiple prompts in a single container run to reduce overhead
2. **Model Selection**: Use faster models (gpt-3.5-turbo) for quick responses
3. **Resource Limits**: Set appropriate CPU and memory limits in Docker

## Security Considerations

1. **Never hardcode API keys**: Always use environment variables
2. **Use secrets management**: In production, use Docker secrets or environment managers
3. **Validate inputs**: The app validates all required env vars
4. **HTTPS only**: When using API keys, ensure HTTPS connections

## Development

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set env vars
export MODEL_ID="gpt-3.5-turbo"
export API_KEY="your-key"
export PROMPTS="Test prompt"

# Run
python app.py
```

### Debugging

Enable verbose logging:
```bash
docker run --rm \
  -e VERBOSE="true" \
  -e MODEL_ID="..." \
  -e API_KEY="..." \
  -e PROMPTS="..." \
  litellm-app:latest
```

## Contributing

Feel free to modify the application for your specific needs. Key areas for customization:

- Temperature and other model parameters in `app.py`
- Additional environment variables for advanced configurations
- Custom prompt processing logic

## License

MIT License - Feel free to use this project for any purpose.

## Support

For issues with LiteLLM: [LiteLLM Documentation](https://docs.litellm.ai/)
For Docker issues: [Docker Documentation](https://docs.docker.com/)
