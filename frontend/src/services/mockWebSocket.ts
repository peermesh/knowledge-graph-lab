import { faker } from '@faker-js/faker'
import { mockEntities } from '@/mocks/data/entities'

type MessageHandler = (data: any) => void

export class MockWebSocketService {
  private listeners: Map<string, MessageHandler[]> = new Map()
  private connected: boolean = false
  private simulationInterval: NodeJS.Timeout | null = null
  
  async connect(): Promise<void> {
    // Simulate connection delay
    await new Promise(resolve => setTimeout(resolve, 300))
    
    this.connected = true
    this.emit('system_notification', {
      message: 'Connected to Knowledge Graph Lab (Mock Mode)',
      timestamp: new Date().toISOString()
    })
    
    console.log('✓ Mock WebSocket connected')
    
    // Start simulating updates
    this.startSimulation()
  }
  
  disconnect(): void {
    this.connected = false
    if (this.simulationInterval) {
      clearInterval(this.simulationInterval)
      this.simulationInterval = null
    }
    console.log('✓ Mock WebSocket disconnected')
  }
  
  subscribe(messageType: string, handler: MessageHandler): void {
    if (!this.listeners.has(messageType)) {
      this.listeners.set(messageType, [])
    }
    this.listeners.get(messageType)!.push(handler)
  }
  
  unsubscribe(messageType: string, handler: MessageHandler): void {
    const handlers = this.listeners.get(messageType)
    if (handlers) {
      const index = handlers.indexOf(handler)
      if (index > -1) {
        handlers.splice(index, 1)
      }
    }
  }
  
  private emit(type: string, data: any): void {
    const handlers = this.listeners.get(type) || []
    handlers.forEach(handler => {
      try {
        handler(data)
      } catch (error) {
        console.error(`Error in ${type} handler:`, error)
      }
    })
  }
  
  private startSimulation(): void {
    // Simulate real-time updates every 10 seconds (not too frequent)
    this.simulationInterval = setInterval(() => {
      if (!this.connected) return
      
      // Random entity update (30% chance)
      if (Math.random() > 0.7 && mockEntities.length > 0) {
        const entity = faker.helpers.arrayElement(mockEntities)
        this.emit('entity_update', {
          entity_id: entity.id,
          action: 'updated',
          entity: {
            ...entity,
            updated_at: new Date().toISOString()
          },
          timestamp: new Date().toISOString()
        })
      }
      
      // Random graph update (20% chance)
      if (Math.random() > 0.8) {
        this.emit('graph_update', {
          nodes_changed: faker.number.int({ min: 1, max: 5 }),
          edges_changed: faker.number.int({ min: 1, max: 10 }),
          timestamp: new Date().toISOString()
        })
      }
      
      // Random feed update (15% chance)
      if (Math.random() > 0.85) {
        this.emit('feed_update', {
          new_items: faker.number.int({ min: 1, max: 3 }),
          timestamp: new Date().toISOString()
        })
      }
      
      // Random notification (10% chance)
      if (Math.random() > 0.9) {
        const notifications = [
          'New research item added to your feed',
          'Entity relationship discovered',
          'Graph analysis complete',
          'New user joined your team',
          'Daily insights report ready'
        ]
        
        this.emit('notification', {
          type: faker.helpers.arrayElement(['info', 'success', 'warning']),
          message: faker.helpers.arrayElement(notifications),
          timestamp: new Date().toISOString()
        })
      }
    }, 10000) // Every 10 seconds
  }
  
  get isConnected(): boolean {
    return this.connected
  }
  
  get connectionState(): string {
    return this.connected ? 'connected' : 'disconnected'
  }
}

// Export singleton
export const mockWebSocketService = new MockWebSocketService()












