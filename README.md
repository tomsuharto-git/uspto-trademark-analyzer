# USPTO Trademark Risk Analyzer

🔍 AI-powered trademark conflict analysis tool with intelligent risk assessment and actionable recommendations.

## Overview

A web application that searches the USPTO trademark database and provides AI-powered risk analysis for potential trademark conflicts. Results are organized by risk level (CRITICAL/HIGH/MEDIUM/LOW) with a comprehensive AI-generated summary and recommendations.

## Features

### 🎯 Core Functionality
- **USPTO Database Search**: Search millions of trademarks via official USPTO APIs
- **AI Risk Analysis**: Claude-powered analysis with multi-factor risk scoring
- **Visual Risk Tiers**: Results organized by CRITICAL, HIGH, MEDIUM, LOW risk
- **TL;DR Summary**: AI-generated summary with key findings and recommendations
- **Detailed Breakdown**: Individual risk factors (similarity, class overlap, status, commerce)

### 🧠 AI Intelligence
- Similarity analysis (text, phonetic, visual)
- International class overlap detection
- Trademark status and strength assessment
- Use in commerce evaluation
- Actionable next steps and timeline estimates

### 🎨 User Experience
- Clean, professional search interface
- Real-time analysis feedback
- Expandable result cards
- Mobile-responsive design
- Distinctive visual design (not generic AI look)

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- USPTO API Key (free at https://data.uspto.gov/myodp)
- Anthropic API Key (for Claude)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd USPTO
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys:
# USPTO_API_KEY=szbcdzcfpygkhqpzigiuoqapzfgiay
# ANTHROPIC_API_KEY=your-claude-key

# Run backend
uvicorn app.main:app --reload --port 8000
```

Backend will be available at http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local if backend URL differs

# Run frontend
npm run dev
```

Frontend will be available at http://localhost:3000

## Usage

1. **Navigate** to http://localhost:3000
2. **Enter** a trademark name in the search box
3. **Click** "Search" to analyze
4. **Review** the AI summary at the top
5. **Explore** risk-tiered results below
6. **Expand** individual cards for detailed risk breakdowns

## Architecture

### Tech Stack

**Backend:**
- FastAPI (Python)
- USPTO TSDR API
- Anthropic Claude API
- Pydantic for data validation

**Frontend:**
- Next.js 14 (React)
- TypeScript
- Tailwind CSS
- Axios for API calls

### Project Structure

```
USPTO/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── api/routes/          # API endpoints
│   │   ├── services/            # Business logic
│   │   │   ├── uspto.py         # USPTO API client
│   │   │   ├── risk_scorer.py   # Risk calculation
│   │   │   └── ai_analyzer.py   # Claude integration
│   │   └── models/              # Data models
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js pages
│   │   ├── components/          # React components
│   │   └── lib/                 # API client, types
│   └── package.json
│
├── PROJECT-SPEC.md              # Detailed specifications
└── README.md                    # This file
```

## Risk Scoring Algorithm

### Multi-Factor Analysis (Weighted)

1. **Similarity (40%)**
   - Levenshtein distance (edit distance)
   - Phonetic matching (Soundex, Metaphone)
   - Substring containment

2. **Class Overlap (30%)**
   - International classification system
   - Related goods/services analysis

3. **Status & Strength (20%)**
   - Registration status (live, pending, dead)
   - Brand strength indicators
   - Time in use

4. **Use in Commerce (10%)**
   - Active commercial use
   - Market presence
   - Geographic scope

### Risk Levels

| Level | Score | Description |
|-------|-------|-------------|
| **CRITICAL** | 90-100 | Identical/near-identical mark, immediate legal review needed |
| **HIGH** | 70-89 | Significant conflicts, attorney consultation strongly advised |
| **MEDIUM** | 40-69 | Potential issues, further research recommended |
| **LOW** | 0-39 | Minimal risk, standard clearance sufficient |

## API Documentation

### Endpoints

**POST** `/api/v1/analysis/analyze`
```json
{
  "query": "ACME WIDGETS",
  "search_type": "text",
  "limit": 50
}
```

Response includes:
- AI-generated summary
- Risk-tiered results
- Individual trademark analyses
- Processing time

See full API docs at: http://localhost:8000/docs

## Screenshots

### Search Interface
Clean, professional search with example queries

### Results Summary
AI-generated TL;DR with risk assessment and recommendations

### Risk Tiers
Results organized by CRITICAL/HIGH/MEDIUM/LOW with visual color coding

### Detail View
Expandable cards showing risk factor breakdowns and specific recommendations

## Environment Variables

### Backend (.env)

```env
USPTO_API_KEY=your-uspto-key
ANTHROPIC_API_KEY=your-claude-key
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Development

### Run Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Code Quality

```bash
# Backend formatting
black app/
isort app/

# Frontend linting
npm run lint
```

## Deployment

### Backend

Deploy to Railway, Render, or similar:
- Python 3.11+
- Install dependencies from requirements.txt
- Set environment variables
- Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Frontend

Deploy to Vercel (recommended):
```bash
vercel
```

Set environment variable:
- `NEXT_PUBLIC_API_URL`: Your backend URL

## Rate Limits

### USPTO API
- Metadata Retrievals: 5,000,000/week
- Patent File Wrapper: 1,200,000/week

### Claude API
- Per your Anthropic plan limits

## Roadmap

### Phase 1 (MVP) ✅
- [x] USPTO API integration
- [x] AI risk analysis
- [x] Risk-tiered results
- [x] Web interface

### Phase 2
- [ ] Real USPTO search API (currently using mock data)
- [ ] User authentication
- [ ] Save searches
- [ ] Export results (PDF/JSON)

### Phase 3
- [ ] Bulk search (CSV upload)
- [ ] Email alerts for status changes
- [ ] Advanced filtering
- [ ] Image-based search
- [ ] Developer API

## Troubleshooting

### Backend won't start

- Verify Python version: `python --version` (3.11+)
- Check virtual environment is activated
- Verify API keys in `.env`

### Frontend can't connect

- Check backend is running on port 8000
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend

### No results returned

- Verify USPTO API key is valid
- Check network connectivity
- Review backend logs for errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

TBD

## Support

For issues or questions:
- Check documentation in PROJECT-SPEC.md
- Review backend/README.md and frontend/README.md
- File an issue on GitHub

---

Built with ❤️ using FastAPI, Next.js, and Claude AI
