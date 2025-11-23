'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft, Building2, Calendar, FileText, Info, Loader2 } from 'lucide-react'
import type { Trademark } from '@/lib/types'

export default function TrademarkDetailPage() {
  const params = useParams()
  const router = useRouter()
  const serialNumber = params.serialNumber as string

  const [trademark, setTrademark] = useState<Trademark | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchTrademarkDetails() {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/trademark/${serialNumber}`
        )

        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('Trademark not found')
          }
          throw new Error('Failed to fetch trademark details')
        }

        const data = await response.json()
        setTrademark(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred')
      } finally {
        setLoading(false)
      }
    }

    if (serialNumber) {
      fetchTrademarkDetails()
    }
  }, [serialNumber])

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1a1a1a] flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-400 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading trademark details...</p>
        </div>
      </div>
    )
  }

  if (error || !trademark) {
    return (
      <div className="min-h-screen bg-[#1a1a1a] flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-red-400 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-100 mb-2">Error</h1>
          <p className="text-gray-400 mb-6">{error || 'Trademark not found'}</p>
          <button
            onClick={() => router.back()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#1a1a1a] py-8 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header with Back Button */}
        <button
          onClick={() => router.back()}
          className="flex items-center gap-2 text-gray-400 hover:text-gray-200 transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Results</span>
        </button>

        {/* Main Content */}
        <div className="bg-[#2a2a2a] rounded-lg border-2 border-gray-700 p-8">
          {/* Trademark Name */}
          <div className="mb-8">
            <h1 className="text-4xl font-display font-bold text-gray-100 mb-2">
              {trademark.mark_text}
            </h1>
            <div className="flex items-center gap-2 text-gray-400">
              <FileText className="w-4 h-4" />
              <span className="font-mono text-sm">Serial: {trademark.serial_number}</span>
              {trademark.registration_number && (
                <>
                  <span className="mx-2">•</span>
                  <span className="font-mono text-sm">Reg: {trademark.registration_number}</span>
                </>
              )}
            </div>
          </div>

          {/* Status Badge */}
          <div className="mb-8">
            <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${
              trademark.status === 'registered'
                ? 'bg-green-500/20 text-green-300 border border-green-500/30'
                : trademark.status === 'pending'
                ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30'
                : 'bg-gray-500/20 text-gray-300 border border-gray-500/30'
            }`}>
              {trademark.status.toUpperCase()}
            </span>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-8">
            {/* Owner Information */}
            <div>
              <h3 className="text-sm font-display font-bold text-gray-400 mb-3 flex items-center gap-2">
                <Building2 className="w-4 h-4" />
                Owner Information
              </h3>
              <div className="space-y-3 text-gray-200">
                <div>
                  <div className="text-sm text-gray-500">Owner Name</div>
                  <div className="font-medium">{trademark.owner_name}</div>
                </div>
                {trademark.attorney_name && (
                  <div>
                    <div className="text-sm text-gray-500">Attorney</div>
                    <div className="font-medium">{trademark.attorney_name}</div>
                  </div>
                )}
                {trademark.correspondence_address && (
                  <div>
                    <div className="text-sm text-gray-500">Correspondence Address</div>
                    <div className="font-medium text-sm">{trademark.correspondence_address}</div>
                  </div>
                )}
              </div>
            </div>

            {/* Dates */}
            <div>
              <h3 className="text-sm font-display font-bold text-gray-400 mb-3 flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                Important Dates
              </h3>
              <div className="space-y-3 text-gray-200">
                {trademark.filing_date && (
                  <div>
                    <div className="text-sm text-gray-500">Filing Date</div>
                    <div className="font-medium">{new Date(trademark.filing_date).toLocaleDateString()}</div>
                  </div>
                )}
                {trademark.registration_date && (
                  <div>
                    <div className="text-sm text-gray-500">Registration Date</div>
                    <div className="font-medium">{new Date(trademark.registration_date).toLocaleDateString()}</div>
                  </div>
                )}
                {trademark.status_date && (
                  <div>
                    <div className="text-sm text-gray-500">Status Date</div>
                    <div className="font-medium">{new Date(trademark.status_date).toLocaleDateString()}</div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* International Classes */}
          {trademark.international_classes && trademark.international_classes.length > 0 && (
            <div className="mb-8">
              <h3 className="text-sm font-display font-bold text-gray-400 mb-3 flex items-center gap-2">
                <Info className="w-4 h-4" />
                International Classes
              </h3>
              <div className="flex flex-wrap gap-2">
                {trademark.international_classes.map((cls) => (
                  <span
                    key={cls}
                    className="px-3 py-1 text-sm font-mono bg-blue-500/20 text-blue-300 rounded border border-blue-500/30"
                  >
                    Class {cls}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Goods & Services Description */}
          {trademark.goods_services_description && (
            <div className="mb-8">
              <h3 className="text-sm font-display font-bold text-gray-400 mb-3">
                Goods & Services Description
              </h3>
              <div className="bg-[#1a1a1a] rounded-lg p-4 border border-gray-700">
                <p className="text-gray-300 leading-relaxed whitespace-pre-wrap">
                  {trademark.goods_services_description}
                </p>
              </div>
            </div>
          )}

          {/* Mark Type */}
          {trademark.mark_type && (
            <div>
              <h3 className="text-sm font-display font-bold text-gray-400 mb-3">
                Mark Type
              </h3>
              <p className="text-gray-200 capitalize">{trademark.mark_type}</p>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="mt-6 flex gap-4">
          <a
            href={`https://tsdr.uspto.gov/#caseNumber=${serialNumber}&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch`}
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            View on USPTO.gov
          </a>
          <button
            onClick={() => router.back()}
            className="px-6 py-3 bg-gray-700 text-gray-200 rounded-lg hover:bg-gray-600 transition-colors font-medium"
          >
            Back to Results
          </button>
        </div>
      </div>
    </div>
  )
}
