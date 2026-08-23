# Smart Expense Tracker

A self-hosted expense-tracking application that extracts structured expense
information from paper receipt images.

## Initial MVP

The first working pipeline will be:

```text
Receipt Image
    ↓
PaddleOCR
    ↓
Ollama
    ↓
Structured JSON
    ↓
PostgreSQL