/**
 * WebSocket service for real-time updates.
 *
 * Handles WebSocket connections, message routing, and reconnection
 * logic for real-time communication with the backend.
 */

import { useUIStore } from '@/store/useUIStore'

export type WebSocketMessageType =
  | 'entity_update'
  | 'relationship_update'
  | 'user_activity'
  | 'system_notification'
  | 'graph_update'
  | 'feed_update'

export interface WebSocketMessage {
  type: WebSocketMessageType
  data: any
  timestamp: string
  id: string
  source: 'backend' | 'ai' | 'user'
}

export interface WebSocketConfig {
  url: string
  reconnectInterval: number
  maxReconnectAttempts: number
  heartbeatInterval: number
  subscriptions: Set<string>
}

class WebSocketService {
  private ws: WebSocket | null = null
  private config: WebSocketConfig
  private reconnectAttempts = 0
  private heartbeatTimer: number | null = null
  private reconnectTimer: number | null = null
  private messageHandlers: Map<WebSocketMessageType, ((data: any) => void)[]> = new Map()
  private isConnecting = false

  constructor(config: Partial<WebSocketConfig> = {}) {
    this.config = {
      url: config.url || 'ws://localhost:8000/ws',
      reconnectInterval: config.reconnectInterval || 1000,
      maxReconnectAttempts: config.maxReconnectAttempts || 5,
      heartbeatInterval: config.heartbeatInterval || 30000,
      subscriptions: config.subscriptions || new Set(),
    }
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.isConnecting || this.ws?.readyState === WebSocket.OPEN) {
        resolve()
        return
      }

      this.isConnecting = true

      try {
        this.ws = new WebSocket(this.config.url)

        this.ws.onopen = () => {
          console.log('WebSocket connected')
          this.isConnecting = false
          this.reconnectAttempts = 0
          this.startHeartbeat()

          useUIStore.getState().addNotification({
            type: 'success',
            message: 'Connected to live updates',
            duration: 2000,
          })

          resolve()
        }

        this.ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data)
            this.handleMessage(message)
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error)
          }
        }

        this.ws.onclose = (event) => {
          console.log('WebSocket disconnected:', event.code, event.reason)
          this.isConnecting = false
          this.stopHeartbeat()

          if (event.code !== 1000) { // Not a normal closure
            this.scheduleReconnect()
          }
        }

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          this.isConnecting = false
          reject(error)
        }

      } catch (error) {
        this.isConnecting = false
        reject(error)
      }
    })
  }

  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }

    this.stopHeartbeat()

    if (this.ws) {
      this.ws.close(1000, 'Client disconnect')
      this.ws = null
    }
  }

  subscribe(messageType: WebSocketMessageType, handler: (data: any) => void): void {
    if (!this.messageHandlers.has(messageType)) {
      this.messageHandlers.set(messageType, [])
    }

    this.messageHandlers.get(messageType)!.push(handler)

    // Send subscription message if connected
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.send({
        type: 'subscribe',
        data: { messageType },
        timestamp: new Date().toISOString(),
        id: crypto.randomUUID(),
        source: 'user',
      })
    }
  }

  unsubscribe(messageType: WebSocketMessageType, handler: (data: any) => void): void {
    const handlers = this.messageHandlers.get(messageType)
    if (handlers) {
      const index = handlers.indexOf(handler)
      if (index > -1) {
        handlers.splice(index, 1)
      }

      if (handlers.length === 0) {
        this.messageHandlers.delete(messageType)
      }
    }

    // Send unsubscription message if connected
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.send({
        type: 'unsubscribe',
        data: { messageType },
        timestamp: new Date().toISOString(),
        id: crypto.randomUUID(),
        source: 'user',
      })
    }
  }

  private send(message: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    }
  }

  private handleMessage(message: WebSocketMessage): void {
    const handlers = this.messageHandlers.get(message.type)
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(message.data)
        } catch (error) {
          console.error(`Error in message handler for ${message.type}:`, error)
        }
      })
    }
  }

  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.send({
          type: 'ping',
          timestamp: new Date().toISOString(),
          id: crypto.randomUUID(),
          source: 'user',
        })
      }
    }, this.config.heartbeatInterval)
  }

  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.config.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached')

      useUIStore.getState().addNotification({
        type: 'error',
        message: 'Connection lost. Please refresh the page.',
        duration: 0, // Don't auto-dismiss
      })

      return
    }

    const delay = Math.min(
      this.config.reconnectInterval * Math.pow(2, this.reconnectAttempts),
      30000 // Max 30 second delay
    )

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts + 1})`)

    this.reconnectTimer = setTimeout(() => {
      this.reconnectAttempts++
      this.connect().catch(console.error)
    }, delay)
  }

  get isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }

  get connectionState(): string {
    if (!this.ws) return 'disconnected'
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING:
        return 'connecting'
      case WebSocket.OPEN:
        return 'connected'
      case WebSocket.CLOSING:
        return 'closing'
      case WebSocket.CLOSED:
        return 'disconnected'
      default:
        return 'unknown'
    }
  }
}

// Create singleton instance
const realWebSocketService = new WebSocketService()

// Import mock service for development
import { mockWebSocketService } from './mockWebSocket'

// Use mock in development, real WebSocket in production
export const websocketService = import.meta.env.DEV 
  ? mockWebSocketService 
  : realWebSocketService

// React hook for using WebSocket service
export function useWebSocket() {
  return {
    isConnected: websocketService.isConnected,
    connectionState: websocketService.connectionState,
    subscribe: websocketService.subscribe.bind(websocketService),
    unsubscribe: websocketService.unsubscribe.bind(websocketService),
    connect: websocketService.connect.bind(websocketService),
    disconnect: websocketService.disconnect.bind(websocketService),
  }
}

// Auto-connect on module load
if (typeof window !== 'undefined') {
  // Connect WebSocket when the module is loaded in the browser
  websocketService.connect().catch(console.error)
}