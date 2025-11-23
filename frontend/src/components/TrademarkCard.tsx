'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { ChevronDown, ChevronUp, FileText, Building2, Calendar, ExternalLink } from 'lucide-react'
import type { TrademarkRiskAnalysis } from '@/lib/types'
import RiskBadge from './RiskBadge'

interface TrademarkCardProps {
  analysis: TrademarkRiskAnalysis
  query: string
}

export default function TrademarkCard({ analysis }: TrademarkCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const router = useRouter()

  return (
    <div className="bg-[#2a2a2a] rounded-lg border-2 border-gray-700 shadow-sm hover:shadow-md transition-shadow">
      {/* Main Card Content */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 text-left hover:bg-black/5 transition-colors"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            {/* Trademark Name */}
            <div className="flex items-center gap-3 mb-2">
              <h4 className="text-lg font-display font-bold text-gray-100 truncate">
                {analysis.mark_text}
              </h4>
              <RiskBadge level={analysis.risk_level} size="small" />
            </div>

            {/* Owner Name */}
            <div className="flex items-center gap-2 mb-2 text-sm text-gray-400">
              <Building2 className="w-3.5 h-3.5" />
              <span className="truncate">{analysis.owner_name}</span>
            </div>

            {/* Risk Score */}
            <div className="flex items-center gap-4 mb-2">
              <div className="flex items-center gap-2">
                <div className="text-sm font-semibold text-gray-400">Risk Score:</div>
                <div className={`text-2xl font-bold text-risk-${analysis.risk_level}`}>
                  {Math.round(analysis.risk_score)}
                </div>
                <div className="text-sm text-gray-500">/100</div>
              </div>
            </div>

            {/* Conflict Reason */}
            <p className="text-sm text-gray-300 line-clamp-2">
              {analysis.conflict_reason}
            </p>

            {/* Serial Number */}
            <div className="mt-2 flex items-center gap-2 text-xs font-mono text-gray-400">
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
        <div className="px-4 pb-4 space-y-4 border-t border-gray-700">
          {/* Risk Factors Breakdown */}
          <div className="pt-4">
            <h5 className="text-sm font-display font-bold text-gray-100 mb-3">Risk Factors</h5>
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

          {/* Goods & Services */}
          {analysis.goods_services_description && (
            <div>
              <h5 className="text-sm font-display font-bold text-gray-100 mb-2">Goods & Services</h5>
              <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
                {analysis.goods_services_description}
              </p>
            </div>
          )}

          {/* International Classes */}
          {analysis.international_classes && analysis.international_classes.length > 0 && (
            <div>
              <h5 className="text-sm font-display font-bold text-gray-100 mb-2">International Classes</h5>
              <div className="flex flex-wrap gap-2">
                {analysis.international_classes.map((cls) => (
                  <span
                    key={cls}
                    className="px-2 py-1 text-xs font-mono bg-blue-500/20 text-blue-300 rounded border border-blue-500/30"
                  >
                    {cls}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Detailed Explanation */}
          <div>
            <h5 className="text-sm font-display font-bold text-gray-100 mb-2">Why This is Flagged</h5>
            <p className="text-sm text-gray-300 leading-relaxed">
              {analysis.risk_explanation}
            </p>
          </div>

          {/* Recommendations */}
          {analysis.recommendations.length > 0 && (
            <div>
              <h5 className="text-sm font-display font-bold text-gray-100 mb-2">Recommendations</h5>
              <ul className="space-y-1">
                {analysis.recommendations.map((rec, i) => (
                  <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                    <span className="text-blue-400 mt-0.5">•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* View Full Details Button */}
          <div className="pt-4 border-t border-gray-700">
            <button
              onClick={(e) => {
                e.stopPropagation()
                router.push(`/trademark/${analysis.serial_number}`)
              }}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center justify-center gap-2 font-medium"
            >
              <ExternalLink className="w-4 h-4" />
              View Full Details
            </button>
          </div>
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
        <span className="font-medium text-gray-300">{label}</span>
        <span className="font-mono text-gray-400">{Math.round(score)}%</span>
      </div>
      <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
        <div
          className={`h-full bg-risk-${color} transition-all duration-500`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  )
}
