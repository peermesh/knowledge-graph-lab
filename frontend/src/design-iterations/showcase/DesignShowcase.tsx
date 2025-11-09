import { useState } from 'react'
import { Palette, ArrowLeft, Eye, Code } from 'lucide-react'
import { Link } from 'react-router-dom'

type IterationId = 'original' | 'v1' | 'v2' | 'v3'
type PageId = 'feed' | 'lab' | 'settings'

const iterations = [
  { id: 'original' as IterationId, name: 'Current Design', color: '#3B82F6' },
  { id: 'v1' as IterationId, name: 'Iteration 1: Modern Research Platform', color: '#4F46E5' },
  { id: 'v2' as IterationId, name: 'Iteration 2: Bold Knowledge Hub', color: '#1E3A8A' },
  { id: 'v3' as IterationId, name: 'Iteration 3: Warm Discovery Space', color: '#10B981' },
]

const pages = [
  { id: 'feed' as PageId, name: 'Feed Page', description: 'Research feed with cards and filters' },
  { id: 'lab' as PageId, name: 'Graph Lab', description: 'Interactive knowledge graph visualization' },
  { id: 'settings' as PageId, name: 'Settings', description: 'Account and preferences management' },
]

export function DesignShowcase() {
  const [selectedIteration, setSelectedIteration] = useState<IterationId>('original')
  const [selectedPage, setSelectedPage] = useState<PageId>('feed')
  const [comparisonMode, setComparisonMode] = useState(false)
  const [compareWith, setCompareWith] = useState<IterationId>('v1')

  const getRouteForIteration = (iteration: IterationId, page: PageId) => {
    if (iteration === 'original') {
      return `/${page === 'lab' ? 'lab' : page}`
    }
    return `/iterations/${iteration}/${page}`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link to="/feed" className="flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors">
                <ArrowLeft className="w-5 h-5" />
                <span className="text-sm font-medium">Back to App</span>
              </Link>
              <div className="h-6 w-px bg-slate-300" />
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg">
                  <Palette className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-slate-900">Design Iterations Showcase</h1>
                  <p className="text-sm text-slate-600">Compare and explore design variations</p>
                </div>
              </div>
            </div>

            <button
              onClick={() => setComparisonMode(!comparisonMode)}
              className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
                comparisonMode
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
              }`}
            >
              {comparisonMode ? 'Single View' : 'Compare Mode'}
            </button>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Iteration Selector */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h2 className="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
              <Palette className="w-4 h-4" />
              Select Design Iteration
            </h2>
            <div className="space-y-2">
              {iterations.map((iteration) => (
                <button
                  key={iteration.id}
                  onClick={() => setSelectedIteration(iteration.id)}
                  className={`w-full text-left px-4 py-3 rounded-lg border-2 transition-all ${
                    selectedIteration === iteration.id
                      ? 'border-indigo-500 bg-indigo-50 shadow-md'
                      : 'border-slate-200 hover:border-slate-300 bg-white'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: iteration.color }}
                    />
                    <span className={`font-medium ${
                      selectedIteration === iteration.id ? 'text-indigo-900' : 'text-slate-700'
                    }`}>
                      {iteration.name}
                    </span>
                  </div>
                </button>
              ))}
            </div>

            {comparisonMode && (
              <div className="mt-6 pt-6 border-t border-slate-200">
                <h3 className="text-sm font-semibold text-slate-700 mb-3">Compare With:</h3>
                <div className="space-y-2">
                  {iterations.filter(it => it.id !== selectedIteration).map((iteration) => (
                    <button
                      key={iteration.id}
                      onClick={() => setCompareWith(iteration.id)}
                      className={`w-full text-left px-4 py-2 rounded-lg border transition-all ${
                        compareWith === iteration.id
                          ? 'border-purple-500 bg-purple-50'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: iteration.color }}
                        />
                        <span className={`text-sm ${
                          compareWith === iteration.id ? 'text-purple-900 font-medium' : 'text-slate-600'
                        }`}>
                          {iteration.name}
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Page Selector */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h2 className="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
              <Eye className="w-4 h-4" />
              Select Page to View
            </h2>
            <div className="space-y-2">
              {pages.map((page) => (
                <button
                  key={page.id}
                  onClick={() => setSelectedPage(page.id)}
                  className={`w-full text-left px-4 py-3 rounded-lg border-2 transition-all ${
                    selectedPage === page.id
                      ? 'border-indigo-500 bg-indigo-50 shadow-md'
                      : 'border-slate-200 hover:border-slate-300 bg-white'
                  }`}
                >
                  <div className="font-medium text-slate-900">{page.name}</div>
                  <div className="text-sm text-slate-600 mt-1">{page.description}</div>
                </button>
              ))}
            </div>

            <div className="mt-6 pt-6 border-t border-slate-200">
              <div className="flex items-start gap-2 text-sm text-slate-600">
                <Code className="w-4 h-4 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-medium text-slate-700 mb-1">Design Specifications</p>
                  <p className="text-xs leading-relaxed">
                    Detailed specs for each iteration are available in the <code className="px-1 py-0.5 bg-slate-100 rounded">design-iterations/specs/</code> directory
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Preview Area */}
        <div className={`grid ${comparisonMode ? 'grid-cols-2' : 'grid-cols-1'} gap-6`}>
          {/* Main Preview */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-slate-200">
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-6 py-4">
              <h3 className="text-white font-semibold">
                {iterations.find(it => it.id === selectedIteration)?.name}
              </h3>
              <p className="text-indigo-100 text-sm">
                {pages.find(p => p.id === selectedPage)?.name}
              </p>
            </div>
            <div className="aspect-video bg-slate-50 border-t border-slate-200 relative">
              <iframe
                src={getRouteForIteration(selectedIteration, selectedPage)}
                className="w-full h-full"
                title={`Preview: ${selectedIteration} - ${selectedPage}`}
              />
              <div className="absolute top-4 right-4">
                <a
                  href={getRouteForIteration(selectedIteration, selectedPage)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-3 py-2 bg-white/90 backdrop-blur-sm rounded-lg shadow-md text-sm font-medium text-slate-700 hover:bg-white transition-colors flex items-center gap-2"
                >
                  <Eye className="w-4 h-4" />
                  Open Full Page
                </a>
              </div>
            </div>
          </div>

          {/* Comparison Preview */}
          {comparisonMode && (
            <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-slate-200">
              <div className="bg-gradient-to-r from-purple-500 to-pink-600 px-6 py-4">
                <h3 className="text-white font-semibold">
                  {iterations.find(it => it.id === compareWith)?.name}
                </h3>
                <p className="text-purple-100 text-sm">
                  {pages.find(p => p.id === selectedPage)?.name}
                </p>
              </div>
              <div className="aspect-video bg-slate-50 border-t border-slate-200 relative">
                <iframe
                  src={getRouteForIteration(compareWith, selectedPage)}
                  className="w-full h-full"
                  title={`Preview: ${compareWith} - ${selectedPage}`}
                />
                <div className="absolute top-4 right-4">
                  <a
                    href={getRouteForIteration(compareWith, selectedPage)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-2 bg-white/90 backdrop-blur-sm rounded-lg shadow-md text-sm font-medium text-slate-700 hover:bg-white transition-colors flex items-center gap-2"
                  >
                    <Eye className="w-4 h-4" />
                    Open Full Page
                  </a>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Info Cards */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 border border-slate-200">
            <h4 className="font-semibold text-slate-900 mb-2">📐 Layout Preserved</h4>
            <p className="text-sm text-slate-600">All iterations maintain the three-panel layout structure</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-slate-200">
            <h4 className="font-semibold text-slate-900 mb-2">⚡ Fully Functional</h4>
            <p className="text-sm text-slate-600">All pages are working implementations, not static mockups</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-slate-200">
            <h4 className="font-semibold text-slate-900 mb-2">🎨 Easy to Implement</h4>
            <p className="text-sm text-slate-600">Pick your favorite and integrate into the main codebase</p>
          </div>
        </div>
      </div>
    </div>
  )
}












