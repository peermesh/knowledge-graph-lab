import { http, HttpResponse } from 'msw'
import { mockUsers, getUserByEmail } from '../data/users'
import { faker } from '@faker-js/faker'

export const authHandlers = [
  // Login
  http.post('/api/v1/auth/login', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 300))
    
    const body = await request.json() as { email: string; password: string }
    const { email, password } = body
    
    // Find user by email
    const user = getUserByEmail(email)
    
    // Validate - for demo, any password >= 6 chars works
    if (!user || password.length < 6) {
      return HttpResponse.json(
        { 
          error: 'Invalid credentials',
          message: 'Email or password is incorrect'
        },
        { status: 401 }
      )
    }
    
    // Check if user is active
    if (!user.is_active) {
      return HttpResponse.json(
        {
          error: 'Account disabled',
          message: 'This account has been disabled'
        },
        { status: 403 }
      )
    }
    
    // Generate mock JWT tokens
    const accessToken = `mock_access_${Date.now()}_${user.id}`
    const refreshToken = `mock_refresh_${Date.now()}_${user.id}`
    
    // Update last login
    user.last_login = new Date().toISOString()
    
    return HttpResponse.json({
      access_token: accessToken,
      refresh_token: refreshToken,
      token_type: 'bearer',
      expires_in: 3600,
      user: {
        id: user.id,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        role: user.role,
        is_active: user.is_active,
        created_at: user.created_at,
        last_login: user.last_login
      }
    })
  }),
  
  // Register
  http.post('/api/v1/auth/register', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const body = await request.json() as {
      email: string
      password: string
      first_name: string
      last_name: string
    }
    
    // Check if user already exists
    const existingUser = getUserByEmail(body.email)
    if (existingUser) {
      return HttpResponse.json(
        {
          error: 'Email already registered',
          message: 'An account with this email already exists'
        },
        { status: 400 }
      )
    }
    
    // Validate password
    if (body.password.length < 6) {
      return HttpResponse.json(
        {
          error: 'Password too short',
          message: 'Password must be at least 6 characters'
        },
        { status: 400 }
      )
    }
    
    // Create new user
    const newUser = {
      id: faker.string.uuid(),
      email: body.email,
      first_name: body.first_name,
      last_name: body.last_name,
      role: 'user' as const,
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      last_login: undefined
    }
    
    // Add to mock users
    mockUsers.push(newUser)
    
    return HttpResponse.json(newUser, { status: 201 })
  }),
  
  // Refresh token
  http.post('/api/v1/auth/refresh', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 200))
    
    const body = await request.json() as { refresh_token: string }
    const { refresh_token } = body
    
    // Validate refresh token format
    if (!refresh_token || !refresh_token.startsWith('mock_refresh_')) {
      return HttpResponse.json(
        {
          error: 'Invalid refresh token',
          message: 'The provided refresh token is invalid'
        },
        { status: 401 }
      )
    }
    
    // Extract user ID from token
    const userId = refresh_token.split('_').pop()
    
    // Generate new access token
    const newAccessToken = `mock_access_${Date.now()}_${userId}`
    
    return HttpResponse.json({
      access_token: newAccessToken,
      token_type: 'bearer',
      expires_in: 3600
    })
  }),
  
  // Logout
  http.post('/api/v1/auth/logout', async () => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 200))
    
    return HttpResponse.json({
      message: 'Successfully logged out'
    })
  }),
  
  // Get current user
  http.get('/api/v1/auth/me', async ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    
    // Check for auth header
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return HttpResponse.json(
        {
          error: 'Unauthorized',
          message: 'No authentication token provided'
        },
        { status: 401 }
      )
    }
    
    // Validate token format
    const token = authHeader.replace('Bearer ', '')
    if (!token.startsWith('mock_access_')) {
      return HttpResponse.json(
        {
          error: 'Invalid token',
          message: 'The provided token is invalid'
        },
        { status: 401 }
      )
    }
    
    // Extract user ID from token
    const userId = token.split('_').pop()
    const user = mockUsers.find(u => u.id === userId)
    
    if (!user) {
      return HttpResponse.json(
        {
          error: 'User not found',
          message: 'No user found for this token'
        },
        { status: 404 }
      )
    }
    
    return HttpResponse.json(user)
  })
]












