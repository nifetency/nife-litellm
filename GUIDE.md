# Visual Guide - How It All Works Together

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Local Machine                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Docker Engine                                      │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  litellm-app Container                       │   │  │
│  │  │                                              │   │  │
│  │  │  ┌────────────────────────────────────────┐ │   │  │
│  │  │  │ Python Application (app.py)            │ │   │  │
│  │  │  │                                        │ │   │  │
│  │  │  │ 1. Reads Environment Variables        │ │   │  │
│  │  │  │    - MODEL_ID                         │ │   │  │
│  │  │  │    - API_KEY                          │ │   │  │
│  │  │  │    - PROMPTS                          │ │   │  │
│  │  │  │                                        │ │   │  │
│  │  │  │ 2. Initializes LiteLLM                │ │   │  │
│  │  │  │                                        │ │   │  │
│  │  │  │ 3. Processes Prompts                  │ │   │  │
│  │  │  │                                        │ │   │  │
│  │  │  │ 4. Returns Results (JSON + Formatted) │ │   │  │
│  │  │  └────────────────────────────────────────┘ │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│                   ┌─────────────────┐                      │
│                   │ Internet        │                      │
│                   └────────┬────────┘                      │
│                            │                                │
└────────────────────────────┼────────────────────────────────┘
                             │
                ┌────────────┬────────────┬────────────┐
                │            │            │            │
                ▼            ▼            ▼            ▼
          ┌─────────┐  ┌──────────┐ ┌────────┐ ┌──────────┐
          │ OpenAI  │  │Anthropic │ │ Google │ │  Cohere  │
          │         │  │ (Claude) │ │(Gemini)│ │          │
          └─────────┘  └──────────┘ └────────┘ └──────────┘
```

## Data Flow Diagram

```
INPUT LAYER
├─ Environment Variables
│  ├─ MODEL_ID
│  ├─ API_KEY
│  └─ PROMPTS (multiple formats)
│
PROCESSING LAYER
├─ Parse prompts (single/pipe/JSON)
├─ Validate environment vars
├─ Set up LiteLLM with API key
└─ Route to correct LLM provider
│
LLM PROVIDERS
├─ OpenAI API
├─ Anthropic API
├─ Google API
└─ Other providers...
│
RESPONSE HANDLING
├─ Collect responses
├─ Handle errors
├─ Format results
└─ Generate exit code
│
OUTPUT LAYER
├─ Formatted Console Output
├─ Structured JSON Output
└─ Exit Code (0 = success, 1 = failure)
```

## Execution Flow

```
START
  │
  ├─► Check Docker is installed
  │
  ├─► Build Docker Image
  │   └─► FROM python:3.11-slim
  │       ├─ Install dependencies
  │       ├─ Copy app.py
  │       └─ Set entry point
  │
  ├─► Run Container
  │   └─► Pass environment variables
  │
  ├─► Container Startup
  │   └─► app.py executes
  │
  ├─► Validation
  │   ├─ Check MODEL_ID exists
  │   ├─ Check API_KEY provided
  │   └─ Check PROMPTS provided
  │
  ├─► Prompt Parsing
  │   ├─ Single: "What is AI?"
  │   ├─ Pipe: "Q1 | Q2 | Q3"
  │   └─ JSON: ["Q1", "Q2"]
  │
  ├─► Process Each Prompt
  │   ├─ Call LiteLLM
  │   ├─ Send to LLM Provider
  │   ├─ Get Response
  │   └─ Handle Errors (if any)
  │
  ├─► Format Output
  │   ├─ Pretty console output
  │   └─ Structured JSON
  │
  ├─► Print Results
  │   └─ Both formats to stdout
  │
  └─► Exit
      ├─ Code 0 (Success)
      └─ Code 1 (Failure)
```

## File Structure Visualization

```
litellm-docker-app/
│
├── 📦 Container Files
│   ├── Dockerfile              (How to build)
│   ├── docker-compose.yml      (How to orchestrate)
│   └── requirements.txt        (Python dependencies)
│
├── 🐍 Application Files
│   └── app.py                  (Main logic)
│
├── 🚀 Runner Scripts
│   ├── run.bat                 (Windows batch)
│   └── run.ps1                 (PowerShell)
│
├── 📚 Documentation
│   ├── README.md               (Full guide)
│   ├── QUICKSTART.md           (Quick start)
│   ├── CONFIGURATION.md        (Config ref)
│   ├── PROJECT_SUMMARY.md      (This summary)
│   └── GUIDE.md                (This file)
│
├── ⚙️  Configuration
│   ├── .env.example            (Env template)
│   └── .gitignore              (Git ignore)
│
└── 📦 Output (created at runtime)
    └── output/                 (If mounted)
```

## How to Use - Step by Step

### Step 1: Setup
```
        ┌─────────────────┐
        │  Open Terminal  │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │ cd C:\Users\Varun S\Desktop\LiteLLM │
        │     \litellm-docker-app             │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │  Get API Key from:  │
        │  • OpenAI           │
        │  • Anthropic        │
        │  • Google           │
        │  • Cohere           │
        └─────────────────────┘
```

### Step 2: Build
```
┌──────────────────────────────────┐
│  docker build -t litellm-app .   │
└────────┬─────────────────────────┘
         │
         ├─► Check Dockerfile
         ├─► Pull base image
         ├─► Install dependencies
         ├─► Copy application
         └─► Ready to run!
```

### Step 3: Run
```
┌────────────────────────────────────┐
│  docker run --rm                   │
│    -e MODEL_ID=gpt-3.5-turbo      │
│    -e API_KEY=sk-xxx              │
│    -e PROMPTS="What is AI?"        │
│    litellm-app:latest              │
└────────┬────────────────────────────┘
         │
         ├─► Container starts
         ├─► Validates inputs
         ├─► Calls LLM API
         ├─► Gets response
         ├─► Formats output
         └─► Displays results
```

## Environment Variable Flow

```
Environment Variables
│
├─► MODEL_ID
│   └─► Used to determine which LLM provider
│       ├─ gpt-3.5-turbo    → OpenAI
│       ├─ claude-3-sonnet  → Anthropic
│       ├─ gemini-pro       → Google
│       └─ command          → Cohere
│
├─► API_KEY
│   └─► Used to authenticate with provider
│       ├─ Sets OPENAI_API_KEY (for OpenAI)
│       ├─ Sets ANTHROPIC_API_KEY (for Claude)
│       ├─ Sets GOOGLE_API_KEY (for Gemini)
│       └─ Sets COHERE_API_KEY (for Cohere)
│
└─► PROMPTS
    └─► Parsed into array
        ├─ Format: "Single"              → 1 prompt
        ├─ Format: "Q1 | Q2 | Q3"        → 3 prompts
        └─ Format: ["Q1", "Q2", "Q3"]    → 3 prompts
```

## Response Processing

```
Input Prompts
│
├─► Prompt 1: "What is AI?"
│   ├─► Send to LLM API
│   ├─► Wait for response
│   ├─► Get: "AI is the simulation of..."
│   └─► Mark: SUCCESS ✓
│
├─► Prompt 2: "Explain Python"
│   ├─► Send to LLM API
│   ├─► Wait for response
│   ├─► Get: "Python is a programming..."
│   └─► Mark: SUCCESS ✓
│
└─► Prompt 3: (error case)
    ├─► Send to LLM API
    ├─► Error: "Rate limit exceeded"
    └─► Mark: FAILED ✗

Final Output:
├─ Summary: 2 successful, 1 failed
├─ Detailed results with responses/errors
├─ JSON structured output
└─ Exit code: 1 (due to failure)
```

## Docker Compose Orchestration

```
docker-compose.yml
│
├─► Reads from .env file
│
├─► Launches Container
│   ├─ Sets all environment variables
│   ├─ Sets resource limits
│   ├─ Sets network
│   └─ Sets health check
│
└─► Results
    ├─ Formatted output
    └─ JSON output
```

## Prompt Format Parsing

```
Input: PROMPTS environment variable
│
├─► Is it a JSON array?
│   └─ Yes: Parse JSON
│       ├─ ["Q1", "Q2"] → [Q1, Q2]
│       └─ Pass to processor
│
├─► Does it contain |?
│   └─ Yes: Split by |
│       ├─ "Q1 | Q2" → [Q1, Q2]
│       └─ Pass to processor
│
└─► Otherwise
    └─ Single prompt
        ├─ "What is AI?" → [What is AI?]
        └─ Pass to processor
```

## Error Handling Flow

```
                    ┌─────────────────┐
                    │ Process Prompt  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Try LLM Call    │
                    └────────┬────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
              ┌───▼────┐            ┌──▼───┐
              │ Success│            │Error │
              └───┬────┘            └──┬───┘
                  │                     │
          ┌───────▼────────┐   ┌────────▼─────────┐
          │ Store Response │   │ Catch Exception  │
          │ Mark: SUCCESS  │   │ Store Error Msg  │
          │ Count: +1      │   │ Mark: FAILED     │
          │                │   │ Count: +1        │
          └────────────────┘   └──────────────────┘
                  │                     │
                  └──────────┬──────────┘
                             │
                  ┌──────────▼──────────┐
                  │ Continue Next       │
                  │ Prompt              │
                  └─────────────────────┘
```

## Quick Reference Diagram

```
┌─────────────────────────────────────────────────────┐
│            QUICK REFERENCE                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  BUILD:  docker build -t litellm-app:latest .     │
│                                                     │
│  RUN:    docker run --rm \                         │
│           -e MODEL_ID=... \                        │
│           -e API_KEY=... \                         │
│           -e PROMPTS=... \                         │
│           litellm-app:latest                       │
│                                                     │
│  COMPOSE:  docker-compose up --build              │
│                                                     │
│  PROVIDERS:                                         │
│           • gpt-3.5-turbo (OpenAI)                │
│           • claude-3-sonnet (Anthropic)           │
│           • gemini-pro (Google)                   │
│           • command (Cohere)                      │
│                                                     │
│  FORMATS:                                           │
│           • Single: "Question"                     │
│           • Pipe: "Q1 | Q2 | Q3"                  │
│           • JSON: ["Q1", "Q2", "Q3"]              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

**For more details, see README.md and QUICKSTART.md**
