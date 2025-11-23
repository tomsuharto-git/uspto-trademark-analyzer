/**
 * TypeScript types for USPTO Trademark Risk Analyzer
 */

export type RiskLevel = 'critical' | 'high' | 'medium' | 'low'

export type TrademarkStatus =
  | 'registered'
  | 'pending'
  | 'abandoned'
  | 'cancelled'
  | 'expired'
  | 'unknown'

export interface Trademark {
  serial_number: string
  registration_number?: string
  mark_text: string
  owner_name: string
  status: TrademarkStatus
  status_date?: string
  filing_date?: string
  registration_date?: string
  international_classes: string[]
  goods_services_description?: string
  mark_type?: string
  attorney_name?: string
  correspondence_address?: string
  mark_image_url?: string
}

export interface RiskFactors {
  similarity_score: number
  class_overlap_score: number
  status_strength_score: number
  use_commerce_score: number
}

export interface TrademarkRiskAnalysis {
  serial_number: string
  mark_text: string
  owner_name: string
  risk_score: number
  risk_level: RiskLevel
  risk_factors: RiskFactors
  risk_explanation: string
  conflict_reason: string
  recommendations: string[]
  goods_services_description?: string
  international_classes?: string[]
  status?: TrademarkStatus
  filing_date?: string
  registration_date?: string
}

export interface SearchResultsSummary {
  query: string
  total_results: number
  overall_risk_level: RiskLevel
  risk_distribution: {
    critical: number
    high: number
    medium: number
    low: number
  }
  key_findings: string[]
  recommendations: string[]
  summary: string
  estimated_timeline?: string
  suggested_next_steps: string[]
}

export interface RiskTierResults {
  critical: TrademarkRiskAnalysis[]
  high: TrademarkRiskAnalysis[]
  medium: TrademarkRiskAnalysis[]
  low: TrademarkRiskAnalysis[]
}

export interface AnalysisResponse {
  query: string
  summary: SearchResultsSummary
  results_by_tier: RiskTierResults
  total_analyzed: number
  processing_time_seconds: number
}

export interface SearchQuery {
  query: string
  search_type?: 'text' | 'serial' | 'owner'
  limit?: number
  classes?: string[]
}
