import { AlertTriangle, CheckCircle2, AlertCircle, Info } from 'lucide-react'
import type { SearchResultsSummary, RiskLevel } from '@/lib/types'
import RiskBadge from './RiskBadge'

interface ResultsSummaryProps {
  summary: SearchResultsSummary
}

const riskIcons: Record<RiskLevel, typeof AlertTriangle> = {
  critical: AlertTriangle,
  high: AlertCircle,
  medium: AlertCircle,
  low: CheckCircle2,
}

export default function ResultsSummary({ summary }: ResultsSummaryProps) {
  const RiskIcon = riskIcons[summary.overall_risk_level]

  return (
    <div className="bg-white rounded-2xl border-2 border-gray-200 shadow-lg overflow-hidden">
      {/* Header with Risk Level */}
      <div className={`px-6 py-4 border-b-2 border-gray-200 risk-gradient-${summary.overall_risk_level}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <RiskIcon className={`w-6 h-6 text-risk-${summary.overall_risk_level}`} />
            <h2 className="text-xl font-bold text-gray-900">Analysis Summary</h2>
          </div>
          <RiskBadge level={summary.overall_risk_level} size="large" />
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-6">
        {/* AI Summary Text */}
        <div className="prose max-w-none">
          <p className="text-gray-700 text-lg leading-relaxed">{summary.summary}</p>
        </div>

        {/* Risk Distribution */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {Object.entries(summary.risk_distribution).map(([level, count]) => (
            <div
              key={level}
              className={`p-3 rounded-lg border-2 risk-gradient-${level}`}
            >
              <div className={`text-2xl font-bold text-risk-${level}`}>{count}</div>
              <div className="text-sm font-semibold text-gray-700 capitalize mt-1">
                {level}
              </div>
            </div>
          ))}
        </div>

        {/* Key Findings */}
        {summary.key_findings.length > 0 && (
          <div>
            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wide mb-3">
              Key Findings
            </h3>
            <ul className="space-y-2">
              {summary.key_findings.map((finding, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-primary mt-1.5">•</span>
                  <span className="text-gray-700">{finding}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {summary.recommendations.length > 0 && (
          <div>
            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wide mb-3">
              Recommendations
            </h3>
            <ul className="space-y-2">
              {summary.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Next Steps */}
        {summary.suggested_next_steps.length > 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="text-sm font-bold text-blue-900 uppercase tracking-wide mb-3 flex items-center gap-2">
              <Info className="w-4 h-4" />
              Suggested Next Steps
            </h3>
            <ol className="space-y-2 list-decimal list-inside">
              {summary.suggested_next_steps.map((step, i) => (
                <li key={i} className="text-blue-900">
                  <span className="text-blue-800">{step}</span>
                </li>
              ))}
            </ol>
            {summary.estimated_timeline && (
              <p className="mt-3 text-sm text-blue-700">
                <strong>Timeline:</strong> {summary.estimated_timeline}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
