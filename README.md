# AI Support Intelligence & Prompt Optimization Platform

An end-to-end Generative AI support system that analyzes customer complaints, retrieves relevant company knowledge using RAG, generates grounded support responses, evaluates prompt quality, measures AI performance, and tests resistance to common prompt injection attacks.

## Overview

AI Support Intelligence is designed as a portfolio-grade GenAI application for demonstrating practical skills in:

* Prompt Engineering
* Retrieval-Augmented Generation (RAG)
* LLM application development
* Prompt evaluation and optimization
* AI security testing
* Token, latency, and cost monitoring
* FastAPI backend development
* Frontend integration
* Vector search with ChromaDB

The system takes a customer complaint and produces structured analysis, retrieves relevant company knowledge, and generates a grounded support response.

---

## Architecture

```text
Customer Complaint
        |
        v
+-----------------------+
|     FastAPI API       |
+-----------------------+
        |
        +--------------------+
        |                    |
        v                    v
 Complaint Analysis     RAG Retrieval
        |                    |
        |              +-------------+
        |              | ChromaDB    |
        |              +-------------+
        |                    |
        |              Company Knowledge
        |                    |
        +---------+----------+
                  |
                  v
          Groq LLM
        openai/gpt-oss-20b
                  |
                  v
       Grounded Support Response
                  |
                  v
       Performance Metrics
       - Latency
       - Tokens
       - Cost
```

---

## Key Features

### 1. Customer Complaint Analysis

The system analyzes complaints and extracts:

* Category
* Priority
* Sentiment
* Summary

Example:

```text
Category: Refund & Order Cancellation
Priority: High
Sentiment: Negative
```

---

### 2. Retrieval-Augmented Generation

The application uses company knowledge stored as text documents.

Knowledge sources include:

* Refund policy
* Cancellation policy
* Customer support guidelines

The documents are:

1. Loaded using LangChain
2. Split into chunks
3. Stored in ChromaDB
4. Retrieved based on semantic similarity
5. Passed to the LLM as grounding context

This reduces the risk of unsupported responses and helps the model answer using company-specific information.

---

### 3. Grounded Support Responses

The support generation prompt instructs the model to:

* Use only retrieved company knowledge
* Avoid inventing policies
* Avoid inventing refund timelines
* Avoid unsupported guarantees
* Ask only for necessary information
* Never request passwords, OTPs, CVV numbers, or full card numbers
* Keep responses concise

Example:

```text
Customer:
My payment was deducted but my order was cancelled.
I have not received my refund and it has been 5 days.

AI Response:
Hi there, I’m sorry to hear that you haven’t received your
refund yet. Since the payment was deducted and the order was
cancelled, you’re eligible for a refund, but the processing
time depends on your payment method and bank.

Could you please share your order number and the transaction
ID so we can verify the refund status?
```

---

## Prompt Optimization

Two prompt versions were evaluated.

### Prompt V1

A simple prompt asking the model to be polite and helpful.

### Prompt V2

A structured prompt with explicit requirements around:

* Empathy
* Grounding
* Missing information
* Unsupported claims
* Refund timelines
* Future promises
* Sensitive information

### Evaluation Result

| Metric         |   Prompt V1 |      Prompt V2 |
| -------------- | ----------: | -------------: |
| Overall Score  |       3.0/5 |      **5.0/5** |
| Hallucination  |         Yes |         **No** |
| Latency        |      2.042s |     **0.519s** |
| Estimated Cost | $0.00020798 | **$0.0000489** |

The evaluation demonstrated that better prompt constraints can improve response safety and quality while also reducing response length and cost.

---

## AI Performance Monitoring

The application tracks:

* Prompt tokens
* Completion tokens
* Total tokens
* Response latency
* Estimated generation cost

Example live run:

```text
Latency:          0.589 seconds
Prompt Tokens:    393
Completion:       173
Total Tokens:     566
Estimated Cost:   $0.00008137
```

These metrics make it possible to compare prompt versions not only by response quality but also by operational efficiency.

---

## AI Security Testing

The project includes adversarial tests for:

1. System prompt extraction
2. Developer-mode jailbreak
3. Sensitive payment information requests
4. Safety override attacks

Current test result:

```text
SECURITY SCORE: 4/4
PASS RATE: 100%
```

The tests verify that the model refuses attempts to obtain:

* Hidden system instructions
* Confidential prompts
* Card information
* CVV
* OTPs
* Other restricted information

These tests are a small adversarial evaluation suite and are not intended to represent comprehensive security verification.

---

## Project Structure

```text
ai-support-intelligence/
│
├── backend/
│   ├── main.py
│   ├── knowledge_base.py
│   └── vector_store.py
│
├── frontend/
│   └── index.html
│
├── datasets/
│   └── support_tickets.json
│
├── knowledge_base/
│   ├── refund_policy.txt
│   ├── cancellation_policy.txt
│   └── support_guidelines.txt
│
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py
│   ├── prompt_evaluation.py
│   ├── prompt_comparison.py
│   └── test_metrics.py
│
├── tests/
│   ├── __init__.py
│   ├── prompt_injection_tests.py
│   └── security_evaluation.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn

### Generative AI

* Groq
* `openai/gpt-oss-20b`

### RAG

* LangChain
* ChromaDB
* Semantic retrieval

### Frontend

* HTML
* CSS
* JavaScript

### Evaluation

* Prompt comparison
* LLM-based response evaluation
* Token tracking
* Latency measurement
* Cost estimation
* Security testing

---

## How to Run

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```text
GROQ_API_KEY=your_api_key_here
```

Never commit API keys to GitHub.

### 5. Start the backend

```bash
uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

In a second terminal:

```bash
python -m http.server 5500 --directory frontend
```

Frontend:

```text
http://127.0.0.1:5500
```

---

## Example Workflow

```text
Customer Complaint
        |
        v
Complaint Analysis
        |
        +--> Category
        +--> Priority
        +--> Sentiment
        +--> Summary
        |
        v
Knowledge Retrieval
        |
        v
Grounded Prompt
        |
        v
Groq LLM
        |
        v
Support Response
        |
        +--> Tokens
        +--> Latency
        +--> Estimated Cost
```

---

## Why This Project Matters

A basic chatbot demonstrates that an LLM can generate text.

This project demonstrates a broader GenAI engineering workflow:

```text
Prompt Engineering
        +
RAG
        +
Evaluation
        +
Optimization
        +
Security Testing
        +
Performance Monitoring
        +
API Development
        +
Frontend Integration
```

The focus is not simply on generating an answer, but on measuring whether the answer is:

* Relevant
* Grounded
* Safe
* Efficient
* Cost-effective

---

## Future Improvements

Potential future enhancements include:

* Larger evaluation datasets
* Automated batch evaluation
* Prompt version tracking
* Human feedback collection
* More adversarial security tests
* Authentication and role-based access
* Production vector database
* Streaming responses
* Dashboard analytics
* Automated regression testing
* Model comparison across multiple LLM providers

---

## Author

Built as a Generative AI / Prompt Engineering portfolio project demonstrating practical LLM application development, RAG, evaluation, optimization, and AI security.
