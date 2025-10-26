import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  Home,
  Settings,
  BarChart3,
  Users,
  BookOpen,
  Lightbulb,
  Target
} from 'lucide-react'

import { cn } from '@/utils/cn'

interface NavigationItem {
  name: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  description?: string
}

const navigationItems: NavigationItem[] = [
  {
    name: 'Feed',
    href: '/feed',
    icon: Home,
    description: 'Personalized research feed'
  },
  {
    name: 'Graph Lab',
    href: '/lab',
    icon: Target,
    description: 'Interactive knowledge exploration'
  },
  {
    name: 'Analytics',
    href: '/analytics',
    icon: BarChart3,
    description: 'Usage and performance insights'
  },
  {
    name: 'Research',
    href: '/research',
    icon: BookOpen,
    description: 'Research tools and resources'
  },
  {
    name: 'Insights',
    href: '/insights',
    icon: Lightbulb,
    description: 'AI-generated insights'
  },
  {
    name: 'Team',
    href: '/team',
    icon: Users,
    description: 'Team collaboration tools'
  },
]

export function MainNavigation() {
  return (
    <nav className="h-full flex flex-col bg-card border-r border-border">
      {/* Logo/Brand */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-sm">KG</span>
          </div>
          <div>
            <h1 className="font-semibold text-lg">Knowledge Graph Lab</h1>
            <p className="text-xs text-muted-foreground">Research Platform</p>
          </div>
        </div>
      </div>

      {/* Navigation Items */}
      <div className="flex-1 p-4">
        <ul className="space-y-2">
          {navigationItems.map((item) => (
            <li key={item.name}>
              <NavLink
                to={item.href}
                className={({ isActive }) =>
                  cn(
                    'flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                    'hover:bg-accent hover:text-accent-foreground',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground'
                  )
                }
                title={item.description}
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </div>

      {/* Settings */}
      <div className="p-4 border-t border-border">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            cn(
              'flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              'hover:bg-accent hover:text-accent-foreground',
              isActive
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground'
            )
          }
        >
          <Settings className="w-5 h-5" />
          <span>Settings</span>
        </NavLink>
      </div>

      {/* User Profile */}
      <div className="p-4 border-t border-border">
        <div className="flex items-center space-x-3 px-3 py-2">
          <div className="w-8 h-8 bg-muted rounded-full flex items-center justify-center">
            <span className="text-sm font-medium text-muted-foreground">U</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">User</p>
            <p className="text-xs text-muted-foreground truncate">user@example.com</p>
          </div>
        </div>
      </div>
    </nav>
  )
}