import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Filter, Plus } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { Input } from '@/components/Common/Input'
import { ResearchItemCard } from '@/components/Feed/ResearchItemCard'
import { useGraphStore } from '@/store/useGraphStore'
import { useUIStore } from '@/store/useUIStore'
import { api } from '@/services/api'
import type { ResearchItem } from '@/types'

export function FeedPage() {
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [items, setItems] = useState<ResearchItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [hasMore, setHasMore] = useState(true)
  const [page, setPage] = useState(0)

  const { addNotification } = useUIStore()
  const { addEntity } = useGraphStore()

  useEffect(() => {
    // Fetch feed items from mock API
    const loadItems = async () => {
      setIsLoading(true)
      try {
        const response = await api.getFeed({ limit: 20, offset: page * 20 })
        setItems(prevItems => page === 0 ? response.data : [...prevItems, ...response.data])
        setHasMore(response.pagination?.has_more || false)
        setIsLoading(false)
        
        console.log(`✓ Loaded ${response.data.length} research items from MSW mock API`)
      } catch (error: any) {
        setIsLoading(false)
        console.error('Failed to load feed:', error)
        addNotification({
          type: 'error',
          message: `Failed to load feed: ${error.message}`,
          duration: 5000,
        })
      }
    }

    loadItems()
  }, [page])

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
            <Button size="sm" onClick={() => navigate('/add-topics')}>
              <Plus className="w-4 h-4 mr-2" />
              Add Topics
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
