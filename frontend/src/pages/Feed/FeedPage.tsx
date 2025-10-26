import { useEffect, useState } from 'react'
import { Search, Filter, Plus } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { Input } from '@/components/Common/Input'
import { ResearchItemCard } from '@/components/Feed/ResearchItemCard'
import { useGraphStore } from '@/store/useGraphStore'
import { useUIStore } from '@/store/useUIStore'
import type { ResearchItem } from '@/types'

export function FeedPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [items, setItems] = useState<ResearchItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [hasMore, setHasMore] = useState(true)
  const [page, setPage] = useState(0)

  const { addNotification } = useUIStore()
  const { addEntity } = useGraphStore()

  // Mock data for demonstration
  const mockItems: ResearchItem[] = [
    {
      id: '1',
      title: 'AI Breakthrough in Entity Recognition',
      summary: 'New research shows 95% accuracy in extracting complex entity relationships from unstructured text, revolutionizing knowledge graph construction.',
      content_type: 'article',
      quality_score: 0.95,
      relevance_score: 0.92,
      entity_tags: ['artificial_intelligence', 'entity_recognition', 'knowledge_graphs'],
      topics: ['AI', 'Machine Learning', 'NLP'],
      published_at: '2025-01-23T10:00:00Z',
      created_at: '2025-01-23T09:00:00Z',
      updated_at: '2025-01-23T09:00:00Z',
      created_by: 'ai_system',
      is_active: true,
    },
    {
      id: '2',
      title: 'Creator Economy Investment Trends 2025',
      summary: 'Analysis of $2.3B in creator economy investments shows growing focus on AI-powered content creation and distribution platforms.',
      content_type: 'insight',
      quality_score: 0.88,
      relevance_score: 0.85,
      entity_tags: ['creator_economy', 'investment', 'ai_content'],
      topics: ['Finance', 'Investment', 'Creator Economy'],
      published_at: '2025-01-23T08:30:00Z',
      created_at: '2025-01-23T08:00:00Z',
      updated_at: '2025-01-23T08:00:00Z',
      created_by: 'ai_system',
      is_active: true,
    },
    {
      id: '3',
      title: 'Multi-Language Entity Extraction Advances',
      summary: 'Recent developments in cross-lingual entity recognition achieve 87% accuracy across English, Spanish, French, and Chinese datasets.',
      content_type: 'article',
      quality_score: 0.91,
      relevance_score: 0.89,
      entity_tags: ['multilingual', 'entity_extraction', 'nlp'],
      topics: ['AI', 'Natural Language Processing', 'International'],
      published_at: '2025-01-23T07:15:00Z',
      created_at: '2025-01-23T07:00:00Z',
      updated_at: '2025-01-23T07:00:00Z',
      created_by: 'ai_system',
      is_active: true,
    },
  ]

  useEffect(() => {
    // Simulate API call to fetch feed items
    const loadItems = async () => {
      setIsLoading(true)
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000))

      setItems(mockItems)
      setIsLoading(false)
    }

    loadItems()
  }, [])

  const handleSaveItem = (itemId: string) => {
    addNotification({
      type: 'success',
      message: 'Research item saved to your collection',
      duration: 3000,
    })
  }

  const handleViewInLab = (item: ResearchItem) => {
    // Navigate to graph lab with item context
    addNotification({
      type: 'info',
      message: 'Opening in Graph Lab...',
      duration: 2000,
    })

    // Extract entities from item and add to graph store
    item.entity_tags.forEach(tag => {
      addEntity({
        id: `entity_${tag}`,
        name: tag.replace('_', ' '),
        type: 'concept',
        confidence: 0.8,
        source: item.id,
        source_type: 'research_item',
        extraction_method: 'automatic',
        metadata: { from_item: item.title },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_active: true,
      })
    })
  }

  const handleLoadMore = () => {
    setPage(prev => prev + 1)
    // Simulate loading more items
    setTimeout(() => {
      setHasMore(false)
    }, 500)
  }

  const filteredItems = items.filter(item =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.topics.some(topic => topic.toLowerCase().includes(searchQuery.toLowerCase()))
  )

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-border p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Research Feed</h1>
            <p className="text-muted-foreground">
              Discover and explore the latest insights and research
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Filter className="w-4 h-4 mr-2" />
              Filters
            </Button>
            <Button size="sm">
              <Plus className="w-4 h-4 mr-2" />
              New Research
            </Button>
          </div>
        </div>

        {/* Search */}
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
          <Input
            placeholder="Search research items, topics, or entities..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <span className="ml-3 text-muted-foreground">Loading research items...</span>
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Search className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium text-foreground mb-2">
                No research items found
              </h3>
              <p className="text-muted-foreground">
                {searchQuery ? 'Try adjusting your search terms' : 'Check back later for new insights'}
              </p>
            </div>
          </div>
        ) : (
          <div className="p-6">
            <div className="grid gap-6 max-w-4xl mx-auto">
              {filteredItems.map((item) => (
                <ResearchItemCard
                  key={item.id}
                  item={item}
                  onSave={() => handleSaveItem(item.id)}
                  onViewInLab={() => handleViewInLab(item)}
                  onShare={() => {
                    addNotification({
                      type: 'success',
                      message: 'Research item shared successfully',
                      duration: 3000,
                    })
                  }}
                />
              ))}

              {hasMore && (
                <div className="flex justify-center pt-6">
                  <Button onClick={handleLoadMore} variant="outline">
                    Load More Items
                  </Button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
