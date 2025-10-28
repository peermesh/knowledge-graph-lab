import { useState, useEffect, useRef } from 'react'
import { Heart, X, Plus, Sparkles, Check } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { Badge } from '@/components/Common/Badge'

interface BubbleInterfaceProps {
  onInterestsChange?: (interests: string[]) => void
  className?: string
  initialInterests?: string[]
}

interface Bubble {
  id: string
  text: string
  x: number
  y: number
  liked?: boolean
  disliked?: boolean
  expanded?: boolean
  parentId?: string
  level: number // 0 = main topic, 1 = related, 2 = sub-topic
  subBubbles?: Bubble[]
}

export function BubbleInterface({ 
  onInterestsChange, 
  className = '',
  initialInterests = []
}: BubbleInterfaceProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [bubbles, setBubbles] = useState<Bubble[]>([])
  const [likedInterests, setLikedInterests] = useState<string[]>(initialInterests)
  const [currentSeed, setCurrentSeed] = useState('')
  const [showSeedInput, setShowSeedInput] = useState(true)
  const [isLoadingRelated, setIsLoadingRelated] = useState(false)

  // Mock API service - simulates backend call for related topics
  const fetchRelatedTopics = async (seed: string): Promise<string[]> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Mock data for demonstration - in production this would call:
    // GET /api/related-topics?seed={seed}&count=5
    const mockTopicDatabase: Record<string, string[]> = {
      'ai': ['Machine Learning', 'Neural Networks', 'Deep Learning', 'Computer Vision', 'Natural Language Processing'],
      'artificial intelligence': ['Machine Learning', 'Neural Networks', 'Deep Learning', 'Computer Vision', 'NLP'],
      'machine learning': ['Supervised Learning', 'Unsupervised Learning', 'Reinforcement Learning', 'Neural Networks', 'Model Training'],
      'creator economy': ['Content Creation', 'Monetization', 'Social Media', 'Influencer Marketing', 'Platform Economics'],
      'blockchain': ['Cryptocurrency', 'Smart Contracts', 'DeFi', 'NFTs', 'Web3'],
      'climate': ['Climate Change', 'Renewable Energy', 'Carbon Capture', 'Sustainability', 'Environmental Policy'],
      'health': ['Healthcare', 'Medical Research', 'Wellness', 'Biotechnology', 'Public Health'],
      'finance': ['Investing', 'Cryptocurrency', 'Banking', 'Financial Markets', 'Personal Finance'],
      'education': ['EdTech', 'Online Learning', 'Pedagogy', 'Educational Technology', 'Student Success'],
      'music': ['Music Production', 'Music Theory', 'Genres', 'Music Technology', 'Artist Development'],
    }

    // Find matching topics
    const lowerSeed = seed.toLowerCase()
    for (const [key, topics] of Object.entries(mockTopicDatabase)) {
      if (lowerSeed.includes(key) || key.includes(lowerSeed)) {
        return topics.slice(0, 5)
      }
    }

    // Default topics if no match
    return [
      `${seed} Basics`,
      `${seed} Applications`,
      `${seed} Research`,
      `${seed} Industry Trends`,
      `${seed} Best Practices`,
    ].slice(0, 5)
  }

  useEffect(() => {
    // Notify parent of initial interests
    if (initialInterests.length > 0) {
      onInterestsChange?.(initialInterests)
    }
  }, [])

  const handleSeedSubmit = async () => {
    if (!currentSeed.trim()) return

    setIsLoadingRelated(true)

    try {
      // Fetch related topics from API (mock for now)
      const relatedTopics = await fetchRelatedTopics(currentSeed)

      // Create the main seed bubble in the center
      const mainBubble: Bubble = {
        id: `main-${Date.now()}`,
        text: currentSeed,
        x: 50,
        y: 50,
        level: 0,
        liked: true, // Auto-like the seed topic
      }

      // Create orbiting related bubbles in a circular pattern
      const angleStep = (2 * Math.PI) / relatedTopics.length
      const radius = 25 // percentage of container

      const orbitingBubbles: Bubble[] = relatedTopics.map((topic, index) => {
        const angle = index * angleStep
        const x = 50 + radius * Math.cos(angle)
        const y = 50 + radius * Math.sin(angle)

        return {
          id: `related-${Date.now()}-${index}`,
          text: topic,
          x,
          y,
          level: 1,
          parentId: mainBubble.id,
        }
      })

      // Add seed topic to liked interests
      const newLiked = [...likedInterests, currentSeed]
      setLikedInterests(newLiked)
      onInterestsChange?.(newLiked)

      // Add all bubbles
      setBubbles([mainBubble, ...orbitingBubbles])
      setCurrentSeed('')
      setShowSeedInput(false)
    } catch (error) {
      console.error('Failed to fetch related topics:', error)
    } finally {
      setIsLoadingRelated(false)
    }
  }

  const handleAddAnother = () => {
    setCurrentSeed('')
    setShowSeedInput(true)
  }

  const handleBubbleClick = async (bubble: Bubble, action: 'like' | 'dislike' | 'expand') => {
    if (action === 'like') {
      // Add to liked interests if not already there
      if (!likedInterests.includes(bubble.text)) {
        const newLiked = [...likedInterests, bubble.text]
        setLikedInterests(newLiked)
        onInterestsChange?.(newLiked)
      }

      // Update bubble state
      setBubbles(prev => prev.map(b =>
        b.id === bubble.id ? { ...b, liked: true, disliked: false } : b
      ))
    } else if (action === 'dislike') {
      // Remove from liked interests if it was liked
      if (likedInterests.includes(bubble.text)) {
        const newLiked = likedInterests.filter(i => i !== bubble.text)
        setLikedInterests(newLiked)
        onInterestsChange?.(newLiked)
      }

      // Update bubble state
      setBubbles(prev => prev.map(b =>
        b.id === bubble.id ? { ...b, disliked: true, liked: false } : b
      ))
    } else if (action === 'expand') {
      // Don't expand if already expanded or has sub-bubbles
      const currentBubble = bubbles.find(b => b.id === bubble.id)
      if (currentBubble?.expanded || currentBubble?.subBubbles) {
        // Just toggle collapse
        setBubbles(prev => prev.map(b =>
          b.id === bubble.id ? { ...b, expanded: !b.expanded } : b
        ))
        return
      }

      // Fetch and add sub-topics
      setIsLoadingRelated(true)
      try {
        const subTopics = await fetchRelatedTopics(bubble.text)
        
        // Create sub-bubbles in a smaller circle around the clicked bubble
        const angleStep = (2 * Math.PI) / subTopics.length
        const radius = 15 // smaller radius for sub-bubbles

        const newSubBubbles: Bubble[] = subTopics.map((topic, index) => {
          const angle = index * angleStep
          const x = bubble.x + radius * Math.cos(angle)
          const y = bubble.y + radius * Math.sin(angle)

          return {
            id: `sub-${bubble.id}-${index}`,
            text: topic,
            x,
            y,
            level: 2,
            parentId: bubble.id,
          }
        })

        // Update the bubble with sub-bubbles and set expanded
        setBubbles(prev => [
          ...prev.map(b =>
            b.id === bubble.id ? { ...b, expanded: true, subBubbles: newSubBubbles } : b
          ),
          ...newSubBubbles,
        ])
      } catch (error) {
        console.error('Failed to fetch sub-topics:', error)
      } finally {
        setIsLoadingRelated(false)
      }
    }
  }

  const handleRemoveInterest = (interest: string) => {
    const newLiked = likedInterests.filter(i => i !== interest)
    setLikedInterests(newLiked)
    onInterestsChange?.(newLiked)

    // Update bubble states
    setBubbles(prev => prev.map(b =>
      b.text === interest ? { ...b, liked: false } : b
    ))
  }

  return (
    <div className={`relative ${className}`}>
      {/* Seed Input */}
      {showSeedInput ? (
        <div className="mb-6 p-6 bg-gradient-to-br from-primary/5 to-purple-500/5 rounded-lg border-2 border-primary/20">
          <div className="flex items-center gap-3 mb-3">
            <Sparkles className="w-5 h-5 text-primary" />
            <h3 className="font-semibold text-foreground">Discover Topics</h3>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={currentSeed}
              onChange={(e) => setCurrentSeed(e.target.value)}
              placeholder="Enter a topic you're interested in... (e.g., AI, climate, music)"
              className="flex-1 px-4 py-3 border border-border rounded-lg bg-background focus:ring-2 focus:ring-primary focus:border-primary transition-all"
              onKeyDown={(e) => e.key === 'Enter' && !isLoadingRelated && handleSeedSubmit()}
              disabled={isLoadingRelated}
              autoFocus
            />
            <Button 
              onClick={handleSeedSubmit} 
              disabled={!currentSeed.trim() || isLoadingRelated}
              size="lg"
            >
              {isLoadingRelated ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
              ) : (
                <Plus className="w-5 h-5" />
              )}
            </Button>
          </div>
        </div>
      ) : (
        <div className="mb-6 flex justify-between items-center">
          <p className="text-sm text-muted-foreground">
            Click bubbles to explore related topics, or add a new topic
          </p>
          <Button variant="outline" size="sm" onClick={handleAddAnother}>
            <Plus className="w-4 h-4 mr-2" />
            Add Another Topic
          </Button>
        </div>
      )}

      {/* Bubble Container */}
      <div
        ref={containerRef}
        className="relative w-full min-h-[500px] bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-blue-950/20 dark:via-purple-950/20 dark:to-pink-950/20 rounded-xl border-2 border-border overflow-hidden shadow-inner"
      >
        {isLoadingRelated && (
          <div className="absolute inset-0 bg-background/50 backdrop-blur-sm flex items-center justify-center z-10">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-3" />
              <p className="text-sm text-muted-foreground">Discovering related topics...</p>
            </div>
          </div>
        )}

        {bubbles.length === 0 ? (
          <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">
            <div className="text-center max-w-md p-8">
              <div className="text-6xl mb-4">🎯</div>
              <h3 className="text-lg font-semibold mb-2">Start Your Discovery Journey</h3>
              <p className="text-sm">
                Enter a topic you're interested in above, and we'll show you related areas to explore
              </p>
            </div>
          </div>
        ) : (
          bubbles.map((bubble) => {
            const isMainBubble = bubble.level === 0
            const isSubBubble = bubble.level === 2
            const sizeClass = isMainBubble ? 'px-6 py-3 text-base' : isSubBubble ? 'px-2 py-1 text-xs' : 'px-4 py-2 text-sm'

            return (
              <div
                key={bubble.id}
                className={`group absolute transition-all duration-300 ${bubble.disliked ? 'opacity-50 scale-90' : 'opacity-100 scale-100'}`}
                style={{
                  left: `${bubble.x}%`,
                  top: `${bubble.y}%`,
                  transform: 'translate(-50%, -50%)',
                  zIndex: isMainBubble ? 20 : isSubBubble ? 5 : 10,
                }}
              >
                {/* Bubble */}
                <div
                  className={`
                    relative ${sizeClass} rounded-full cursor-pointer transition-all duration-200 shadow-md hover:shadow-lg font-medium
                    ${bubble.liked
                      ? 'bg-green-500 text-white border-2 border-green-600 scale-105'
                      : bubble.disliked
                      ? 'bg-red-100 text-red-800 border-2 border-red-300 line-through'
                      : 'bg-white text-foreground border-2 border-border hover:border-primary hover:scale-105'
                    }
                    ${isMainBubble ? 'font-bold shadow-xl' : ''}
                  `}
                  onClick={() => !bubble.liked && !isMainBubble && handleBubbleClick(bubble, 'expand')}
                  title={bubble.expanded ? 'Click to collapse' : 'Click to explore related topics'}
                >
                  <span>{bubble.text}</span>

                  {/* Expand indicator */}
                  {bubble.expanded && bubble.subBubbles && (
                    <span className="ml-2 text-xs">▼</span>
                  )}

                  {/* Action Buttons */}
                  {!bubble.liked && !bubble.disliked && !isMainBubble && (
                    <div className="absolute -top-2 -right-2 flex gap-1 transition-opacity">
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleBubbleClick(bubble, 'like')
                        }}
                        className="w-7 h-7 bg-green-500 text-white rounded-full flex items-center justify-center hover:bg-green-600 transition-all hover:scale-110 shadow-lg"
                        title="Add to my interests"
                      >
                        <Heart className="w-4 h-4 fill-current" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleBubbleClick(bubble, 'dislike')
                        }}
                        className="w-7 h-7 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-all hover:scale-110 shadow-lg"
                        title="Not interested"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )
          })
        )}
      </div>

      {/* Selected Interests */}
      {likedInterests.length > 0 && (
        <div className="mt-6 p-5 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 border border-green-200 dark:border-green-800 rounded-lg shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-semibold text-green-900 dark:text-green-100 flex items-center gap-2">
              <Check className="w-5 h-5" />
              Selected Topics ({likedInterests.length})
            </h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {likedInterests.map((interest) => (
              <div
                key={interest}
                className="group relative inline-flex items-center gap-2 px-3 py-1.5 bg-green-500 text-white rounded-full text-sm font-medium shadow-sm hover:bg-green-600 transition-colors"
              >
                <span>{interest}</span>
                <button
                  onClick={() => handleRemoveInterest(interest)}
                  className="opacity-0 group-hover:opacity-100 transition-opacity ml-1 hover:scale-110"
                  title="Remove topic"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}