import React from 'react'
import { format } from 'date-fns'
import { Save, Share2, Eye, Tag, Clock, User } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { Badge } from '@/components/Common/Badge'
import type { ResearchItem } from '@/types'

interface ResearchItemCardProps {
  item: ResearchItem
  onSave?: () => void
  onViewInLab?: () => void
  onShare?: () => void
  className?: string
}

export function ResearchItemCard({
  item,
  onSave,
  onViewInLab,
  onShare,
  className = '',
}: ResearchItemCardProps) {
  const handleSave = (e: React.MouseEvent) => {
    e.stopPropagation()
    onSave?.()
  }

  const handleViewInLab = (e: React.MouseEvent) => {
    e.stopPropagation()
    onViewInLab?.()
  }

  const handleShare = (e: React.MouseEvent) => {
    e.stopPropagation()
    onShare?.()
  }

  return (
    <article className={`bg-card border border-border rounded-lg p-6 hover:shadow-md transition-shadow ${className}`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-foreground mb-2 line-clamp-2">
            {item.title}
          </h3>

          {/* Metadata */}
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              <span>{format(new Date(item.published_at), 'MMM d, yyyy')}</span>
            </div>

            <div className="flex items-center gap-1">
              <User className="w-4 h-4" />
              <span>AI Generated</span>
            </div>

            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full bg-green-500"></div>
                <span className="text-xs">
                  Quality: {Math.round(item.quality_score * 100)}%
                </span>
              </div>

              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                <span className="text-xs">
                  Relevance: {Math.round(item.relevance_score * 100)}%
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleSave}
            title="Save to collection"
          >
            <Save className="w-4 h-4" />
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={handleViewInLab}
            title="View in Graph Lab"
          >
            <Eye className="w-4 h-4" />
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={handleShare}
            title="Share"
          >
            <Share2 className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Summary */}
      <div className="mb-4">
        <p className="text-muted-foreground line-clamp-3">
          {item.summary}
        </p>
      </div>

      {/* Tags and Topics */}
      <div className="flex flex-wrap gap-2 mb-4">
        {/* Entity Tags */}
        {item.entity_tags.slice(0, 3).map((tag) => (
          <Badge key={tag} variant="secondary" className="text-xs">
            <Tag className="w-3 h-3 mr-1" />
            {tag.replace('_', ' ')}
          </Badge>
        ))}

        {/* Topics */}
        {item.topics.slice(0, 2).map((topic) => (
          <Badge key={topic} variant="outline" className="text-xs">
            {topic}
          </Badge>
        ))}

        {item.entity_tags.length > 3 && (
          <Badge variant="outline" className="text-xs">
            +{item.entity_tags.length - 3} more
          </Badge>
        )}
      </div>

      {/* Content Type Badge */}
      <div className="flex justify-between items-center">
        <Badge
          variant={
            item.content_type === 'alert' ? 'destructive' :
            item.content_type === 'insight' ? 'default' : 'secondary'
          }
          className="text-xs"
        >
          {item.content_type.charAt(0).toUpperCase() + item.content_type.slice(1)}
        </Badge>

        <span className="text-xs text-muted-foreground">
          Updated {format(new Date(item.updated_at), 'MMM d')}
        </span>
      </div>
    </article>
  )
}