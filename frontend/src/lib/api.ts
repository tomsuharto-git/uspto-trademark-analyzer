/**
 * API client for USPTO backend
 */
import axios from 'axios'
import type {
  AnalysisResponse,
  SearchQuery,
  Trademark
} from './types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds for AI analysis
})

/**
 * Search trademarks in USPTO database
 */
export async function searchTrademarks(
  query: SearchQuery
): Promise<Trademark[]> {
  const response = await api.post<Trademark[]>('/search/', query)
  return response.data
}

/**
 * Get trademark details by serial number
 */
export async function getTrademarkBySerial(
  serialNumber: string
): Promise<Trademark> {
  const response = await api.get<Trademark>(`/search/${serialNumber}`)
  return response.data
}

/**
 * Analyze trademark for risk conflicts
 * Returns AI-powered analysis with risk tiers
 */
export async function analyzeTrademarkRisk(
  query: SearchQuery
): Promise<AnalysisResponse> {
  const response = await api.post<AnalysisResponse>('/analysis/analyze', query)
  return response.data
}

/**
 * Error handler for API calls
 */
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.detail || error.message
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'An unknown error occurred'
}
