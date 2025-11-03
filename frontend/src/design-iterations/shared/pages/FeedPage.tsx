import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Filter, Plus, Sparkles, Clock, User, Tag, TrendingUp } from 'lucide-react'
import { format } from 'date-fns'

import { api } from '@/services/api'
import { useGraphStore } from '@/store/useGraphStore'
import { useUIStore } from '@/store/useUIStore'
import type { ResearchItem } from '@/types'
import { useDesignTheme } from '../ThemeProvider'
import { ThemedButton } from '../components/ThemedButton'
import { ThemedCard } from '../components/ThemedCard'
import { ThemedInput } from '../components/ThemedInput'
import { ThemedBadge } from '../components/ThemedBadge'

export function SharedFeedPage() {
  const theme = useDesignTheme()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [items, setItems] = useState<ResearchItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [hasMore, setHasMore] = useState(true)
  const [page, setPage] = useState(0)

  const { addNotification } = useUIStore()

  useEffect(() => {
    const loadItems = async () => {
      setIsLoading(true)
      try {
        const response = await api.getFeed({ limit: 20, offset: page * 20 })
        setItems(prevItems => page === 0 ? response.data : [...prevItems, ...response.data])
        setHasMore(response.pagination?.has_more || false)
        setIsLoading(false)
      } catch (error: any) {
        setIsLoading(false)
        addNotification({ type: 'error', message: `Failed to load feed: ${error.message}`, duration: 5000 })
      }
    }
    loadItems()
  }, [page, addNotification])

  const filteredItems = items.filter(item =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.summary.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="h-full flex flex-col" style={{ background: `linear-gradient(to bottom, ${theme.colors.neutral[50]}, ${theme.colors.neutral[100]})` }}>
      {/* Header */}
      <div
        className="bg-white"
        style={{
          borderBottom: `1px solid ${theme.colors.neutral[200]}`,
          boxShadow: theme.shadows.sm,
        }}
      >
        <div style={{ padding: `${theme.spacing.lg} ${theme.spacing.xl}` }}>
          <div className="flex items-center justify-between mb-6">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div
                  style={{
                    padding: theme.spacing.sm,
                    borderRadius: theme.borderRadius.md,
                    background: `linear-gradient(135deg, ${theme.colors.primary[500]} 0%, ${theme.colors.primary[700]} 100%)`,
                  }}
                >
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <h1
                  style={{
                    fontSize: theme.typography.fontSize['3xl'],
                    fontWeight: theme.typography.fontWeight.bold,
                    color: theme.colors.neutral[900],
                  }}
                >
                  Research Feed
                </h1>
              </div>
              <p style={{ color: theme.colors.neutral[500], fontSize: theme.typography.fontSize.sm }}>
                Discover and explore the latest insights and research
              </p>
            </div>

            <div className="flex items-center gap-3">
              <ThemedButton variant="secondary" icon={<Filter className="w-4 h-4" />}>
                Filters
              </ThemedButton>
              <ThemedButton
                variant="primary"
                icon={<Plus className="w-4 h-4" />}
                onClick={() => navigate('/add-topics')}
              >
                Add Topics
              </ThemedButton>
            </div>
          </div>

          {/* Search Bar */}
          <div className="max-w-2xl">
            <ThemedInput
              type="search"
              placeholder="Search research items, topics, or entities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              icon={<Search className="w-5 h-5" />}
            />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        {isLoading && page === 0 ? (
          <div className="flex items-center justify-center h-64">
            <div className="flex items-center gap-3">
              <div
                className="animate-spin rounded-full h-8 w-8 border-b-2"
                style={{ borderColor: theme.colors.primary[500] }}
              ></div>
              <span style={{ color: theme.colors.neutral[500] }}>Loading research items...</span>
            </div>
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Search className="w-12 h-12 mx-auto mb-4" style={{ color: theme.colors.neutral[300] }} />
              <h3
                className="text-lg font-semibold mb-2"
                style={{ color: theme.colors.neutral[900] }}
              >
                No research items found
              </h3>
              <p style={{ color: theme.colors.neutral[500], fontSize: theme.typography.fontSize.sm }}>
                {searchQuery ? 'Try adjusting your search terms' : 'Check back later for new insights'}
              </p>
            </div>
          </div>
        ) : (
          <div style={{ padding: `${theme.spacing.lg} ${theme.spacing.xl}` }}>
            <div className="grid gap-6 max-w-4xl mx-auto">
              {filteredItems.map((item) => (
                <ResearchItemCard
                  key={item.id}
                  item={item}
                  onSave={() =>
                    addNotification({ type: 'success', message: 'Saved to collection', duration: 3000 })
                  }
                  onViewInLab={() => navigate('/lab')}
                />
              ))}

              {hasMore && (
                <div className="flex justify-center pt-6">
                  <ThemedButton variant="outline" onClick={() => setPage(prev => prev + 1)}>
                    Load More Items
                  </ThemedButton>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// Research Item Card Component
function ResearchItemCard({
  item,
  onSave,
  onViewInLab,
}: {
  item: ResearchItem
  onSave: () => void
  onViewInLab: () => void
}) {
  const theme = useDesignTheme()

  return (
    <ThemedCard accentBorder="left">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <h3
          className="text-xl font-bold line-clamp-2 flex-1"
          style={{ color: theme.colors.neutral[900] }}
        >
          {item.title}
        </h3>
        <div className="flex gap-2 ml-4">
          <ThemedButton variant="ghost" size="sm" onClick={onSave}>
            <TrendingUp className="w-4 h-4" />
          </ThemedButton>
          <ThemedButton variant="ghost" size="sm" onClick={onViewInLab}>
            <Sparkles className="w-4 h-4" />
          </ThemedButton>
        </div>
      </div>

      {/* Metadata */}
      <div
        className="flex flex-wrap items-center gap-4 mb-4"
        style={{ fontSize: theme.typography.fontSize.sm, color: theme.colors.neutral[500] }}
      >
        <div className="flex items-center gap-1.5">
          <Clock className="w-4 h-4" />
          <span>{format(new Date(item.published_at), 'MMM d, yyyy')}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <User className="w-4 h-4" />
          <span>AI Generated</span>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <div
              className="w-2 h-2 rounded-full"
              style={{ background: theme.colors.accent[500] }}
            ></div>
            <span style={{ fontWeight: theme.typography.fontWeight.medium }}>
              Quality: {Math.round(item.quality_score * 100)}%
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <div
              className="w-2 h-2 rounded-full"
              style={{ background: theme.colors.primary[500] }}
            ></div>
            <span style={{ fontWeight: theme.typography.fontWeight.medium }}>
              Relevance: {Math.round(item.relevance_score * 100)}%
            </span>
          </div>
        </div>
      </div>

      {/* Summary */}
      <p
        className="mb-4 line-clamp-2"
        style={{
          color: theme.colors.neutral[600],
          fontSize: theme.typography.fontSize.sm,
          lineHeight: 1.6,
        }}
      >
        {item.summary}
      </p>

      {/* Tags */}
      <div className="flex flex-wrap gap-2 mb-4">
        {item.entity_tags.slice(0, 3).map((tag) => (
          <ThemedBadge key={tag} variant="primary" icon={<Tag className="w-3 h-3" />}>
            {tag.replace('_', ' ')}
          </ThemedBadge>
        ))}
        {item.topics.slice(0, 2).map((topic) => (
          <ThemedBadge key={topic} variant="accent">
            {topic}
          </ThemedBadge>
        ))}
        {item.entity_tags.length > 3 && (
          <ThemedBadge variant="neutral">+{item.entity_tags.length - 3} more</ThemedBadge>
        )}
      </div>

      {/* Footer */}
      <div className="flex justify-between items-center">
        <ThemedBadge
          variant={
            item.content_type === 'alert'
              ? 'error'
              : item.content_type === 'insight'
              ? 'primary'
              : 'warning'
          }
        >
          {item.content_type.toUpperCase()}
        </ThemedBadge>
        <span style={{ fontSize: theme.typography.fontSize.xs, color: theme.colors.neutral[400] }}>
          Updated {format(new Date(item.updated_at), 'MMM d')}
        </span>
      </div>
    </ThemedCard>
  )
}

