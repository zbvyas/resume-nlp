# resume-nlp

samples of tika extractions for testing purposes

## setup virtual environment
```bash
python -m venv .venv
source source nlp/bin/activate
pip install -r requirements.txt
```

## run extractions
```bash
python extractions.py -f /path/to/resume
```

## API
```bash
fastapi dev main.py # fastapi dev will start with auto-reload enabled for local development

# Serving at: http://localhost:8000
# API docs: http://localhost:8000/docs
```