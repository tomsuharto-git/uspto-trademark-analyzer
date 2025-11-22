# USPTO Trademark Risk Analyzer - Frontend

Next.js frontend for the trademark risk analysis tool.

## Features

- **Clean Search Interface**: Professional, distraction-free search experience
- **AI Summary**: TL;DR analysis with risk level and recommendations
- **Risk-Tiered Results**: Results organized by CRITICAL/HIGH/MEDIUM/LOW
- **Interactive Cards**: Expandable trademark cards with detailed breakdowns
- **Responsive Design**: Mobile-friendly, works on all screen sizes
- **Real-time Analysis**: Live feedback during search and analysis

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local`:

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx          # Main search page
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Global styles
│   ├── components/
│   │   ├── ResultsSummary.tsx    # AI summary display
│   │   ├── RiskTierSection.tsx   # Risk tier group
│   │   ├── TrademarkCard.tsx     # Individual result card
│   │   └── RiskBadge.tsx         # Risk level badge
│   └── lib/
│       ├── api.ts            # API client
│       └── types.ts          # TypeScript types
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## Design System

### Colors

- **Critical Risk**: Red (#DC2626)
- **High Risk**: Orange (#EA580C)
- **Medium Risk**: Yellow (#CA8A04)
- **Low Risk**: Green (#16A34A)
- **Primary**: Blue (#1E40AF)

### Typography

- **Font Family**: Inter (headings & body), JetBrains Mono (monospace data)
- **Weights**: 300-800 range for hierarchy
- **Sizing**: Responsive, mobile-first

### Components

All components follow a clean, professional aesthetic:
- Card-based layouts with subtle shadows
- Risk color coding throughout
- Smooth animations and transitions
- Clear visual hierarchy

## Available Scripts

```bash
# Development server with hot reload
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## API Integration

The frontend communicates with the FastAPI backend via REST endpoints:

```typescript
// Search and analyze trademark
const results = await analyzeTrademarkRisk({
  query: 'ACME',
  search_type: 'text',
  limit: 50,
})
```

## User Flow

1. **Landing**: Clean search interface with examples
2. **Search**: User enters trademark name
3. **Loading**: Visual feedback while searching and analyzing
4. **Results**:
   - AI Summary at top (TL;DR)
   - Risk-tiered results below
   - Expandable cards for details

## Customization

### Changing Colors

Edit `tailwind.config.ts`:

```typescript
colors: {
  risk: {
    critical: '#YOUR_COLOR',
    // ...
  }
}
```

### Adding Features

Component locations:
- Search interface: `src/app/page.tsx`
- Summary display: `src/components/ResultsSummary.tsx`
- Result cards: `src/components/TrademarkCard.tsx`

## Building for Production

```bash
# Create optimized production build
npm run build

# Test production build locally
npm start
```

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Environment Variables

Set in deployment platform:

```
NEXT_PUBLIC_API_URL=https://your-api-domain.com/api/v1
```

## Troubleshooting

### "Cannot connect to backend"

- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure backend is running on correct port
- Verify CORS settings in backend

### Styling issues

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Performance

- Code splitting with Next.js
- Lazy loading of components
- Optimized images and fonts
- Fast initial page load
- Smooth animations (60fps)

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance (WCAG AA)
- Screen reader friendly

## License

TBD
