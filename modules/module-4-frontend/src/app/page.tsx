'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Badge } from '../components/ui/badge'
import { Progress } from '../components/ui/progress'
import { 
  Brain, 
  Database, 
  Search, 
  TrendingUp, 
  Users, 
  Globe,
  ArrowRight,
  Activity,
  Clock,
  AlertCircle
} from 'lucide-react'

interface ServiceStatus {
  name: string
  status: 'healthy' | 'unhealthy' | 'unknown'
  url: string
  icon: React.ElementType
}

interface KnowledgeStats {
  totalEntities: number
  totalRelationships: number
  activeSources: number
  lastUpdate: string
}

export default function HomePage() {
  const [serviceStatuses, setServiceStatuses] = useState<ServiceStatus[]>([
    { name: 'Ingestion Service', status: 'unknown', url: '/api/health', icon: Database },
    { name: 'Knowledge Graph', status: 'unknown', url: '/api/health', icon: Brain },
    { name: 'Reasoning Engine', status: 'unknown', url: '/api/health', icon: TrendingUp },
  ])

  const [stats, setStats] = useState<KnowledgeStats>({
    totalEntities: 0,
    totalRelationships: 0,
    activeSources: 0,
    lastUpdate: new Date().toISOString()
  })

  useEffect(() => {
    // Check service health on component mount
    const checkServiceHealth = async () => {
      // Mock health check - in real implementation, would check actual services
      setServiceStatuses(prev => prev.map(service => ({ 
        ...service, 
        status: Math.random() > 0.2 ? 'healthy' : 'unhealthy'
      })))
      
      // Mock stats - in real implementation, would fetch from knowledge graph API
      setStats({
        totalEntities: Math.floor(Math.random() * 1000) + 100,
        totalRelationships: Math.floor(Math.random() * 500) + 200,
        activeSources: Math.floor(Math.random() * 20) + 5,
        lastUpdate: new Date().toISOString()
      })
    }

    checkServiceHealth()
  }, [])

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 24
      }
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'bg-green-500'
      case 'unhealthy': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent mb-4">
          Knowledge Graph Lab
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Autonomous AI research system that discovers, organizes, and synthesizes knowledge 
          from the creator economy and beyond.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" className="group">
            Explore Knowledge Graph
            <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </Button>
          <Button size="lg" variant="outline">
            View Research Dashboard
          </Button>
        </div>
      </motion.div>

      {/* Service Status Grid */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
      >
        {serviceStatuses.map((service, index) => (
          <motion.div key={service.name} variants={itemVariants}>
            <Card className="relative overflow-hidden">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <service.icon className="h-5 w-5 text-muted-foreground" />
                    <CardTitle className="text-base">{service.name}</CardTitle>
                  </div>
                  <div className={`h-2 w-2 rounded-full ${getStatusColor(service.status)}`} />
                </div>
              </CardHeader>
              <CardContent>
                <Badge 
                  variant={service.status === 'healthy' ? 'default' : 'destructive'}
                  className="text-xs"
                >
                  {service.status === 'healthy' ? 'Operational' : 
                   service.status === 'unhealthy' ? 'Error' : 'Checking...'}
                </Badge>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {/* Knowledge Base Stats */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12"
      >
        <motion.div variants={itemVariants}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                Knowledge Base Overview
              </CardTitle>
              <CardDescription>
                Current state of the autonomous research system
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{stats.totalEntities}</div>
                  <div className="text-sm text-muted-foreground">Entities</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-violet-600">{stats.totalRelationships}</div>
                  <div className="text-sm text-muted-foreground">Relationships</div>
                </div>
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span>Active Data Sources</span>
                  <span className="font-medium">{stats.activeSources}</span>
                </div>
                <Progress value={(stats.activeSources / 25) * 100} className="h-2" />
              </div>

              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Clock className="h-4 w-4" />
                Last updated: {new Date(stats.lastUpdate).toLocaleTimeString()}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                System Activity
              </CardTitle>
              <CardDescription>
                Real-time insights and research progress
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-sm">Research Queue Active</span>
                  </div>
                  <Badge variant="secondary">3 topics</Badge>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-blue-500" />
                    <span className="text-sm">Content Generation</span>
                  </div>
                  <Badge variant="secondary">2 digests</Badge>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-yellow-500" />
                    <span className="text-sm">Knowledge Gaps</span>
                  </div>
                  <Badge variant="secondary">5 identified</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
      >
        <motion.div variants={itemVariants}>
          <Card className="cursor-pointer hover:shadow-md transition-shadow">
            <CardContent className="flex flex-col items-center justify-center p-6 text-center">
              <Search className="h-8 w-8 mb-3 text-blue-600" />
              <h3 className="font-semibold mb-1">Search Knowledge</h3>
              <p className="text-sm text-muted-foreground">
                Explore entities and relationships
              </p>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card className="cursor-pointer hover:shadow-md transition-shadow">
            <CardContent className="flex flex-col items-center justify-center p-6 text-center">
              <Brain className="h-8 w-8 mb-3 text-violet-600" />
              <h3 className="font-semibold mb-1">AI Research</h3>
              <p className="text-sm text-muted-foreground">
                Start autonomous research
              </p>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card className="cursor-pointer hover:shadow-md transition-shadow">
            <CardContent className="flex flex-col items-center justify-center p-6 text-center">
              <Users className="h-8 w-8 mb-3 text-green-600" />
              <h3 className="font-semibold mb-1">User Profiles</h3>
              <p className="text-sm text-muted-foreground">
                Manage preferences
              </p>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card className="cursor-pointer hover:shadow-md transition-shadow">
            <CardContent className="flex flex-col items-center justify-center p-6 text-center">
              <Globe className="h-8 w-8 mb-3 text-orange-600" />
              <h3 className="font-semibold mb-1">Content Hub</h3>
              <p className="text-sm text-muted-foreground">
                Generated digests & insights
              </p>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>
    </div>
  )
}