/**
 * Performance monitoring and optimization service.
 *
 * Tracks performance metrics, monitors resource usage, and provides
 * optimization recommendations for the frontend application.
 */

interface PerformanceMetrics {
  loadTime: number
  domContentLoaded: number
  firstContentfulPaint: number
  largestContentfulPaint: number
  firstInputDelay: number
  cumulativeLayoutShift: number
  memoryUsage: number
  cpuUsage: number
  networkLatency: number
  bundleSize: number
}

interface PerformanceThresholds {
  loadTime: number // ms
  domContentLoaded: number // ms
  firstContentfulPaint: number // ms
  largestContentfulPaint: number // ms
  firstInputDelay: number // ms
  cumulativeLayoutShift: number
  memoryUsage: number // MB
  cpuUsage: number // %
  networkLatency: number // ms
  bundleSize: number // KB
}

class PerformanceMonitor {
  private metrics: PerformanceMetrics = {
    loadTime: 0,
    domContentLoaded: 0,
    firstContentfulPaint: 0,
    largestContentfulPaint: 0,
    firstInputDelay: 0,
    cumulativeLayoutShift: 0,
    memoryUsage: 0,
    cpuUsage: 0,
    networkLatency: 0,
    bundleSize: 0,
  }

  private thresholds: PerformanceThresholds = {
    loadTime: 2000, // 2 seconds
    domContentLoaded: 1500, // 1.5 seconds
    firstContentfulPaint: 1800, // 1.8 seconds
    largestContentfulPaint: 2500, // 2.5 seconds
    firstInputDelay: 100, // 100ms
    cumulativeLayoutShift: 0.1, // 0.1
    memoryUsage: 100, // 100MB
    cpuUsage: 70, // 70%
    networkLatency: 100, // 100ms
    bundleSize: 1024, // 1MB
  }

  private observers: PerformanceObserver[] = []
  private intervals: number[] = []

  startMonitoring(): void {
    this.observeNavigationTiming()
    this.observePaintTiming()
    this.observeLayoutShifts()
    this.observeMemoryUsage()
    this.observeNetworkLatency()
    this.observeBundleSize()
  }

  stopMonitoring(): void {
    this.observers.forEach(observer => observer.disconnect())
    this.intervals.forEach(interval => clearInterval(interval))
    this.observers = []
    this.intervals = []
  }

  private observeNavigationTiming(): void {
    if ('performance' in window && 'getEntriesByType' in performance) {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming

      if (navigation) {
        this.metrics.loadTime = navigation.loadEventEnd - navigation.fetchStart
        this.metrics.domContentLoaded = navigation.domContentLoadedEventEnd - navigation.fetchStart

        // Check thresholds and alert if exceeded
        this.checkThreshold('loadTime', this.metrics.loadTime)
        this.checkThreshold('domContentLoaded', this.metrics.domContentLoaded)
      }
    }
  }

  private observePaintTiming(): void {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.name === 'first-contentful-paint') {
            this.metrics.firstContentfulPaint = entry.startTime
            this.checkThreshold('firstContentfulPaint', entry.startTime)
          } else if (entry.name === 'largest-contentful-paint') {
            this.metrics.largestContentfulPaint = entry.startTime
            this.checkThreshold('largestContentfulPaint', entry.startTime)
          }
        }
      })

      try {
        observer.observe({ entryTypes: ['paint', 'largest-contentful-paint'] })
        this.observers.push(observer)
      } catch (e) {
        console.warn('Performance observer not supported')
      }
    }
  }

  private observeLayoutShifts(): void {
    if ('PerformanceObserver' in window) {
      let cumulativeLayoutShift = 0

      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!(entry as any).hadRecentInput) {
            cumulativeLayoutShift += (entry as any).value
          }
        }

        this.metrics.cumulativeLayoutShift = cumulativeLayoutShift
        this.checkThreshold('cumulativeLayoutShift', cumulativeLayoutShift)
      })

      try {
        observer.observe({ entryTypes: ['layout-shift'] })
        this.observers.push(observer)
      } catch (e) {
        console.warn('Layout shift observer not supported')
      }
    }
  }

  private observeMemoryUsage(): void {
    const updateMemoryUsage = () => {
      if ('memory' in performance) {
        const memory = (performance as any).memory
        this.metrics.memoryUsage = memory.usedJSHeapSize / (1024 * 1024) // Convert to MB
        this.checkThreshold('memoryUsage', this.metrics.memoryUsage)
      }
    }

    updateMemoryUsage()
    const interval = setInterval(updateMemoryUsage, 5000) // Update every 5 seconds
    this.intervals.push(interval)
  }

  private observeNetworkLatency(): void {
    const updateNetworkLatency = () => {
      // Measure network latency by timing a small request
      const start = performance.now()
      fetch('/health', {
        method: 'HEAD',
        cache: 'no-cache',
      }).then(() => {
        const latency = performance.now() - start
        this.metrics.networkLatency = latency
        this.checkThreshold('networkLatency', latency)
      }).catch(() => {
        // Network request failed, don't update metrics
      })
    }

    updateNetworkLatency()
    const interval = setInterval(updateNetworkLatency, 10000) // Update every 10 seconds
    this.intervals.push(interval)
  }

  private observeBundleSize(): void {
    // Estimate bundle size from network requests
    if ('performance' in window && 'getEntriesByType' in performance) {
      const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[]

      const jsResources = resources.filter(resource =>
        resource.name.includes('.js') && !resource.name.includes('node_modules')
      )

      const totalSize = jsResources.reduce((total, resource) => total + (resource.transferSize || 0), 0)
      this.metrics.bundleSize = totalSize / 1024 // Convert to KB

      this.checkThreshold('bundleSize', this.metrics.bundleSize)
    }
  }

  private checkThreshold(metric: keyof PerformanceThresholds, value: number): void {
    const threshold = this.thresholds[metric]

    if (value > threshold) {
      console.warn(`Performance threshold exceeded: ${metric} = ${value} (threshold: ${threshold})`)

      // Send alert to monitoring service
      this.sendPerformanceAlert(metric, value, threshold)
    }
  }

  private sendPerformanceAlert(metric: string, value: number, threshold: number): void {
    // In a real application, this would send to monitoring service
    console.warn(`PERFORMANCE ALERT: ${metric} = ${value} exceeds threshold ${threshold}`)

    // Could integrate with services like Sentry, DataDog, etc.
  }

  getMetrics(): PerformanceMetrics {
    return { ...this.metrics }
  }

  getThresholds(): PerformanceThresholds {
    return { ...this.thresholds }
  }

  updateThresholds(newThresholds: Partial<PerformanceThresholds>): void {
    this.thresholds = { ...this.thresholds, ...newThresholds }
  }

  generateReport(): string {
    const metrics = this.getMetrics()
    const thresholds = this.getThresholds()

    return `
Performance Report:
==================

Core Web Vitals:
- Load Time: ${metrics.loadTime}ms (threshold: ${thresholds.loadTime}ms)
- DOM Content Loaded: ${metrics.domContentLoaded}ms (threshold: ${thresholds.domContentLoaded}ms)
- First Contentful Paint: ${metrics.firstContentfulPaint}ms (threshold: ${thresholds.firstContentfulPaint}ms)
- Largest Contentful Paint: ${metrics.largestContentfulPaint}ms (threshold: ${thresholds.largestContentfulPaint}ms)
- First Input Delay: ${metrics.firstInputDelay}ms (threshold: ${thresholds.firstInputDelay}ms)
- Cumulative Layout Shift: ${metrics.cumulativeLayoutShift} (threshold: ${thresholds.cumulativeLayoutShift})

Resource Usage:
- Memory Usage: ${metrics.memoryUsage.toFixed(1)}MB (threshold: ${thresholds.memoryUsage}MB)
- Bundle Size: ${metrics.bundleSize.toFixed(1)}KB (threshold: ${thresholds.bundleSize}KB)

Network:
- Latency: ${metrics.networkLatency.toFixed(1)}ms (threshold: ${thresholds.networkLatency}ms)

Status: ${this.getOverallStatus()}
    `.trim()
  }

  private getOverallStatus(): string {
    const metrics = this.getMetrics()
    const thresholds = this.getThresholds()

    const exceededMetrics = Object.entries(metrics).filter(([key, value]) => {
      const thresholdKey = key as keyof PerformanceThresholds
      return value > thresholds[thresholdKey]
    })

    if (exceededMetrics.length === 0) {
      return '✅ All metrics within thresholds'
    } else {
      return `⚠️ ${exceededMetrics.length} metrics exceed thresholds: ${exceededMetrics.map(([key]) => key).join(', ')}`
    }
  }
}

// Create singleton instance
export const performanceMonitor = new PerformanceMonitor()

// Auto-start monitoring
if (typeof window !== 'undefined') {
  performanceMonitor.startMonitoring()
}

// React hook for accessing performance metrics
export function usePerformanceMetrics() {
  return {
    metrics: performanceMonitor.getMetrics(),
    thresholds: performanceMonitor.getThresholds(),
    report: performanceMonitor.generateReport(),
    updateThresholds: performanceMonitor.updateThresholds.bind(performanceMonitor),
  }
}
