 `README.md`
# College Student AI Assistant — LangChain & Ollama

A local, privacy-first AI Assistant and LangChain toolkit designed for academic administrative inquiries, student record lookups, and automated academic calculations. Powered by LangChain and a local Ollama model (`qwen2.5:3b`).

---

## Project Structure
.
├── college_assistant.py     # Main interactive CLI tool-calling agent
├── custom_tools.py          # Zero-shot ReAct agent implementation with custom tools
├── parser.py                # Structured output extraction using Pydantic & JsonOutputParser
├── lcel.py                  # LangChain Expression Language (LCEL) invocation, streaming, and batching
├── prompttemplate.py        # ChatPromptTemplate formatting demonstrations
├── model.py                 # Direct Ollama LLM integration baseline
├── report.py                # Conversation history buffer and JSON session export
├── session_report.json      # Serialized conversation session logs
└── requirements.txt         # Project dependencies

```

---

## Core Features & Modules

### 1. Main Interactive Assistant (`college_assistant.py`)

A tool-calling agent powered by `create_tool_calling_agent` that answers student queries via specialized tools:

* **Attendance Calculator:** Computes percentage and exam eligibility (minimum 75% threshold).
* **Result Calculator:** Computes 5-subject average, letter grade (A–D), and pass/fail status.
* **Fee Balance Calculator:** Tracks pending course fee balances.
* **Library Fine Calculator:** Calculates overdue book fees (₹5/day).
* **Hostel Fee Calculator:** Calculates boarding costs based on stay duration.
* **Student Profile Lookup:** Queries the mock student database by ID.

### 2. LangChain Foundations & ReAct Agent

* **ReAct Agent (`custom_tools.py`):** Uses `ZERO_SHOT_REACT_DESCRIPTION` with a safe mathematical evaluator and student status lookup.
* **Structured JSON Parser (`parser.py`):** Extracts unstructured student notes directly into typed Pydantic models (`StudentProfile`).
* **LCEL Pipelines (`lcel.py`):** Demonstrates single invoke, token-by-token streaming, and parallel batch queries across technical domains.
* **Conversation Auditing (`report.py`):** Manages `ConversationBufferWindowMemory` and exports interactions to `session_report.json`.

---

## Setup & Installation

### Step 1 — Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```
### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt

```
### Step 3 — Pull the Local LLM via Ollama

Ensure [Ollama](https://ollama.com/) is installed and running, then pull the target model:

```bash
ollama pull qwen2.5:3b

```
---
## Usage Guide
### Run the Interactive College Assistant
```bash
python college_assistant.py

```
**Example Queries:**

* *"Can student S001 take the exam if they attended 42 out of 50 classes?"*
* *"Check fee balance for course fee 85000 and paid 60000."*
* *"Look up profile for student S002."*
* *"Calculate grade for marks: 85, 78, 92, 66, 74."*

### Run Individual Demonstrations

```bash
# Structured JSON extraction
python parser.py

# LCEL invoke, streaming, and batching
python lcel.py

# ReAct Agent with safe calculator
python custom_tools.py

# Export conversation memory to JSON
python report.py

```

```

```