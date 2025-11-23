'use client'

import { useState } from 'react'
import { Search, AlertCircle } from 'lucide-react'
import { analyzeTrademarkRisk, getErrorMessage } from '@/lib/api'
import type { AnalysisResponse } from '@/lib/types'
import ResultsSummary from '@/components/ResultsSummary'
import RiskTierSection from '@/components/RiskTierSection'
import ClassSelector from '@/components/ClassSelector'

export default function Home() {
  const [query, setQuery] = useState('')
  const [selectedClasses, setSelectedClasses] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<AnalysisResponse | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!query.trim()) {
      setError('Please enter a trademark name to search')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const analysisResults = await analyzeTrademarkRisk({
        query: query.trim(),
        search_type: 'text',
        limit: 50,
        classes: selectedClasses.length > 0 ? selectedClasses : undefined,
      })
      setResults(analysisResults)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-[#1a1a1a]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Logo/Title Section */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-display font-bold text-blue-400 mb-2">
            Clearance
          </h1>
          <p className="text-lg text-blue-300/70">
            USPTO Trademark Risk Analyzer
          </p>
        </div>

        {/* Search Section */}
        <div className="mb-12">
          <form onSubmit={handleSearch} className="max-w-3xl mx-auto">
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter trademark name to analyze..."
                className="w-full px-6 py-4 pr-32 text-lg bg-[#2a2a2a] border-2 border-gray-700 text-gray-200 placeholder-gray-500 rounded-xl focus:border-blue-400 focus:outline-none focus:ring-4 focus:ring-blue-400/20 transition-all"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading}
                className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2.5 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    Search
                  </>
                )}
              </button>
            </div>

            {/* Class Selector */}
            <ClassSelector
              selectedClasses={selectedClasses}
              onChange={setSelectedClasses}
            />
          </form>

          {/* Error Display */}
          {error && (
            <div className="max-w-3xl mx-auto mt-6 p-4 bg-red-900/20 border border-red-700/50 rounded-lg flex items-start gap-3 animate-fade-in">
              <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-red-300">Error</p>
                <p className="text-red-400 text-sm mt-1">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="max-w-4xl mx-auto text-center py-12 animate-fade-in">
            <div className="w-16 h-16 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <p className="text-lg font-semibold text-blue-300">Searching USPTO database...</p>
            <p className="text-gray-400 mt-2">Analyzing results with AI...</p>
          </div>
        )}

        {/* Results Section */}
        {results && !loading && (
          <div className="space-y-8 animate-slide-up">
            {/* AI Summary */}
            <ResultsSummary summary={results.summary} />

            {/* Risk Tier Results */}
            <div className="space-y-6">
              <h2 className="text-2xl font-display font-bold text-blue-300">
                Search Results ({results.total_analyzed} trademarks analyzed)
              </h2>

              {results.results_by_tier.critical.length > 0 && (
                <RiskTierSection
                  title="Critical Risk"
                  riskLevel="critical"
                  results={results.results_by_tier.critical}
                  query={results.query}
                />
              )}

              {results.results_by_tier.high.length > 0 && (
                <RiskTierSection
                  title="High Risk"
                  riskLevel="high"
                  results={results.results_by_tier.high}
                  query={results.query}
                />
              )}

              {results.results_by_tier.medium.length > 0 && (
                <RiskTierSection
                  title="Medium Risk"
                  riskLevel="medium"
                  results={results.results_by_tier.medium}
                  query={results.query}
                />
              )}

              {results.results_by_tier.low.length > 0 && (
                <RiskTierSection
                  title="Low Risk"
                  riskLevel="low"
                  results={results.results_by_tier.low}
                  query={results.query}
                  defaultCollapsed
                />
              )}
            </div>

            {/* Processing Time */}
            <div className="text-center text-sm text-gray-500">
              Analysis completed in {results.processing_time_seconds}s
            </div>
          </div>
        )}

      </div>
    </main>
  )
}
