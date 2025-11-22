'use client'

import { useState } from 'react'
import { Search, AlertCircle } from 'lucide-react'
import { analyzeTrademarkRisk, getErrorMessage } from '@/lib/api'
import type { AnalysisResponse } from '@/lib/types'
import ResultsSummary from '@/components/ResultsSummary'
import RiskTierSection from '@/components/RiskTierSection'

export default function Home() {
  const [query, setQuery] = useState('')
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
      })
      setResults(analysisResults)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            USPTO Trademark Risk Analyzer
          </h1>
          <p className="mt-2 text-gray-600">
            AI-powered conflict analysis for trademark clearance
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Search Section */}
        <div className="mb-12">
          <form onSubmit={handleSearch} className="max-w-3xl mx-auto">
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter trademark name to analyze..."
                className="w-full px-6 py-4 pr-32 text-lg border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-blue-100 transition-all"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading}
                className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2.5 bg-primary text-white rounded-lg font-semibold hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
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

            {/* Search Tips */}
            {!results && !loading && (
              <div className="mt-4 text-sm text-gray-500 text-center">
                <p>
                  Examples: <button
                    type="button"
                    onClick={() => setQuery('ACME')}
                    className="text-primary hover:underline mx-1"
                  >
                    ACME
                  </button>
                  •
                  <button
                    type="button"
                    onClick={() => setQuery('TECH PRO')}
                    className="text-primary hover:underline mx-1"
                  >
                    TECH PRO
                  </button>
                  •
                  <button
                    type="button"
                    onClick={() => setQuery('WIDGET')}
                    className="text-primary hover:underline mx-1"
                  >
                    WIDGET
                  </button>
                </p>
              </div>
            )}
          </form>

          {/* Error Display */}
          {error && (
            <div className="max-w-3xl mx-auto mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3 animate-fade-in">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-red-900">Error</p>
                <p className="text-red-700 text-sm mt-1">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="max-w-4xl mx-auto text-center py-12 animate-fade-in">
            <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <p className="text-lg font-semibold text-gray-700">Searching USPTO database...</p>
            <p className="text-gray-500 mt-2">Analyzing results with AI...</p>
          </div>
        )}

        {/* Results Section */}
        {results && !loading && (
          <div className="space-y-8 animate-slide-up">
            {/* AI Summary */}
            <ResultsSummary summary={results.summary} />

            {/* Risk Tier Results */}
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900">
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

        {/* Welcome State */}
        {!results && !loading && !error && (
          <div className="max-w-2xl mx-auto text-center py-12">
            <div className="w-20 h-20 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Search className="w-10 h-10 text-primary" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Ready to analyze your trademark?
            </h2>
            <p className="text-gray-600 mb-8">
              Enter a trademark name above to search the USPTO database and receive
              AI-powered risk analysis with actionable recommendations.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-left">
              <div className="p-4 bg-white rounded-lg border border-gray-200">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-3">
                  <span className="text-2xl">🔍</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">Search USPTO</h3>
                <p className="text-sm text-gray-600">
                  Search millions of trademarks in the USPTO database
                </p>
              </div>
              <div className="p-4 bg-white rounded-lg border border-gray-200">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mb-3">
                  <span className="text-2xl">🤖</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">AI Analysis</h3>
                <p className="text-sm text-gray-600">
                  Get intelligent risk assessment powered by Claude
                </p>
              </div>
              <div className="p-4 bg-white rounded-lg border border-gray-200">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-3">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">Clear Results</h3>
                <p className="text-sm text-gray-600">
                  Results organized by risk level with recommendations
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
