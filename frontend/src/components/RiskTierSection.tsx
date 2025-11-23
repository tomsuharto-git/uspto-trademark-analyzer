import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'
import type { TrademarkRiskAnalysis, RiskLevel } from '@/lib/types'
import TrademarkCard from './TrademarkCard'

interface RiskTierSectionProps {
  title: string
  riskLevel: RiskLevel
  results: TrademarkRiskAnalysis[]
  query: string
  defaultCollapsed?: boolean
}

export default function RiskTierSection({
  title,
  riskLevel,
  results,
  query,
  defaultCollapsed = false,
}: RiskTierSectionProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed)

  if (results.length === 0) return null

  return (
    <div className={`rounded-xl border-2 overflow-hidden risk-gradient-${riskLevel}`}>
      {/* Section Header */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-black/5 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className={`w-1 h-8 rounded-full bg-risk-${riskLevel}`} />
          <div className="text-left">
            <h3 className="text-lg font-display font-bold text-gray-100">{title}</h3>
            <p className="text-sm text-gray-600">
              {results.length} trademark{results.length !== 1 ? 's' : ''} found
            </p>
          </div>
        </div>
        {isCollapsed ? (
          <ChevronDown className="w-5 h-5 text-gray-600" />
        ) : (
          <ChevronUp className="w-5 h-5 text-gray-600" />
        )}
      </button>

      {/* Results Grid */}
      {!isCollapsed && (
        <div className="p-4 space-y-3">
          {results.map((result) => (
            <TrademarkCard
              key={result.serial_number}
              analysis={result}
              query={query}
            />
          ))}
        </div>
      )}
    </div>
  )
}
