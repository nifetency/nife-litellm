"""
nife-llmlite - Production-Ready LiteLLM API Service
Simple, fast, multi-provider LLM API wrapper
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from typing import Dict, Any, List
import litellm
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# LiteLLM configuration
litellm.set_verbose = os.getenv("VERBOSE", "false").lower() == "true"
litellm.drop_params = True


def detect_provider(model_id: str) -> str:
    """Detect provider from model ID"""
    model_lower = model_id.lower()
    
    # Check for prefix-based providers
    if "/" in model_id:
        prefix = model_id.split("/")[0].lower()
        provider_map = {
            "google": "google", "gemini": "google", 
            "together_ai": "together", "replicate": "replicate",
            "groq": "groq", "anyscale": "anyscale",
            "perplexity": "perplexity", "huggingface": "huggingface"
        }
        return provider_map.get(prefix, prefix)
    
    # Pattern-based detection
    if any(x in model_lower for x in ["gpt", "o1-", "o3-"]):
        return "openai"
    if any(x in model_lower for x in ["claude", "anthropic"]):
        return "anthropic"
    if "gemini" in model_lower:
        return "google"
    if any(x in model_lower for x in ["mistral", "mixtral"]):
        return "mistral"
    if "llama" in model_lower:
        return "together"
    if any(x in model_lower for x in ["command", "cohere"]):
        return "cohere"
    if "deepseek" in model_lower:
        return "deepseek"
    
    return "unknown"


def normalize_model_id(model_id: str) -> str:
    """Normalize model ID for LiteLLM"""
    model_lower = model_id.lower()
    
    # Gemini normalization
    if model_lower.startswith("google/gemini"):
        return model_id.replace("google/", "gemini/", 1)
    if "gemini" in model_lower and "/" not in model_id:
        return f"gemini/{model_id}"
    
    # Together AI (Llama) normalization
    if "llama" in model_lower and "/" not in model_id:
        return f"together_ai/{model_id}"
    
    # Mistral normalization
    if any(x in model_lower for x in ["mistral", "mixtral"]) and "/" not in model_id:
        return f"mistral/{model_id}"
    
    # DeepSeek normalization
    if "deepseek" in model_lower and "/" not in model_id:
        return f"deepseek/{model_id}"
    
    return model_id


def set_api_key(model_id: str, api_key: str) -> str:
    """Set provider API key and return normalized model ID"""
    normalized = normalize_model_id(model_id)
    provider = detect_provider(normalized)
    
    # Map provider to environment variable
    key_mapping = {
        "google": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "cohere": "COHERE_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "together": "TOGETHERAI_API_KEY",
        "replicate": "REPLICATE_API_KEY",
        "groq": "GROQ_API_KEY"
    }
    
    env_key = key_mapping.get(provider, "LITELLM_API_KEY")
    os.environ[env_key] = api_key
    
    logger.info(f"Provider: {provider}, Model: {normalized}")
    return normalized


@app.route('/', methods=['GET'])
def root():
    """API information endpoint"""
    return jsonify({
        "service": "nife-llmlite",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "completion": "/api/completion",
            "models": "/api/models"
        }
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/completion', methods=['POST'])
def completion():
    """
    LLM completion endpoint
    
    Request Body:
    {
        "model_id": "gpt-4",
        "api_key": "sk-...",
        "prompts": ["question 1", "question 2"],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    Response:
    {
        "timestamp": "2024-...",
        "model": "gpt-4",
        "provider": "openai",
        "responses": [...],
        "summary": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Required fields validation
        model_id = data.get('model_id')
        api_key = data.get('api_key')
        prompts = data.get('prompts')
        
        if not model_id:
            return jsonify({"error": "model_id is required"}), 400
        if not api_key:
            return jsonify({"error": "api_key is required"}), 400
        if not prompts:
            return jsonify({"error": "prompts is required"}), 400
        
        # Optional parameters
        temperature = float(data.get('temperature', 0.7))
        max_tokens = int(data.get('max_tokens', 1000))
        
        # Normalize prompts to list
        if isinstance(prompts, str):
            prompts = [prompts]
        
        # Set API key and get normalized model
        normalized_model = set_api_key(model_id, api_key)
        provider = detect_provider(normalized_model)
        
        # Process all prompts
        results = {
            "timestamp": datetime.now().isoformat(),
            "model": model_id,
            "normalized_model": normalized_model,
            "provider": provider,
            "responses": [],
            "summary": {
                "total": len(prompts),
                "successful": 0,
                "failed": 0
            }
        }
        
        for idx, prompt in enumerate(prompts, 1):
            try:
                response = litellm.completion(
                    model=normalized_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                content = response.choices[0].message.content
                
                results["responses"].append({
                    "prompt_id": idx,
                    "prompt": prompt,
                    "response": content,
                    "status": "success"
                })
                results["summary"]["successful"] += 1
                logger.info(f"Prompt {idx}/{len(prompts)} completed")
                
            except Exception as e:
                results["responses"].append({
                    "prompt_id": idx,
                    "prompt": prompt,
                    "response": None,
                    "status": "error",
                    "error": str(e)
                })
                results["summary"]["failed"] += 1
                logger.error(f"Prompt {idx} failed: {str(e)}")
        
        # Return 207 if partial success, 200 if all successful
        status_code = 200 if results["summary"]["failed"] == 0 else 207
        return jsonify(results), status_code
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/models', methods=['GET'])
def models():
    """List supported providers and example models"""
    return jsonify({
        "providers": {
            "openai": {
                "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"],
                "api_key_env": "OPENAI_API_KEY"
            },
            "anthropic": {
                "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
                "api_key_env": "ANTHROPIC_API_KEY"
            },
            "google": {
                "models": ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"],
                "api_key_env": "GEMINI_API_KEY"
            },
            "mistral": {
                "models": ["mistral-large", "mistral-medium", "mistral-small"],
                "api_key_env": "MISTRAL_API_KEY"
            },
            "cohere": {
                "models": ["command", "command-light", "command-r"],
                "api_key_env": "COHERE_API_KEY"
            },
            "together": {
                "models": ["meta-llama/Llama-3-70b-chat-hf"],
                "api_key_env": "TOGETHERAI_API_KEY"
            },
            "deepseek": {
                "models": ["deepseek-chat", "deepseek-coder"],
                "api_key_env": "DEEPSEEK_API_KEY"
            }
        },
        "note": "This is a sample list. Check provider documentation for complete model catalog."
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info("=" * 60)
    logger.info(f"🚀 nife-llmlite API starting")
    logger.info(f"📍 Address: {host}:{port}")
    logger.info(f"🐛 Debug: {debug}")
    logger.info("=" * 60)
    
    app.run(host=host, port=port, debug=debug)
