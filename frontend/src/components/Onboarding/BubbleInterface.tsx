import { useState, useEffect, useRef } from 'react'
import { Heart, X, Plus } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { Badge } from '@/components/Common/Badge'

interface BubbleInterfaceProps {
  onInterestsChange?: (interests: string[]) => void
  className?: string
}

interface Bubble {
  id: string
  text: string
  x: number
  y: number
  liked?: boolean
  disliked?: boolean
  expanded?: boolean
  subBubbles?: Bubble[]
}

export function BubbleInterface({ onInterestsChange, className = '' }: BubbleInterfaceProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [bubbles, setBubbles] = useState<Bubble[]>([])
  const [likedInterests, setLikedInterests] = useState<string[]>([])
  const [currentSeed, setCurrentSeed] = useState('')

  // Mock data for demonstration
  const mockTopics = [
    'Artificial Intelligence',
    'Machine Learning',
    'Natural Language Processing',
    'Computer Vision',
    'Robotics',
    'Data Science',
    'Blockchain',
    'Cybersecurity',
    'Cloud Computing',
    'DevOps',
  ]

  const mockSubTopics = {
    'Artificial Intelligence': [
      'Neural Networks',
      'Deep Learning',
      'Expert Systems',
      'Computer Vision',
      'Natural Language Processing',
    ],
    'Machine Learning': [
      'Supervised Learning',
      'Unsupervised Learning',
      'Reinforcement Learning',
      'Feature Engineering',
      'Model Evaluation',
    ],
    'Natural Language Processing': [
      'Text Classification',
      'Named Entity Recognition',
      'Sentiment Analysis',
      'Language Models',
      'Text Generation',
    ],
  }

  useEffect(() => {
    // Initialize with seed bubble
    const initialBubbles: Bubble[] = [
      {
        id: 'seed',
        text: 'Start typing your interests...',
        x: 50,
        y: 50,
        expanded: false,
      },
    ]
    setBubbles(initialBubbles)
  }, [])

  const handleSeedSubmit = () => {
    if (!currentSeed.trim()) return

    // Generate related bubbles
    const relatedBubbles: Bubble[] = mockTopics
      .filter(topic => topic.toLowerCase().includes(currentSeed.toLowerCase()) ||
                      currentSeed.toLowerCase().includes(topic.toLowerCase()))
      .slice(0, 6)
      .map((topic, index) => ({
        id: `bubble-${index}`,
        text: topic,
        x: 20 + (index % 3) * 30,
        y: 20 + Math.floor(index / 3) * 25,
        expanded: false,
        subBubbles: mockSubTopics[topic as keyof typeof mockSubTopics]?.map((sub, subIndex) => ({
          id: `sub-${topic}-${subIndex}`,
          text: sub,
          x: 10 + subIndex * 15,
          y: 10 + subIndex * 10,
        })) || [],
      }))

    setBubbles(relatedBubbles)
    setCurrentSeed('')
  }

  const handleBubbleClick = (bubble: Bubble, action: 'like' | 'dislike' | 'expand') => {
    if (action === 'like') {
      const newLiked = [...likedInterests, bubble.text]
      setLikedInterests(newLiked)
      onInterestsChange?.(newLiked)

      // Update bubble state
      setBubbles(prev => prev.map(b =>
        b.id === bubble.id ? { ...b, liked: true } : b
      ))
    } else if (action === 'dislike') {
      // Update bubble state
      setBubbles(prev => prev.map(b =>
        b.id === bubble.id ? { ...b, disliked: true } : b
      ))
    } else if (action === 'expand') {
      // Toggle expansion
      setBubbles(prev => prev.map(b =>
        b.id === bubble.id ? { ...b, expanded: !b.expanded } : b
      ))
    }
  }

  const handleSubBubbleClick = (subBubble: Bubble, action: 'like' | 'dislike') => {
    if (action === 'like') {
      const newLiked = [...likedInterests, subBubble.text]
      setLikedInterests(newLiked)
      onInterestsChange?.(newLiked)
    }
  }

  return (
    <div className={`relative ${className}`}>
      {/* Seed Input */}
      <div className="mb-6 p-4 bg-muted/50 rounded-lg">
        <div className="flex gap-2">
          <input
            type="text"
            value={currentSeed}
            onChange={(e) => setCurrentSeed(e.target.value)}
            placeholder="Enter your main area of interest..."
            className="flex-1 px-3 py-2 border border-border rounded-md bg-background"
            onKeyDown={(e) => e.key === 'Enter' && handleSeedSubmit()}
          />
          <Button onClick={handleSeedSubmit} disabled={!currentSeed.trim()}>
            <Plus className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Bubble Container */}
      <div
        ref={containerRef}
        className="relative w-full h-96 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg border-2 border-dashed border-border overflow-hidden"
      >
        {bubbles.length === 0 ? (
          <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">
            <div className="text-center">
              <div className="text-4xl mb-2">💭</div>
              <p>Enter an interest above to explore related topics</p>
            </div>
          </div>
        ) : (
          bubbles.map((bubble) => (
            <div key={bubble.id} className="absolute">
              {/* Main Bubble */}
              <div
                className={`
                  relative px-3 py-2 rounded-full cursor-pointer transition-all duration-200
                  ${bubble.liked
                    ? 'bg-green-100 text-green-800 border-2 border-green-300'
                    : bubble.disliked
                    ? 'bg-red-100 text-red-800 border-2 border-red-300'
                    : 'bg-white text-foreground border-2 border-border hover:border-primary'
                  }
                `}
                style={{
                  left: `${bubble.x}%`,
                  top: `${bubble.y}%`,
                  transform: 'translate(-50%, -50%)',
                }}
                onClick={() => handleBubbleClick(bubble, 'expand')}
              >
                <span className="text-sm font-medium">{bubble.text}</span>

                {/* Action Buttons */}
                {!bubble.liked && !bubble.disliked && (
                  <div className="absolute -top-1 -right-1 flex gap-1">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleBubbleClick(bubble, 'like')
                      }}
                      className="w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center hover:bg-green-600 transition-colors"
                    >
                      <Heart className="w-3 h-3" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleBubbleClick(bubble, 'dislike')
                      }}
                      className="w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </div>
                )}
              </div>

              {/* Sub-bubbles (when expanded) */}
              {bubble.expanded && bubble.subBubbles && (
                <div className="absolute top-full left-0 mt-2">
                  <div className="flex flex-wrap gap-2 max-w-64">
                    {bubble.subBubbles.map((subBubble) => (
                      <button
                        key={subBubble.id}
                        onClick={() => handleSubBubbleClick(subBubble, 'like')}
                        className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors"
                      >
                        {subBubble.text}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Selected Interests */}
      {likedInterests.length > 0 && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <h4 className="font-medium text-green-800 mb-2">Selected Interests:</h4>
          <div className="flex flex-wrap gap-2">
            {likedInterests.map((interest) => (
              <Badge key={interest} variant="default" className="bg-green-100 text-green-800">
                {interest}
              </Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}