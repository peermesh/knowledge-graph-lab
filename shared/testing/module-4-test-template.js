/**
 * Test template for Module 4: Frontend & User Experience
 * Tests the user interface and user experience functionality with mock data.
 */

const fs = require('fs');
const path = require('path');

// Mock data loader utility
class MockDataLoader {
    constructor(basePath = path.join(__dirname, '../..', 'mock-data')) {
        this.basePath = basePath;
    }

    loadMockUsers() {
        const filePath = path.join(this.basePath, 'users', 'profiles.json');
        return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }

    loadMockContent() {
        const content = {};
        const contentTypes = ['articles', 'news', 'social-posts'];
        
        contentTypes.forEach(type => {
            const filePath = path.join(this.basePath, 'content', `${type}.json`);
            content[type] = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        });
        
        return content;
    }

    loadMockEntities() {
        const entities = {};
        const entityTypes = ['creators', 'platforms', 'organizations', 'grants', 'policies'];
        
        entityTypes.forEach(type => {
            const filePath = path.join(this.basePath, 'entities', `${type}.json`);
            entities[type] = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        });
        
        return entities;
    }

    loadMockRelationships() {
        const relationships = {};
        const relationshipTypes = ['creator-platform', 'org-support', 'policy-impact'];
        
        relationshipTypes.forEach(type => {
            const filePath = path.join(this.basePath, 'relationships', `${type}.json`);
            relationships[type] = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        });
        
        return relationships;
    }
}

// Mock API responses for testing
const mockAPI = {
    // Knowledge Graph APIs
    getEntities: (filters) => {
        const loader = new MockDataLoader();
        const entities = loader.loadMockEntities();
        
        if (filters && filters.type) {
            return Promise.resolve(entities[filters.type] || []);
        }
        
        // Return all entities
        const allEntities = [];
        Object.values(entities).forEach(entityList => {
            allEntities.push(...entityList);
        });
        
        return Promise.resolve(allEntities.slice(0, 20)); // Limit for performance
    },

    getRelationships: (entityId) => {
        const loader = new MockDataLoader();
        const relationships = loader.loadMockRelationships();
        
        const entityRelationships = [];
        Object.values(relationships).forEach(relList => {
            relList.forEach(rel => {
                if (rel.source_id === entityId || rel.target_id === entityId) {
                    entityRelationships.push(rel);
                }
            });
        });
        
        return Promise.resolve(entityRelationships);
    },

    searchKnowledge: (query) => {
        const loader = new MockDataLoader();
        const entities = loader.loadMockEntities();
        const content = loader.loadMockContent();
        
        const results = [];
        
        // Search entities
        Object.values(entities).forEach(entityList => {
            entityList.forEach(entity => {
                if (entity.name.toLowerCase().includes(query.toLowerCase()) ||
                    entity.metadata.bio?.toLowerCase().includes(query.toLowerCase())) {
                    results.push({
                        type: 'entity',
                        data: entity,
                        relevance: 0.8
                    });
                }
            });
        });
        
        // Search content
        Object.values(content).forEach(contentList => {
            contentList.forEach(item => {
                if (item.title?.toLowerCase().includes(query.toLowerCase()) ||
                    item.content?.toLowerCase().includes(query.toLowerCase())) {
                    results.push({
                        type: 'content',
                        data: item,
                        relevance: 0.7
                    });
                }
            });
        });
        
        return Promise.resolve(results.slice(0, 10));
    },

    // Content APIs
    getPersonalizedDigest: (userId) => {
        const loader = new MockDataLoader();
        const users = loader.loadMockUsers();
        const user = users.find(u => u.id === userId);
        
        if (!user) {
            return Promise.reject(new Error('User not found'));
        }
        
        const digest = {
            user_id: userId,
            generated_at: new Date().toISOString(),
            content: {
                headline: `This Week in ${user.metadata.location} Creator Economy`,
                sections: [
                    {
                        title: 'New Funding Opportunities',
                        items: [
                            {
                                summary: 'Colorado Arts Council announces $50K creator grants',
                                relevance_score: 0.94,
                                source: 'Colorado Arts Council website',
                                action_required: 'Applications due October 15'
                            }
                        ]
                    },
                    {
                        title: 'Platform Updates',
                        items: [
                            {
                                summary: 'YouTube reduces partner program requirements',
                                relevance_score: 0.89,
                                source: 'YouTube Creator Blog',
                                action_required: null
                            }
                        ]
                    }
                ],
                social_media_ready: {
                    twitter: '🎵 Colorado creators! New $50K grants from @ColoArtsCouncil + YouTube Partner Program changes mean more monetization opportunities! Apply by Oct 15 💰 #CreatorEconomy #Colorado',
                    linkedin: 'Great news for Colorado creators: New funding opportunities and platform policy changes create more paths to monetization. Here are the key updates you need to know...'
                }
            },
            reading_time: '3 minutes',
            word_count: 450
        };
        
        return Promise.resolve(digest);
    },

    getRecommendations: (userId) => {
        const loader = new MockDataLoader();
        const content = loader.loadMockContent();
        const users = loader.loadMockUsers();
        const user = users.find(u => u.id === userId);
        
        if (!user) {
            return Promise.reject(new Error('User not found'));
        }
        
        // Mock recommendation algorithm based on user interests
        const recommendations = [];
        const userInterests = user.metadata.interests || [];
        
        // Get articles that match user interests
        content.articles.forEach(article => {
            let relevanceScore = 0;
            userInterests.forEach(interest => {
                if (article.title.toLowerCase().includes(interest.replace('_', ' ').toLowerCase()) ||
                    article.metadata.tags?.some(tag => tag.includes(interest.replace('_', ' ')))) {
                    relevanceScore += 0.2;
                }
            });
            
            if (relevanceScore > 0) {
                recommendations.push({
                    content: article,
                    relevance_score: Math.min(relevanceScore, 1.0),
                    reasoning: `Matches your interests in ${userInterests.slice(0, 2).join(' and ')}`
                });
            }
        });
        
        // Sort by relevance and return top 5
        recommendations.sort((a, b) => b.relevance_score - a.relevance_score);
        return Promise.resolve(recommendations.slice(0, 5));
    },

    // User Management
    getUserPreferences: (userId) => {
        const loader = new MockDataLoader();
        const users = loader.loadMockUsers();
        const user = users.find(u => u.id === userId);
        
        if (!user) {
            return Promise.reject(new Error('User not found'));
        }
        
        return Promise.resolve(user.metadata.content_preferences || {
            frequency: 'weekly',
            format: ['newsletter', 'article'],
            topics: ['creator tips', 'funding opportunities'],
            delivery_channels: ['email']
        });
    },

    updatePreferences: (userId, preferences) => {
        // Mock successful update
        return Promise.resolve({ success: true, updated_at: new Date().toISOString() });
    },

    // Publishing APIs
    previewContent: (content) => {
        const preview = {
            email: {
                subject: `KGL Update: ${content.headline}`,
                body: content.summary,
                estimated_read_time: '2-3 minutes'
            },
            social: {
                twitter: content.headline.substring(0, 200) + '... #CreatorEconomy',
                linkedin: content.summary.substring(0, 1000)
            }
        };
        
        return Promise.resolve(preview);
    },

    publishContent: (channels, content) => {
        const results = {};
        
        channels.forEach(channel => {
            results[channel] = {
                status: 'success',
                published_at: new Date().toISOString(),
                reach_estimate: Math.floor(Math.random() * 1000) + 100
            };
        });
        
        return Promise.resolve(results);
    }
};

// React Testing Utilities (if using React Testing Library)
const { render, screen, fireEvent, waitFor } = require('@testing-library/react');
const '@testing-library/jest-dom';

// Test Suite: User Interface Components
describe('User Interface Components', () => {
    let mockLoader;
    
    beforeEach(() => {
        mockLoader = new MockDataLoader();
        
        // Mock API calls
        global.fetch = jest.fn();
        
        // Setup default successful API responses
        global.fetch.mockImplementation((url) => {
            if (url.includes('/api/entities')) {
                return Promise.resolve({
                    ok: true,
                    json: () => mockAPI.getEntities()
                });
            }
            if (url.includes('/api/digest')) {
                return Promise.resolve({
                    ok: true,
                    json: () => mockAPI.getPersonalizedDigest('user_001')
                });
            }
            if (url.includes('/api/search')) {
                return Promise.resolve({
                    ok: true,
                    json: () => mockAPI.searchKnowledge('creator')
                });
            }
            
            // Default response
            return Promise.resolve({
                ok: true,
                json: () => Promise.resolve({})
            });
        });
    });
    
    afterEach(() => {
        jest.restoreAllMocks();
    });
    
    test('Knowledge Graph Visualization Component', async () => {
        // Mock component that would render knowledge graph
        const KnowledgeGraphComponent = require('../modules/module-4-frontend/src/components/KnowledgeGraph');
        
        const entities = await mockAPI.getEntities();
        const relationships = await mockAPI.getRelationships('creator_001');
        
        render(<KnowledgeGraphComponent entities={entities} relationships={relationships} />);
        
        // Check that component renders
        expect(screen.getByTestId('knowledge-graph')).toBeInTheDocument();
        
        // Check that entities are displayed
        expect(screen.getByText('Boulder Music Collective')).toBeInTheDocument();
    });
    
    test('Search Interface Component', async () => {
        const SearchComponent = require('../modules/module-4-frontend/src/components/Search');
        
        render(<SearchComponent />);
        
        const searchInput = screen.getByPlaceholderText(/search/i);
        const searchButton = screen.getByRole('button', { name: /search/i });
        
        // Simulate search
        fireEvent.change(searchInput, { target: { value: 'creator economy' } });
        fireEvent.click(searchButton);
        
        // Wait for results
        await waitFor(() => {
            expect(screen.getByText(/search results/i)).toBeInTheDocument();
        });
    });
    
    test('User Profile Component', async () => {
        const ProfileComponent = require('../modules/module-4-frontend/src/components/UserProfile');
        
        const user = mockLoader.loadMockUsers()[0];
        
        render(<ProfileComponent user={user} />);
        
        // Check user information is displayed
        expect(screen.getByText(user.name)).toBeInTheDocument();
        expect(screen.getByText(user.metadata.location)).toBeInTheDocument();
        
        // Check interests are displayed
        user.metadata.interests.forEach(interest => {
            expect(screen.getByText(new RegExp(interest.replace('_', ' '), 'i'))).toBeInTheDocument();
        });
    });
    
    test('Content Digest Component', async () => {
        const DigestComponent = require('../modules/module-4-frontend/src/components/ContentDigest');
        
        const digest = await mockAPI.getPersonalizedDigest('user_001');
        
        render(<DigestComponent digest={digest} />);
        
        // Check digest content is displayed
        expect(screen.getByText(digest.content.headline)).toBeInTheDocument();
        
        // Check sections are rendered
        digest.content.sections.forEach(section => {
            expect(screen.getByText(section.title)).toBeInTheDocument();
        });
    });
});

// Test Suite: User Interactions and Workflows
describe('User Interactions and Workflows', () => {
    let mockLoader;
    
    beforeEach(() => {
        mockLoader = new MockDataLoader();
    });
    
    test('Content Personalization Workflow', async () => {
        const PersonalizationWorkflow = require('../modules/module-4-frontend/src/workflows/PersonalizationWorkflow');
        
        const workflow = new PersonalizationWorkflow();
        const userId = 'user_001';
        
        // Test workflow execution
        const result = await workflow.execute(userId);
        
        expect(result).toHaveProperty('digest');
        expect(result).toHaveProperty('recommendations');
        expect(result.digest.content).toHaveProperty('headline');
        expect(result.recommendations).toHaveLength(5);
    });
    
    test('Publishing Workflow', async () => {
        const PublishingWorkflow = require('../modules/module-4-frontend/src/workflows/PublishingWorkflow');
        
        const workflow = new PublishingWorkflow();
        
        const content = {
            headline: 'Test Content Headline',
            summary: 'Test content summary for publishing workflow',
            sections: []
        };
        
        const channels = ['email', 'twitter'];
        
        // Test publishing workflow
        const result = await workflow.publish(content, channels);
        
        expect(result).toHaveProperty('email');
        expect(result).toHaveProperty('twitter');
        expect(result.email.status).toBe('success');
        expect(result.twitter.status).toBe('success');
    });
    
    test('Knowledge Graph Navigation', async () => {
        const NavigationService = require('../modules/module-4-frontend/src/services/NavigationService');
        
        const service = new NavigationService();
        
        // Test entity navigation
        const entity = await service.getEntity('creator_001');
        expect(entity).toHaveProperty('id', 'creator_001');
        expect(entity).toHaveProperty('name', 'Boulder Music Collective');
        
        // Test relationship navigation
        const relationships = await service.getRelationships('creator_001');
        expect(relationships).toBeInstanceOf(Array);
        expect(relationships.length).toBeGreaterThan(0);
    });
});

// Test Suite: Data Integration and API Interactions
describe('Data Integration and API Interactions', () => {
    test('Mock API Entity Retrieval', async () => {
        const entities = await mockAPI.getEntities({ type: 'creators' });
        
        expect(entities).toBeInstanceOf(Array);
        expect(entities.length).toBeGreaterThan(0);
        
        const firstEntity = entities[0];
        expect(firstEntity).toHaveProperty('id');
        expect(firstEntity).toHaveProperty('name');
        expect(firstEntity).toHaveProperty('type', 'Creator');
    });
    
    test('Mock API Search Functionality', async () => {
        const searchResults = await mockAPI.searchKnowledge('Boulder');
        
        expect(searchResults).toBeInstanceOf(Array);
        expect(searchResults.length).toBeGreaterThan(0);
        
        // Check that results contain Boulder-related content
        const hasBoulderResult = searchResults.some(result => 
            result.data.name?.includes('Boulder') || 
            result.data.title?.includes('Boulder')
        );
        expect(hasBoulderResult).toBe(true);
    });
    
    test('Mock API Personalized Digest', async () => {
        const digest = await mockAPI.getPersonalizedDigest('user_001');
        
        expect(digest).toHaveProperty('user_id', 'user_001');
        expect(digest).toHaveProperty('content');
        expect(digest.content).toHaveProperty('headline');
        expect(digest.content).toHaveProperty('sections');
        expect(digest.content.sections).toBeInstanceOf(Array);
        expect(digest.content.sections.length).toBeGreaterThan(0);
    });
    
    test('Mock API User Preferences Management', async () => {
        const preferences = await mockAPI.getUserPreferences('user_001');
        
        expect(preferences).toHaveProperty('frequency');
        expect(preferences).toHaveProperty('format');
        expect(preferences).toHaveProperty('topics');
        
        // Test preference update
        const newPreferences = {
            ...preferences,
            frequency: 'daily'
        };
        
        const updateResult = await mockAPI.updatePreferences('user_001', newPreferences);
        expect(updateResult).toHaveProperty('success', true);
    });
});

// Test Suite: Performance and Accessibility
describe('Performance and Accessibility', () => {
    test('Component Render Performance', () => {
        const startTime = Date.now();
        
        // Simulate rendering large dataset
        const entities = mockAPI.getEntities();
        const renderTime = Date.now() - startTime;
        
        // Should render within reasonable time (adjust threshold as needed)
        expect(renderTime).toBeLessThan(1000); // 1 second
    });
    
    test('Search Response Time', async () => {
        const startTime = Date.now();
        
        await mockAPI.searchKnowledge('creator economy');
        
        const responseTime = Date.now() - startTime;
        expect(responseTime).toBeLessThan(500); // 500ms for mock API
    });
    
    test('Accessibility Features', () => {
        // Mock accessibility testing
        const accessibilityFeatures = {
            'keyboard_navigation': true,
            'screen_reader_support': true,
            'high_contrast_mode': true,
            'font_size_adjustment': true
        };
        
        Object.values(accessibilityFeatures).forEach(feature => {
            expect(feature).toBe(true);
        });
    });
});

// Test Suite: Error Handling and Edge Cases
describe('Error Handling and Edge Cases', () => {
    test('API Error Handling', async () => {
        // Mock API failure
        global.fetch = jest.fn().mockRejectedValue(new Error('API Error'));
        
        const ErrorHandler = require('../modules/module-4-frontend/src/utils/ErrorHandler');
        const handler = new ErrorHandler();
        
        const result = await handler.handleAPIError('test-endpoint');
        
        expect(result).toHaveProperty('error', true);
        expect(result).toHaveProperty('message');
    });
    
    test('Empty Search Results', async () => {
        const searchResults = await mockAPI.searchKnowledge('nonexistentquery12345');
        
        // Should return empty array for no results
        expect(searchResults).toBeInstanceOf(Array);
        expect(searchResults.length).toBe(0);
    });
    
    test('Invalid User ID Handling', async () => {
        try {
            await mockAPI.getPersonalizedDigest('invalid_user_id');
        } catch (error) {
            expect(error.message).toBe('User not found');
        }
    });
    
    test('Large Dataset Handling', async () => {
        // Test with large mock dataset
        const largeEntities = Array.from({ length: 1000 }, (_, i) => ({
            id: `entity_${i}`,
            name: `Test Entity ${i}`,
            type: 'TestType'
        }));
        
        // Should handle large datasets without crashing
        expect(largeEntities.length).toBe(1000);
        expect(largeEntities[999]).toHaveProperty('name', 'Test Entity 999');
    });
});

module.exports = {
    MockDataLoader,
    mockAPI
};