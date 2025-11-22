# USPTO Trademark Risk Analyzer - Backend API

FastAPI backend for AI-powered trademark conflict analysis.

## Features

- **USPTO API Integration**: Search trademark database via TSDR API
- **Risk Scoring**: Multi-factor risk analysis (similarity, class overlap, status, commerce)
- **AI Analysis**: Claude-powered summaries and recommendations
- **Risk Tiers**: Results organized by CRITICAL/HIGH/MEDIUM/LOW risk

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
USPTO_API_KEY=szbcdzcfpygkhqpzigiuoqapzfgiay
ANTHROPIC_API_KEY=your-claude-api-key-here
```

### 3. Run the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --port 8000

# Or use the main script
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Search Trademarks

**POST** `/api/v1/search/`

Search USPTO database for trademarks.

```json
{
  "query": "ACME",
  "search_type": "text",
  "limit": 50
}
```

### Get Trademark Details

**GET** `/api/v1/search/{serial_number}`

Get detailed info for specific trademark.

### Analyze Trademark Risk

**POST** `/api/v1/analysis/analyze`

Comprehensive risk analysis with AI summary.

```json
{
  "query": "ACME WIDGETS",
  "search_type": "text",
  "limit": 50
}
```

**Response:**

```json
{
  "query": "ACME WIDGETS",
  "summary": {
    "overall_risk_level": "high",
    "key_findings": [...],
    "recommendations": [...],
    "summary": "AI-generated overview..."
  },
  "results_by_tier": {
    "critical": [...],
    "high": [...],
    "medium": [...],
    "low": [...]
  },
  "total_analyzed": 25,
  "processing_time_seconds": 3.45
}
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── api/
│   │   └── routes/
│   │       ├── search.py    # Search endpoints
│   │       └── analysis.py  # Analysis endpoints
│   ├── services/
│   │   ├── uspto.py         # USPTO API client
│   │   ├── risk_scorer.py   # Risk calculation
│   │   └── ai_analyzer.py   # Claude integration
│   └── models/
│       ├── trademark.py     # Data models
│       └── risk.py          # Risk models
├── requirements.txt
├── .env
└── README.md
```

## Risk Scoring Algorithm

### Risk Factors (Weighted)

1. **Similarity (40%)**
   - Levenshtein distance
   - Phonetic similarity (Soundex, Metaphone)
   - Substring matching

2. **Class Overlap (30%)**
   - International classification
   - Related goods/services

3. **Status & Strength (20%)**
   - Registered vs pending
   - Active vs abandoned
   - Brand strength indicators

4. **Use in Commerce (10%)**
   - Years in use
   - Market presence
   - Geographic scope

### Risk Levels

- **CRITICAL (90-100)**: Direct conflicts, immediate legal review needed
- **HIGH (70-89)**: Significant conflicts, attorney consultation advised
- **MEDIUM (40-69)**: Potential issues, further research needed
- **LOW (0-39)**: Minimal risk, standard clearance sufficient

## Development

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black app/
isort app/
```

### Type Checking

```bash
mypy app/
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `USPTO_API_KEY` | USPTO Open Data Portal API key | Yes |
| `ANTHROPIC_API_KEY` | Claude API key for AI analysis | Yes |
| `ENVIRONMENT` | development/production | No |
| `DEBUG` | Enable debug mode | No |
| `CORS_ORIGINS` | Allowed CORS origins | No |

## API Rate Limits

- **USPTO**: 5,000,000 metadata retrievals/week
- **Claude**: Per your Anthropic plan

## Troubleshooting

### "Module not found" errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### CORS errors

Add your frontend URL to `CORS_ORIGINS` in `.env`:

```env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### USPTO API errors

- Verify API key in `.env`
- Check rate limits on https://data.uspto.gov/myodp
- Review API documentation at https://developer.uspto.gov/

## Next Steps

- [ ] Integrate real USPTO search API (currently using mock data)
- [ ] Add database caching (PostgreSQL)
- [ ] Implement user authentication
- [ ] Add rate limiting middleware
- [ ] Deploy to production (Railway/Render)

## License

TBD
