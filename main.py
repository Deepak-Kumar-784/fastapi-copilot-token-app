# main.py
"""
FastAPI app for:
- generating pseudorandom tokens derived from input text
- returning an MD5 checksum of the input text
- serving an interactive HTML page to call the API
Includes Pydantic models, endpoint docstrings, and comments for clarity.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import hashlib
import secrets
import os
from typing import List

app = FastAPI(
    title="Improvise Python App (Copilot)",
    description="Demo FastAPI app that generates pseudorandom tokens and checksums. Built with GitHub Copilot.",
    version="1.0.0",
)

# Templates directory
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


# ---------------------------
# Pydantic models
# ---------------------------
# Copilot hint: generate a Pydantic model named `GenerateRequest` with a single field `text: str`.
class TextOnly(BaseModel):
    text: str


class GenerateRequest(BaseModel):
    """Request model for the `/generate` endpoint."""

    text: str


class ChecksumResponse(BaseModel):
    text: str
    checksum: str


class TokensResponse(BaseModel):
    tokens: List[str]
    checksum: str


# ---------------------------
# Helper functions
# ---------------------------
def _checksum_md5(text: str) -> str:
    """Return the MD5 checksum (hex) of the given text."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _generate_tokens_from_text(text: str, count: int = 5) -> List[str]:
    """Generate `count` pseudorandom tokens derived from the input text."""
    tokens = []
    for i in range(count):
        salt = secrets.token_hex(8)
        token = hashlib.sha256(f"{text}-{i}-{salt}".encode("utf-8")).hexdigest()
        tokens.append(token)
    return tokens


def generate(text: str, count: int = 5) -> TokensResponse:
    """Public generate function that returns tokens and checksum for given text.

    This wrapper is intentionally small so it can be used by an endpoint
    (and by tests) to produce the same output as `_generate_tokens_from_text`.
    """
    checksum = _checksum_md5(text)
    tokens = _generate_tokens_from_text(text, count=count)
    return TokensResponse(tokens=tokens, checksum=checksum)


# ---------------------------
# Routes / Endpoints
# ---------------------------
@app.get("/", summary="Welcome route")
def welcome():
    participant_name = "Deepak Kumar Behera"
    return {
        "message": f"Welcome to the Improvise Python App — built for {participant_name}"
    }


@app.post(
    "/checksum",
    response_model=ChecksumResponse,
    summary="Compute MD5 checksum of provided text",
)
def checksum_endpoint(body: TextOnly):
    """Compute MD5 checksum for the provided JSON `text` field.

    Uses `ChecksumResponse` as the response model to provide explicit output
    typing and avoid ambiguous response model warnings.
    """
    cs = _checksum_md5(body.text)
    return ChecksumResponse(text=body.text, checksum=cs)


@app.post(
    "/tokens",
    response_model=TokensResponse,
    summary="Generate list of tokens from text",
)
def tokens_endpoint(body: TextOnly):
    """Generate pseudorandom tokens from the provided text.

    This legacy endpoint uses the internal helper function directly.
    """
    checksum = _checksum_md5(body.text)
    tokens = _generate_tokens_from_text(body.text, count=5)
    return TokensResponse(tokens=tokens, checksum=checksum)


# Copilot hint: create a FastAPI endpoint that accepts JSON and returns tokens + checksum.
@app.post(
    "/generate",
    response_model=TokensResponse,
    summary="Generate tokens and checksum from text",
)
def generate_endpoint(body: GenerateRequest):
    """POST endpoint that accepts JSON payload `{"text": "..."}` and returns tokens + checksum.

    This endpoint delegates to the public `generate()` function so business logic
    stays testable and separate from request handling.
    """
    return generate(body.text)


@app.get("/form", response_class=HTMLResponse, summary="Interactive HTML form")
def form_page(request: Request):
    participant_name = "Deepak Kumar Behera"
    return templates.TemplateResponse(
        "form.html",
        {"request": request, "participant": participant_name},
    )


@app.post("/form", response_class=HTMLResponse, summary="Process HTML form submission")
def form_submit(request: Request, text: str = Form(...)):
    """
    Process form submission from form.html.
    Returns the same form page with generated tokens and checksum.
    """
    result = {
        "text": text,
        "checksum": _checksum_md5(text),
        "tokens": _generate_tokens_from_text(text, count=5),
    }
    participant_name = "Deepak Kumar Behera"
    return templates.TemplateResponse(
        "form.html",
        {"request": request, "participant": participant_name, "result": result},
    )
