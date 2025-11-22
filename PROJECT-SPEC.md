# USPTO Trademark Search - AI Risk Analysis Tool

## Product Vision

A web application that searches the USPTO trademark database and provides AI-powered risk analysis for trademark conflicts, with clear visual results tiered by risk level.

## Core Features

### 1. Search Interface
- Clean, professional search bar
- Query by trademark name, serial number, or keywords
- Advanced filters (status, class, owner)

### 2. AI-Powered Results Analysis
**Above Results: TL;DR Summary**
- Overall risk assessment (LOW/MEDIUM/HIGH/CRITICAL)
- Key findings and potential conflicts
- Actionable recommendations
- Estimated timeline/next steps

**Results Display: Risk-Tiered**
- **CRITICAL** (Red): Direct matches, high conflict probability
- **HIGH** (Orange): Similar marks in same class
- **MEDIUM** (Yellow): Phonetic/visual similarity
- **LOW** (Green): Distant similarity, different classes

### 3. Individual Result Cards
Each trademark result shows:
- Mark text/image
- Serial/registration number
- Owner information
- Status (live, dead, pending)
- International class
- Filing/registration date
- AI risk explanation (why this is flagged)

### 4. Visual Design
- Risk level color coding throughout
- Clear information hierarchy
- Responsive design (mobile-friendly)
- Professional, distinctive aesthetic (not generic AI look)

## Technical Architecture

### Tech Stack

**Backend:**
- Python 3.11+
- FastAPI (fast, modern, great API docs)
- USPTO API integration (TSDR)
- Claude API for risk analysis
- SQLite (development) → PostgreSQL (production)

**Frontend:**
- Next.js 14+ (React)
- TypeScript
- Tailwind CSS (custom theme)
- shadcn/ui components (customized)

**Deployment:**
- Vercel (frontend)
- Railway/Render (backend)
- Environment variables for API keys

### Project Structure

```
trademark-risk-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── search.py    # Search endpoints
│   │   │   │   └── analysis.py  # Risk analysis endpoints
│   │   ├── services/
│   │   │   ├── uspto.py         # USPTO API client
│   │   │   ├── ai_analyzer.py   # Claude API integration
│   │   │   └── risk_scorer.py   # Risk calculation logic
│   │   ├── models/
│   │   │   ├── trademark.py     # Data models
│   │   │   └── risk.py
│   │   └── config.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx         # Home/search page
│   │   │   ├── results/
│   │   │   │   └── page.tsx     # Results page
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── SearchBar.tsx
│   │   │   ├── ResultsSummary.tsx
│   │   │   ├── RiskTierSection.tsx
│   │   │   ├── TrademarkCard.tsx
│   │   │   └── RiskBadge.tsx
│   │   ├── lib/
│   │   │   ├── api.ts           # Backend API client
│   │   │   └── types.ts
│   │   └── styles/
│   ├── package.json
│   └── tailwind.config.ts
│
├── README.md
└── .gitignore
```

## API Key Information

**USPTO API Key:** `szbcdzcfpygkhqpzigiuoqapzfgiay`

**Rate Limits:**
- Patent File Wrapper: 1,200,000/week
- Metadata Retrievals: 5,000,000/week

**Required Environment Variables:**
```
USPTO_API_KEY=szbcdzcfpygkhqpzigiuoqapzfgiay
ANTHROPIC_API_KEY=<your-claude-api-key>
```

## AI Risk Analysis Logic

### Risk Factors Analyzed

1. **Similarity Score (40% weight)**
   - Text similarity (Levenshtein distance)
   - Phonetic similarity (Soundex/Metaphone)
   - Visual similarity (for logos)

2. **Class Overlap (30% weight)**
   - Same international class = higher risk
   - Related classes = medium risk
   - Different industries = lower risk

3. **Status & Strength (20% weight)**
   - Live registered marks = highest risk
   - Pending applications = medium risk
   - Dead/abandoned = lower risk
   - Famous marks = elevated risk

4. **Use & Commerce (10% weight)**
   - Active use in commerce
   - Geographic overlap
   - Market presence

### Risk Tiers

**CRITICAL (90-100)**
- Identical or near-identical mark
- Same international class
- Currently in use/registered
- Strong brand presence

**HIGH (70-89)**
- High similarity score
- Same or related class
- Active trademark
- Potential confusion likely

**MEDIUM (40-69)**
- Moderate similarity
- Related goods/services
- Some conflict potential
- Further research needed

**LOW (0-39)**
- Low similarity
- Different classes
- Minimal conflict risk
- Proceed with caution

## User Experience Flow

1. **Landing Page**
   - Clean search interface
   - Example searches
   - Quick explanation of risk analysis

2. **Search Action**
   - Loading state with progress
   - "Searching USPTO database..."
   - "Analyzing results with AI..."

3. **Results Page**
   - **Top Section:** AI Summary
     - Risk level badge
     - Key findings (3-5 bullets)
     - Recommendations
   - **Middle Section:** Results by Risk Tier
     - CRITICAL section (if any)
     - HIGH section
     - MEDIUM section
     - LOW section (collapsible)
   - **Individual Cards:** Detailed trademark info

4. **Interaction**
   - Click card to expand details
   - Export results (PDF/JSON)
   - Save search
   - Share results

## Design Principles

### Typography
- Headings: **Inter** (700-800 weight) - clean, professional
- Body: **Inter** (400-500 weight)
- Mono/Data: **JetBrains Mono** for serial numbers, dates

### Color System
```css
--critical: #DC2626 (red-600)
--high: #EA580C (orange-600)
--medium: #CA8A04 (yellow-600)
--low: #16A34A (green-600)
--primary: #1E40AF (blue-700)
--background: #F9FAFB (gray-50)
--card: #FFFFFF
--text: #111827 (gray-900)
```

### Visual Elements
- Risk level color bars on cards
- Gradient backgrounds (subtle)
- Smooth animations on state changes
- Clear iconography (search, alert, check)

## MVP Features (Phase 1)

- [ ] Basic trademark search by name
- [ ] USPTO API integration
- [ ] AI risk analysis with Claude
- [ ] Results display with risk tiers
- [ ] TL;DR summary
- [ ] Individual result cards
- [ ] Responsive design

## Future Enhancements (Phase 2+)

- [ ] User accounts & saved searches
- [ ] Search history
- [ ] Export results (PDF)
- [ ] Bulk search (CSV upload)
- [ ] Email alerts for status changes
- [ ] Advanced filtering
- [ ] Image-based search
- [ ] Phonetic search
- [ ] API for developers

## Success Metrics

- Search results accuracy
- AI analysis relevance
- User trust in risk scores
- Time saved vs manual search
- User satisfaction (surveys)

## Development Timeline

**Week 1:** Setup & Backend
- Project structure
- USPTO API integration
- Basic search functionality
- Data models

**Week 2:** AI Integration
- Claude API setup
- Risk scoring logic
- Analysis engine
- Testing & tuning

**Week 3:** Frontend Development
- Next.js setup
- Search interface
- Results display
- Risk tier components

**Week 4:** Polish & Deploy
- Design refinement
- Error handling
- Performance optimization
- Deployment & testing

## Notes

- Start simple: text search → expand to advanced features
- Focus on UX: clear, actionable insights
- Trust signals: show sources, methodology
- Mobile-first design
- Fast response times (< 3s for results)
