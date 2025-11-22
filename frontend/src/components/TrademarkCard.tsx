import { useState } from 'react'
import { ChevronDown, ChevronUp, FileText, Building2, Calendar } from 'lucide-react'
import type { TrademarkRiskAnalysis } from '@/lib/types'
import RiskBadge from './RiskBadge'

interface TrademarkCardProps {
  analysis: TrademarkRiskAnalysis
  query: string
}

export default function TrademarkCard({ analysis }: TrademarkCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      {/* Main Card Content */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 text-left hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            {/* Trademark Name */}
            <div className="flex items-center gap-3 mb-2">
              <h4 className="text-lg font-bold text-gray-900 truncate">
                {analysis.mark_text}
              </h4>
              <RiskBadge level={analysis.risk_level} size="small" />
            </div>

            {/* Risk Score */}
            <div className="flex items-center gap-4 mb-2">
              <div className="flex items-center gap-2">
                <div className="text-sm font-semibold text-gray-500">Risk Score:</div>
                <div className={`text-2xl font-bold text-risk-${analysis.risk_level}`}>
                  {Math.round(analysis.risk_score)}
                </div>
                <div className="text-sm text-gray-500">/100</div>
              </div>
            </div>

            {/* Conflict Reason */}
            <p className="text-sm text-gray-600 line-clamp-2">
              {analysis.conflict_reason}
            </p>

            {/* Serial Number */}
            <div className="mt-2 flex items-center gap-2 text-xs font-mono text-gray-500">
              <FileText className="w-3 h-3" />
              {analysis.serial_number}
            </div>
          </div>

          {/* Expand Icon */}
          <div className="flex-shrink-0">
            {isExpanded ? (
              <ChevronUp className="w-5 h-5 text-gray-400" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-400" />
            )}
          </div>
        </div>
      </button>

      {/* Expanded Details */}
      {isExpanded && (
        <div className="px-4 pb-4 space-y-4 border-t border-gray-100">
          {/* Risk Factors Breakdown */}
          <div className="pt-4">
            <h5 className="text-sm font-bold text-gray-900 mb-3">Risk Factors</h5>
            <div className="space-y-2">
              <RiskFactorBar
                label="Similarity"
                score={analysis.risk_factors.similarity_score}
                color={analysis.risk_level}
              />
              <RiskFactorBar
                label="Class Overlap"
                score={analysis.risk_factors.class_overlap_score}
                color={analysis.risk_level}
              />
              <RiskFactorBar
                label="Status & Strength"
                score={analysis.risk_factors.status_strength_score}
                color={analysis.risk_level}
              />
              <RiskFactorBar
                label="Use in Commerce"
                score={analysis.risk_factors.use_commerce_score}
                color={analysis.risk_level}
              />
            </div>
          </div>

          {/* Detailed Explanation */}
          <div>
            <h5 className="text-sm font-bold text-gray-900 mb-2">Why This is Flagged</h5>
            <p className="text-sm text-gray-700 leading-relaxed">
              {analysis.risk_explanation}
            </p>
          </div>

          {/* Recommendations */}
          {analysis.recommendations.length > 0 && (
            <div>
              <h5 className="text-sm font-bold text-gray-900 mb-2">Recommendations</h5>
              <ul className="space-y-1">
                {analysis.recommendations.map((rec, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-primary mt-0.5">•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function RiskFactorBar({
  label,
  score,
  color,
}: {
  label: string
  score: number
  color: string
}) {
  return (
    <div>
      <div className="flex items-center justify-between text-xs mb-1">
        <span className="font-medium text-gray-700">{label}</span>
        <span className="font-mono text-gray-500">{Math.round(score)}%</span>
      </div>
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full bg-risk-${color} transition-all duration-500`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  )
}
