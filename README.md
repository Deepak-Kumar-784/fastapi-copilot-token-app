# Improvise Python App (GitHub Copilot Exercise)

A simple FastAPI-based web application that demonstrates generating pseudorandom tokens and MD5 checksums from user-provided text. This project was built as an exercise using GitHub Copilot.

## Features

- **Token Generation**: Generate 5 pseudorandom tokens derived from input text using SHA-256 hashing.
- **Checksum Calculation**: Compute MD5 checksums for input text.
- **Interactive Web Form**: User-friendly HTML form for easy interaction.
- **API Endpoints**: RESTful API with OpenAPI documentation.
- **Testing**: Comprehensive pytest test suite.

## Workspace Structure

```
01-improvise-python-app-copilot/
├── main.py                    # FastAPI application with API endpoints
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── test_main.py              # Unit tests using pytest
├── __pycache__/              # Python bytecode cache (auto-generated)
└── templates/
    └── form.html             # HTML template for the interactive form
```

### File Descriptions

- `main.py` — FastAPI application with API endpoints
- `templates/form.html` — HTML template for the interactive form
- `test_main.py` — Unit tests using pytest
- `requirements.txt` — Python dependencies

## API Endpoints

- `GET /` — Returns a welcome message
- `POST /checksum` — Accepts JSON `{"text": "..."}` and returns MD5 checksum
- `POST /tokens` — Accepts JSON `{"text": "..."}` and returns 5 pseudorandom tokens and checksum
- `POST /generate` — Accepts JSON `{"text": "..."}` and returns tokens and checksum (delegates to `generate()` function)
- `GET /form` — Serves an interactive HTML form that calls `/tokens` and displays results

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Local Development

1. **Clone the repository** (if not already done):

   ```bash
   git clone <repository-url>
   cd 01-improvise-python-app-copilot
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**:
   - Interactive form: http://localhost:8000/form
   - API documentation (Swagger UI): http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Running Tests

To run the test suite:

```bash
pytest -q
```

Or for more verbose output:

```bash
pytest -v
```

## Usage Examples

### Using the API

**Get checksum:**

```bash
curl -X POST "http://localhost:8000/checksum" \
     -H "Content-Type: application/json" \
     -d '{"text": "hello world"}'
```

**Generate tokens:**

```bash
curl -X POST "http://localhost:8000/tokens" \
     -H "Content-Type: application/json" \
     -d '{"text": "hello world"}'
```

### Using the Web Form

1. Navigate to http://localhost:8000/form
2. Enter text in the textarea
3. Click "Generate tokens"
4. View the results below

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Jinja2**: Templating engine for HTML rendering
- **Pydantic**: Data validation and serialization
- **pytest**: Testing framework

## Contributing

This is an exercise project. Feel free to fork and experiment!

## License

This project is for educational purposes. Check the original repository for licensing information.
