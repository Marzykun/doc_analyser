import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None

# Load backend/.env so GEMINI_API_KEY is available even if not exported in shell.
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)

_model = None
_configured_key = None
_configured_model_name = None


def _pick_fallback_model() -> str | None:
    """Pick an available model that supports generateContent."""
    preferred = (
        "models/gemini-2.5-flash",
        "models/gemini-2.0-flash",
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-flash",
        "models/gemini-pro",
    )
    available = []
    for m in genai.list_models():
        methods = getattr(m, "supported_generation_methods", []) or []
        if "generateContent" in methods:
            available.append(getattr(m, "name", ""))

    for name in preferred:
        if name in available:
            return name
    return next((name for name in available if "gemini" in name), None)


def _get_model():
    global _model, _configured_key, _configured_model_name
    if genai is None:
        return None, "google-generativeai package is not installed"

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, "GEMINI_API_KEY is not set"

    requested_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    if (
        _model is None
        or _configured_key != api_key
        or _configured_model_name != requested_model
    ):
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel(requested_model)
        _configured_key = api_key
        _configured_model_name = requested_model

    return _model, None


def safe_parse(text):
    if not text:
        return {
            "error": "Invalid JSON from Gemini",
            "raw": text
        }

    cleaned = text.strip()

    # Remove markdown code fences like ```json ... ```
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    # If extra text surrounds JSON, keep the outermost JSON object candidate.
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        cleaned = cleaned[first_brace:last_brace + 1]

    try:
        return json.loads(cleaned)
    except Exception:
        return {
            "error": "Invalid JSON from Gemini",
            "raw": text
        }


def analyze_contract(text):
    model, init_error = _get_model()
    if init_error:
        return {
            "error": "Gemini is not configured",
            "details": init_error
        }

    prompt = f"""
You are a contract analysis expert.

Analyze the contract below and return ONLY valid JSON.

Tasks:
1. Give a short summary (max 5 lines)
2. List risks (clear and practical)
3. Explain important clauses in simple English

Focus on:
- Termination
- Payment
- Liability

Contract:
{text}

Output format:
{{
  "summary": "...",
  "risks": ["...", "..."],
  "clauses_explained": [
    {{
      "clause": "Termination",
      "explanation": "..."
    }},
    {{
      "clause": "Payment",
      "explanation": "..."
    }},
    {{
      "clause": "Liability",
      "explanation": "..."
    }}
  ]
}}
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "max_output_tokens": 4096,
                "temperature": 0.2,
            },
        )
        return safe_parse(response.text)

    except Exception as e:
        msg = str(e)
        # Auto-recover when configured model no longer exists.
        if "not found" in msg.lower() and genai is not None:
            try:
                fallback = _pick_fallback_model()
                if fallback:
                    response = genai.GenerativeModel(fallback).generate_content(prompt)
                    parsed = safe_parse(response.text)
                    if isinstance(parsed, dict):
                        parsed.setdefault("_model_used", fallback)
                    return parsed
            except Exception as fallback_error:
                return {
                    "error": "Gemini API failed",
                    "details": f"{msg}; fallback failed: {str(fallback_error)}"
                }

        return {
            "error": "Gemini API failed",
            "details": msg
        }
