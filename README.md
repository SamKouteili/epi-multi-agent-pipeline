---
title: EPI Proxy Discovery Pipeline
emoji: "\U0001F30D"
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---

# EPI Proxy Discovery Pipeline

Multi-agent system for discovering and validating data proxies for the
[Yale Environmental Performance Index](https://epi.yale.edu/) (EPI).

## Quick Start (local)

```bash
pip install -e .
pip install gradio

# Set API keys
export ANTHROPIC_API_KEY=...
export GEMINI_API_KEY=...

# Launch web UI
python web/app.py
# → opens at http://localhost:7860

# Or run via CLI
python -m src -i WRR
```

## Architecture

1. **Stage 1 — Deep Research Agent**: Gemini Deep Research + Claude structured
   extraction generates proxy hypotheses for a given EPI indicator.
2. **Stage 2 — Code Agent**: Claude Code SDK agent downloads data, runs statistical
   tests (correlation, partial correlation, functional form), and outputs verified
   results.

## Deployment (Hugging Face Spaces)

1. Create a Space at `huggingface.co/new-space` with **Docker** SDK.
2. Add secrets in Space settings: `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`.
3. Push:
   ```bash
   git remote add hf https://huggingface.co/spaces/<user>/epi-proxy-discovery
   git push hf main
   ```
