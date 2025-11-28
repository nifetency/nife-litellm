"""
LiteLLM Docker Application
Accepts model_id, api_key, and prompts as environment variables
Supports: OpenAI, Anthropic, Google (Gemini), Cohere, Mistral, Llama (via various providers)
"""

import os
import json
import sys
from typing import Dict, Any, List, Optional
import litellm
from datetime import datetime

# Set up logging
litellm.set_verbose = os.getenv("VERBOSE", "false").lower() == "true"


def validate_env_vars() -> Dict[str, str]:
    """
    Validate and retrieve required environment variables
    """
    required_vars = {
        "MODEL_ID": os.getenv("MODEL_ID"),
        "API_KEY": os.getenv("API_KEY"),
        "PROMPTS": os.getenv("PROMPTS"),
    }

    missing_vars = [key for key, value in required_vars.items() if not value]

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    return required_vars


def parse_prompts(prompts_str: str) -> List[str]:
    """
    Parse prompts from environment variable
    Supports both JSON array format and pipe-separated format
    """
    prompts_str = prompts_str.strip()

    # Try JSON format first
    if prompts_str.startswith("["):
        try:
            prompts = json.loads(prompts_str)
            if isinstance(prompts, list):
                return [str(p) for p in prompts]
        except json.JSONDecodeError as e:
            print(f"[WARN] Failed to parse JSON prompts: {e}", file=sys.stderr)

    # Try pipe-separated format
    if "|" in prompts_str:
        return [p.strip() for p in prompts_str.split("|") if p.strip()]

    # Single prompt
    return [prompts_str]


def detect_provider(model_id: str) -> str:
    """
    Detect the provider based on model_id
    """
    model_id_lower = model_id.lower()
    
    # Check for explicit provider prefixes
    if "/" in model_id:
        provider_prefix = model_id.split("/")[0].lower()
        # Map prefixes to standard provider names
        prefix_map = {
            "google": "google",
            "gemini": "google",
            "together_ai": "together",
            "replicate": "replicate",
            "groq": "groq",
            "anyscale": "anyscale",
            "perplexity": "perplexity",
            "huggingface": "huggingface"
        }
        return prefix_map.get(provider_prefix, provider_prefix)
    
    # Detect by model name patterns
    if any(x in model_id_lower for x in ["gpt-", "gpt4", "gpt3", "o1-", "o3-"]):
        return "openai"
    elif any(x in model_id_lower for x in ["claude", "anthropic"]):
        return "anthropic"
    elif "gemini" in model_id_lower:
        return "google"
    elif "mistral" in model_id_lower or "mixtral" in model_id_lower:
        return "mistral"
    elif any(x in model_id_lower for x in ["llama", "meta-llama"]):
        return "llama"
    elif "command" in model_id_lower or "cohere" in model_id_lower:
        return "cohere"
    elif any(x in model_id_lower for x in ["deepseek", "deep-seek"]):
        return "deepseek"
    
    return "unknown"


def normalize_model_id(model_id: str) -> str:
    """
    Normalize model ID to LiteLLM's expected format
    """
    model_id_lower = model_id.lower()
    
    # Fix Google/Gemini model IDs - LiteLLM expects 'gemini/' prefix
    if model_id_lower.startswith("google/gemini"):
        return model_id.replace("google/", "gemini/", 1)
    
    # If it's a bare Gemini model without prefix, add it
    if "gemini" in model_id_lower and "/" not in model_id:
        return f"gemini/{model_id}"
    
    # For Llama models without prefix, try to use together_ai as default
    if any(x in model_id_lower for x in ["llama-4", "llama-3"]) and "/" not in model_id:
        return f"together_ai/{model_id}"
    
    # For Mistral models, ensure proper prefix
    if any(x in model_id_lower for x in ["mixtral", "mistral"]) and "/" not in model_id:
        return f"mistral/{model_id}"
    
    # For DeepSeek models
    if "deepseek" in model_id_lower and "/" not in model_id:
        return f"deepseek/{model_id}"
    
    return model_id


def set_provider_api_key(model_id: str, api_key: str) -> str:
    """
    Set API keys based on the provider.
    Supports multiple LLM providers with proper routing.
    Returns normalized model_id.
    """
    # Normalize the model ID first
    normalized_id = normalize_model_id(model_id)
    provider = detect_provider(normalized_id)
    model_id_lower = normalized_id.lower()
    
    if normalized_id != model_id:
        print(f"[INFO] Normalized model ID: {model_id} -> {normalized_id}")
    print(f"[INFO] Detected provider: {provider}")
    
    # Google/Gemini - use Google AI Studio
    if provider == "google" or "gemini" in model_id_lower:
        os.environ["GEMINI_API_KEY"] = api_key
        print("[INFO] Using Google AI Studio (Gemini) via GEMINI_API_KEY")
        return normalized_id
    
    # OpenAI
    if provider == "openai" or any(x in model_id_lower for x in ["gpt", "o1-", "o3-"]):
        os.environ["OPENAI_API_KEY"] = api_key
        print("[INFO] Using OpenAI API")
        return normalized_id
    
    # Anthropic
    if provider == "anthropic" or "claude" in model_id_lower:
        os.environ["ANTHROPIC_API_KEY"] = api_key
        print("[INFO] Using Anthropic API")
        return normalized_id
    
    # Mistral
    if provider == "mistral" or "mistral" in model_id_lower or "mixtral" in model_id_lower:
        os.environ["MISTRAL_API_KEY"] = api_key
        print("[INFO] Using Mistral API")
        return normalized_id
    
    # Cohere
    if provider == "cohere" or "command" in model_id_lower:
        os.environ["COHERE_API_KEY"] = api_key
        print("[INFO] Using Cohere API")
        return normalized_id
    
    # DeepSeek
    if provider == "deepseek" or "deepseek" in model_id_lower:
        os.environ["DEEPSEEK_API_KEY"] = api_key
        print("[INFO] Using DeepSeek API")
        return normalized_id
    
    # Llama models - these can be hosted on various platforms
    if provider == "llama" or "llama" in model_id_lower or provider in ["together", "together_ai"]:
        # Check for specific hosting platforms
        if "together" in model_id_lower or provider == "together" or provider == "together_ai":
            os.environ["TOGETHERAI_API_KEY"] = api_key
            print("[INFO] Using Together AI for Llama models")
        elif "replicate" in model_id_lower or provider == "replicate":
            os.environ["REPLICATE_API_KEY"] = api_key
            print("[INFO] Using Replicate for Llama models")
        elif "anyscale" in model_id_lower or provider == "anyscale":
            os.environ["ANYSCALE_API_KEY"] = api_key
            print("[INFO] Using Anyscale for Llama models")
        elif "perplexity" in model_id_lower or provider == "perplexity":
            os.environ["PERPLEXITYAI_API_KEY"] = api_key
            print("[INFO] Using Perplexity AI for Llama models")
        elif "groq" in model_id_lower or provider == "groq":
            os.environ["GROQ_API_KEY"] = api_key
            print("[INFO] Using Groq for Llama models")
        elif "huggingface" in model_id_lower or provider == "huggingface":
            os.environ["HUGGINGFACE_API_KEY"] = api_key
            print("[INFO] Using HuggingFace for Llama models")
        else:
            # Default to Together AI for Llama
            os.environ["TOGETHERAI_API_KEY"] = api_key
            print("[INFO] Using Together AI for Llama models (default)")
        return normalized_id
    
    # Fallback - set generic LiteLLM API key
    print(f"[WARN] Unknown provider '{provider}', using LITELLM_API_KEY as fallback")
    os.environ["LITELLM_API_KEY"] = api_key
    return normalized_id


def call_litellm(
    model_id: str, api_key: str, prompts: List[str]
) -> Dict[str, Any]:
    """
    Call LiteLLM with the provided model, API key, and prompts
    """
    # Set API key and get normalized model ID
    normalized_model_id = set_provider_api_key(model_id, api_key)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "model": model_id,
        "normalized_model": normalized_model_id,
        "provider": detect_provider(normalized_model_id),
        "responses": [],
        "errors": [],
        "summary": {
            "total_prompts": len(prompts),
            "successful": 0,
            "failed": 0,
        },
    }

    # Process each prompt
    for idx, prompt in enumerate(prompts, 1):
        print(f"[INFO] Processing prompt {idx}/{len(prompts)}...")
        try:
            response = litellm.completion(
                model=normalized_model_id,  # Use normalized model ID
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            response_content = response.choices[0].message.content
            
            results["responses"].append(
                {
                    "prompt_id": idx,
                    "prompt": prompt,
                    "response": response_content,
                    "status": "success",
                    "model_used": getattr(response, "model", normalized_model_id),
                }
            )
            results["summary"]["successful"] += 1
            print(f"[SUCCESS] Prompt {idx} completed")

        except Exception as e:
            error_msg = f"Error processing prompt {idx}: {str(e)}"
            results["responses"].append(
                {
                    "prompt_id": idx,
                    "prompt": prompt,
                    "response": None,
                    "status": "error",
                    "error": str(e),
                }
            )
            results["errors"].append(error_msg)
            results["summary"]["failed"] += 1
            print(f"[ERROR] {error_msg}", file=sys.stderr)

    return results


def format_output(results: Dict[str, Any]) -> str:
    """
    Format results for output
    """
    output = []
    output.append("=" * 80)
    output.append("LiteLLM Docker Application Results")
    output.append("=" * 80)
    output.append(f"Timestamp: {results['timestamp']}")
    output.append(f"Model: {results['model']}")
    if results.get('normalized_model') and results['normalized_model'] != results['model']:
        output.append(f"Normalized Model: {results['normalized_model']}")
    output.append(f"Provider: {results['provider']}")
    output.append("")
    output.append("Summary:")
    output.append(f"  Total Prompts: {results['summary']['total_prompts']}")
    output.append(f"  Successful: {results['summary']['successful']}")
    output.append(f"  Failed: {results['summary']['failed']}")
    output.append("")
    output.append("Detailed Results:")
    output.append("-" * 80)

    for resp in results["responses"]:
        output.append(f"\nPrompt {resp['prompt_id']}:")
        output.append(f"  Input: {resp['prompt'][:100]}{'...' if len(resp['prompt']) > 100 else ''}")
        if resp["status"] == "success":
            response_preview = resp['response'][:200] if resp['response'] else ""
            output.append(f"  Response: {response_preview}{'...' if len(resp.get('response', '')) > 200 else ''}")
            if "model_used" in resp:
                output.append(f"  Model Used: {resp['model_used']}")
        else:
            output.append(f"  Error: {resp['error']}")

    output.append("")
    output.append("=" * 80)
    output.append("Raw JSON Output:")
    output.append("=" * 80)

    return "\n".join(output)


def print_supported_providers():
    """
    Print information about supported providers
    """
    print("""
Supported LLM Providers and Model ID Formats:
---------------------------------------------

OpenAI:
  - gpt-4o, gpt-4.1-mini, gpt-4.1-nano
  - Example: MODEL_ID=gpt-4o
  
Anthropic:
  - claude-3-7-sonnet-20250219, claude-3-haiku-20240307, claude-opus-4-1-20250805
  - Example: MODEL_ID=claude-3-7-sonnet-20250219
  
Google Gemini:
  - gemini-2.5-flash, gemini-2.0-pro, gemini-1.5-pro
  - Format: gemini/MODEL_NAME or google/gemini-MODEL_NAME (auto-normalized)
  - Example: MODEL_ID=gemini/gemini-2.5-flash
  - Example: MODEL_ID=google/gemini-1.5-pro (will be normalized to gemini/gemini-1.5-pro)
  
Mistral AI:
  - mistral-large-latest, mistral-small, open-mixtral-8x7b
  - Format: mistral/MODEL_NAME or just MODEL_NAME
  - Example: MODEL_ID=mistral/mistral-large-latest
  
Meta Llama (via various providers):
  - Llama-4-Scout-17B-16E-Instruct-FP8, Llama-3.3-8B-Instruct, Llama-4-Maverick-17B-128E-Instruct-FP8
  - Together AI: MODEL_ID=together_ai/meta-llama/Llama-3-70b-chat-hf
  - Replicate: MODEL_ID=replicate/meta/llama-2-70b-chat
  - Groq: MODEL_ID=groq/llama3-70b-8192
  - Anyscale: MODEL_ID=anyscale/meta-llama/Llama-2-70b-chat-hf
  - HuggingFace: MODEL_ID=huggingface/meta-llama/Llama-2-7b-chat-hf
  
Cohere:
  - cohere-command-r, command-r-plus
  - Example: MODEL_ID=command-r
  
DeepSeek:
  - deepseek-v3, deepseek-coder
  - Format: deepseek/MODEL_NAME or just MODEL_NAME
  - Example: MODEL_ID=deepseek/deepseek-v3

Environment Variables Required:
  MODEL_ID    - The model identifier (see formats above)
  API_KEY     - Your API key for the provider
  PROMPTS     - JSON array or pipe-separated prompts
  VERBOSE     - (Optional) Set to "true" for detailed logs

Examples:
  # Single prompt
  MODEL_ID=gemini/gemini-2.5-flash API_KEY=your_key PROMPTS="Hello, world!"
  
  # Multiple prompts (JSON)
  PROMPTS='["What is AI?", "Explain quantum computing"]'
  
  # Multiple prompts (pipe-separated)
  PROMPTS="What is AI? | Explain quantum computing"

Note: The application will automatically normalize model IDs to the correct
      format required by LiteLLM (e.g., google/gemini-* -> gemini/gemini-*)
    """)
    
def main():
    """
    Main entry point
    """
    try:
        # Check for help flag
        if "--help" in sys.argv or "-h" in sys.argv:
            print_supported_providers()
            sys.exit(0)
        
        # Validate environment variables
        env_vars = validate_env_vars()

        # Parse prompts
        prompts = parse_prompts(env_vars["PROMPTS"])
        
        if not prompts:
            raise ValueError("No valid prompts found in PROMPTS environment variable")

        print("[INFO] Starting LiteLLM Docker Application")
        print(f"[INFO] Model: {env_vars['MODEL_ID']}")
        print(f"[INFO] Number of prompts: {len(prompts)}")
        print("[INFO] Processing prompts...")

        # Call LiteLLM - model_id is now normalized inside call_litellm
        results = call_litellm(
            env_vars["MODEL_ID"], env_vars["API_KEY"], prompts
        )

        # Format and print output
        formatted_output = format_output(results)
        print("\n" + formatted_output)

        # Also output raw JSON for programmatic use
        print(json.dumps(results, indent=2))

        # Exit with appropriate code
        exit_code = 0 if results["summary"]["failed"] == 0 else 1
        sys.exit(exit_code)

    except ValueError as ve:
        print(f"[ERROR] Configuration Error: {str(ve)}", file=sys.stderr)
        print("\nUse --help to see supported providers and usage examples", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()