import clsx from 'clsx'
import type { RiskLevel } from '@/lib/types'

interface RiskBadgeProps {
  level: RiskLevel
  size?: 'small' | 'medium' | 'large'
}

const sizeClasses = {
  small: 'px-2 py-1 text-xs',
  medium: 'px-3 py-1.5 text-sm',
  large: 'px-4 py-2 text-base',
}

const colorClasses: Record<RiskLevel, string> = {
  critical: 'bg-red-100 text-red-800 border-red-300',
  high: 'bg-orange-100 text-orange-800 border-orange-300',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  low: 'bg-green-100 text-green-800 border-green-300',
}

export default function RiskBadge({ level, size = 'medium' }: RiskBadgeProps) {
  return (
    <span
      className={clsx(
        'inline-flex items-center font-bold uppercase tracking-wide rounded-lg border-2',
        sizeClasses[size],
        colorClasses[level]
      )}
    >
      {level}
    </span>
  )
}
