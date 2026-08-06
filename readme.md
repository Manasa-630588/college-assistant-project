# ABC Technologies — AI Customer Support System
AI-Powered Customer Support Automation using LangGraph, LangChain, Ollama, and SQLite.
## Project Structure
customer_support/
├── main.py                   ← Full source code (all 10 tasks)
├── memory.db                 ← SQLite memory (auto-created on first run)
├── README.md                 ← This file
└── documents/
    ├── company_policy.txt    ← Refund, cancellation, escalation policies
    ├── pricing_guide.txt     ← Subscription plans and pricing
    ├── technical_manual.txt  ← Troubleshooting and technical help
    └── faq.txt               ← Frequently asked questions
## Setup Instructions

### Step 1 — Activate your virtual environment
```bash
# Windows (from agentic_frwk folder)
venv\Scripts\activate
```

### Step 2 — Install required packages
```bash
pip install langgraph langchain langchain-ollama langchain-core langchain-community
```

### Step 3 — Pull the Ollama model (run once)
```bash
ollama pull qwen2.5:3b
```

### Step 4 — Run the system
```bash
cd customer_support
python main.py
```

## What Happens When You Run It

The system will automatically process 5 demonstration queries:

| Query | Department | Special Feature |
|-------|-----------|-----------------|
| Pricing plans? | Sales | RAG retrieves pricing_guide.txt |
| Forgot password | Account | RAG retrieves faq.txt |
| App crashes on upload | Technical | RAG retrieves technical_manual.txt |
| Need a refund | Billing | ⚠ PAUSES for human approval |
| What was my previous issue? | Memory | Reads from SQLite database |

### For Query 4 (Refund):
The system will pause and ask you:
```
SUPERVISOR: Approve this request? (yes/no):
```
Type `yes` to approve or `no` to reject.

## Tasks Implemented

| Task | Description | Location in code |
|------|-------------|-----------------|
| Task 1 | LangGraph Workflow | `build_graph()` function |
| Task 2 | State Structure | `SupportState` TypedDict |
| Task 3 | Intent Classification | `classify_intent()` node |
| Task 4 | Conditional Routing | `route_to_department()` |
| Task 5 | Department Agents | `sales_agent`, `technical_agent`, `billing_agent`, `account_agent` |
| Task 6 | RAG Pipeline | `rag_retrieval()` + `retrieve_context()` |
| Task 7 | SQLite Memory | `init_memory_db()`, `save_message()`, `load_history()` |
| Task 8 | Human-in-the-Loop | `human_in_the_loop()` node |
| Task 9 | Supervisor Agent | `supervisor_agent()` node |
| Task 10 | Demonstration | `if __name__ == "__main__"` block |

## Human-in-the-Loop Triggers

The following request types require supervisor approval:
- Refund requests
- Subscription cancellation
- Account closure
- Compensation requests
- Escalation to management