import { X, ExternalLink, Tag, Calendar, User, Building, DollarSign, MapPin } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { Badge } from '@/components/Common/Badge'
import type { Entity, EntityRelationship } from '@/types'

interface NodeDetailsPanelProps {
  entity: Entity | null
  relationships: EntityRelationship[]
  onClose?: () => void
  className?: string
}

export function NodeDetailsPanel({
  entity,
  relationships,
  onClose,
  className = '',
}: NodeDetailsPanelProps) {
  if (!entity) {
    return (
      <div className={`p-4 text-center text-muted-foreground ${className}`}>
        <div className="text-4xl mb-2">🎯</div>
        <p>Select a node to view details</p>
      </div>
    )
  }

  const getEntityIcon = (type: string) => {
    switch (type) {
      case 'organization':
        return <Building className="w-4 h-4" />
      case 'person':
        return <User className="w-4 h-4" />
      case 'funding_amount':
        return <DollarSign className="w-4 h-4" />
      case 'date':
        return <Calendar className="w-4 h-4" />
      case 'location':
        return <MapPin className="w-4 h-4" />
      default:
        return <Tag className="w-4 h-4" />
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return 'text-green-600 bg-green-50'
    if (confidence >= 0.7) return 'text-blue-600 bg-blue-50'
    if (confidence >= 0.5) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString()
    } catch {
      return dateString
    }
  }

  return (
    <div className={`bg-card border border-border rounded-lg ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              {getEntityIcon(entity.type)}
            </div>
            <div>
              <h3 className="font-semibold text-lg text-foreground">
                {entity.name}
              </h3>
              <div className="flex items-center gap-2 mt-1">
                <Badge variant="outline" className="text-xs">
                  {entity.type.replace('_', ' ')}
                </Badge>
                <span className={`text-xs px-2 py-1 rounded-full ${getConfidenceColor(entity.confidence)}`}>
                  {Math.round(entity.confidence * 100)}% confidence
                </span>
              </div>
            </div>
          </div>

          {onClose && (
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="w-4 h-4" />
            </Button>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-4 space-y-4">
        {/* Metadata */}
        {entity.metadata && Object.keys(entity.metadata).length > 0 && (
          <div>
            <h4 className="font-medium text-sm text-foreground mb-2">Details</h4>
            <div className="space-y-2">
              {Object.entries(entity.metadata).map(([key, value]) => (
                <div key={key} className="flex justify-between text-sm">
                  <span className="text-muted-foreground capitalize">
                    {key.replace('_', ' ')}:
                  </span>
                  <span className="text-foreground">
                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Source Information */}
        <div>
          <h4 className="font-medium text-sm text-foreground mb-2">Source</h4>
          <div className="text-sm text-muted-foreground">
            <p>Extracted from: {entity.source}</p>
            <p>Method: {entity.extraction_method}</p>
            <p>Created: {formatDate(entity.created_at)}</p>
          </div>
        </div>

        {/* Relationships */}
        {relationships.length > 0 && (
          <div>
            <h4 className="font-medium text-sm text-foreground mb-2">
              Relationships ({relationships.length})
            </h4>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {relationships.map((relationship) => (
                <div
                  key={relationship.id}
                  className="p-2 bg-muted/50 rounded border border-border"
                >
                  <div className="flex items-center justify-between mb-1">
                    <Badge variant="outline" className="text-xs">
                      {relationship.relationship_type}
                    </Badge>
                    <span className={`text-xs px-1 py-0.5 rounded ${getConfidenceColor(relationship.confidence)}`}>
                      {Math.round(relationship.confidence * 100)}%
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {relationship.evidence}
                  </p>
                  {relationship.temporal_context && (
                    <div className="text-xs text-muted-foreground mt-1">
                      {relationship.temporal_context.start_date && (
                        <span>From: {formatDate(relationship.temporal_context.start_date)}</span>
                      )}
                      {relationship.temporal_context.end_date && (
                        <span> To: {formatDate(relationship.temporal_context.end_date)}</span>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="pt-2 border-t border-border">
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="flex-1">
              <ExternalLink className="w-3 h-3 mr-1" />
              View Source
            </Button>
            <Button variant="outline" size="sm" className="flex-1">
              Add to Collection
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}