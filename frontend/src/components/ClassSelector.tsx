'use client'

import { useState } from 'react'
import { ChevronDown, ChevronUp, Package, Briefcase, Search } from 'lucide-react'
import { TRADEMARK_CLASSES } from '@/lib/trademark-classes'

interface ClassSelectorProps {
  selectedClasses: string[]
  onChange: (classes: string[]) => void
}

export default function ClassSelector({ selectedClasses, onChange }: ClassSelectorProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [showGoods, setShowGoods] = useState(true)
  const [showServices, setShowServices] = useState(true)

  const toggleClass = (classNumber: string) => {
    if (selectedClasses.includes(classNumber)) {
      onChange(selectedClasses.filter(c => c !== classNumber))
    } else {
      onChange([...selectedClasses, classNumber])
    }
  }

  const clearAll = () => {
    onChange([])
  }

  // Get all classes and filter by type toggles and search query
  const filteredClasses = TRADEMARK_CLASSES.filter((classItem) => {
    // Filter by type toggles
    if (!showGoods && classItem.type === 'goods') return false
    if (!showServices && classItem.type === 'services') return false

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      return classItem.number.includes(query) || classItem.description.toLowerCase().includes(query)
    }

    return true
  })

  return (
    <div className="mt-4">
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 text-sm text-gray-400 hover:text-blue-400 font-medium transition-colors"
      >
        {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        <span>
          Specify International Classes (Optional)
          {selectedClasses.length > 0 && (
            <span className="ml-2 px-2 py-0.5 bg-blue-500/20 text-blue-400 rounded-full text-xs font-semibold">
              {selectedClasses.length} selected
            </span>
          )}
        </span>
      </button>

      {isExpanded && (
        <div className="mt-4 p-4 bg-[#2a2a2a] border border-gray-700 rounded-lg animate-fade-in">
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm text-gray-400">
              Select the classes your trademark will be used in for more accurate risk assessment
            </p>
            {selectedClasses.length > 0 && (
              <button
                type="button"
                onClick={clearAll}
                className="text-sm text-red-400 hover:text-red-300 font-medium"
              >
                Clear all
              </button>
            )}
          </div>

          {/* Filter and Search Row */}
          <div className="flex flex-col sm:flex-row gap-3 mb-4">
            {/* Search Box */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search classes by number or description..."
                className="w-full pl-10 pr-4 py-2 bg-[#222222] border border-gray-700 text-gray-200 placeholder-gray-500 rounded-lg focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400/20 transition-all text-sm"
              />
            </div>

            {/* Type Filters */}
            <div className="flex gap-3">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showGoods}
                  onChange={(e) => setShowGoods(e.target.checked)}
                  className="w-4 h-4 rounded border-gray-600 bg-[#222222] text-blue-500 focus:ring-2 focus:ring-blue-400/20 focus:ring-offset-0"
                />
                <span className="flex items-center gap-1.5 text-sm font-medium text-gray-300">
                  <Package className="w-4 h-4" />
                  Goods (1-34)
                </span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showServices}
                  onChange={(e) => setShowServices(e.target.checked)}
                  className="w-4 h-4 rounded border-gray-600 bg-[#222222] text-blue-500 focus:ring-2 focus:ring-blue-400/20 focus:ring-offset-0"
                />
                <span className="flex items-center gap-1.5 text-sm font-medium text-gray-300">
                  <Briefcase className="w-4 h-4" />
                  Services (35-45)
                </span>
              </label>
            </div>
          </div>

          {/* Class Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-h-96 overflow-y-auto custom-scrollbar">
            {filteredClasses.length === 0 ? (
              <div className="col-span-2 text-center py-8 text-gray-400">
                {searchQuery.trim()
                  ? `No classes found matching "${searchQuery}"`
                  : 'Select at least one type filter (Goods or Services)'}
              </div>
            ) : (
              filteredClasses.map((classItem) => {
                const isSelected = selectedClasses.includes(classItem.number)
                return (
                  <button
                    key={classItem.number}
                    type="button"
                    onClick={() => toggleClass(classItem.number)}
                    className={`text-left p-3 rounded-lg border-2 transition-all ${
                      isSelected
                        ? 'border-blue-500 bg-blue-500/10'
                        : 'border-gray-700 bg-[#222222] hover:border-gray-600 hover:bg-[#252525]'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      <div
                        className={`flex-shrink-0 w-5 h-5 rounded border-2 mt-0.5 flex items-center justify-center ${
                          isSelected
                            ? 'border-blue-500 bg-blue-500'
                            : 'border-gray-600 bg-transparent'
                        }`}
                      >
                        {isSelected && (
                          <svg
                            className="w-3 h-3 text-white"
                            fill="none"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="3"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold text-gray-200">
                          Class {classItem.number}
                        </div>
                        <div className="text-xs text-gray-400 mt-0.5 line-clamp-2">
                          {classItem.description}
                        </div>
                      </div>
                    </div>
                  </button>
                )
              })
            )}
          </div>
        </div>
      )}
    </div>
  )
}
