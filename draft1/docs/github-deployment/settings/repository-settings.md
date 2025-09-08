# GitHub Repository Settings Configuration

**Complete setup instructions for repository settings, branch protection, and security**

---

## Repository Settings

### General Settings
- **Repository Name**: `knowledge-graph-lab`
- **Description**: `AI-Powered Creator Economy Research Platform - 10-week intern development program`
- **Website**: `https://github.com/peermesh/knowledge-graph-lab` (can be updated with live demo)
- **Topics**: `ai`, `knowledge-graph`, `creator-economy`, `research-platform`, `internship`, `peermesh`
- **Visibility**: `Private` initially, can be made public for demo
- **Features to Enable**:
  - ✅ Issues
  - ✅ Projects  
  - ✅ Wiki
  - ✅ Discussions
  - ✅ Pull Requests
  - ✅ Actions (for CI/CD)

### Repository Permissions
- **Base permissions**: `Read` (default for organization members)
- **Admin access**: Project lead (Grig)
- **Write access**: All 4 interns (to be added when team is formed)
- **Maintain access**: Any additional mentors or reviewers

---

## Branch Protection Rules

### Main Branch Protection (`main`)

**Settings Path**: Settings → Branches → Add rule

#### Branch Protection Configuration
- **Branch name pattern**: `main`
- **Restrict pushes to matching branches**: ✅ Enabled

#### Protection Rules
- **Require a pull request before merging**: ✅ Enabled
  - **Require approvals**: 1 approval minimum
  - **Dismiss stale reviews**: ✅ Enabled
  - **Require review from code owners**: ✅ Enabled (once CODEOWNERS is configured)
  - **Allow specified actors to bypass**: Project lead only

- **Require status checks to pass**: ✅ Enabled (when CI/CD is set up)
  - **Require branches to be up to date**: ✅ Enabled
  - **Status checks**: Add when GitHub Actions are configured

- **Require conversation resolution**: ✅ Enabled
- **Require signed commits**: ❌ Disabled (optional for learning environment)
- **Require linear history**: ❌ Disabled (allow merge commits for learning)
- **Include administrators**: ❌ Disabled (allow admin override for urgent fixes)

### Development Branch Protection (`develop`)

**When Created**: Week 3 (when development starts)

#### Branch Protection Configuration
- **Branch name pattern**: `develop`
- **Require a pull request before merging**: ✅ Enabled
  - **Require approvals**: 1 approval from any team member
  - **Allow self-review**: ✅ Enabled (for learning environment)
- **Require status checks to pass**: ✅ Enabled
- **Include administrators**: ❌ Disabled

---

## Security Settings

### Code Security and Analysis

**Settings Path**: Settings → Security & analysis

#### Dependency Management
- **Dependency graph**: ✅ Enabled
- **Dependabot alerts**: ✅ Enabled
- **Dependabot security updates**: ✅ Enabled
- **Dependabot version updates**: ✅ Enabled (create `.github/dependabot.yml`)

#### Code Scanning
- **Code scanning**: ✅ Enable when first push is made
- **Secret scanning**: ✅ Enabled (GitHub Advanced Security feature)
- **Private vulnerability reporting**: ✅ Enabled

### Repository Security Advisories
- **Enable private vulnerability reporting**: ✅ Enabled
- **Security policy**: Link to `SECURITY.md` in root directory

---

## Collaborator Management

### Team Structure
1. **Project Lead** (Admin)
   - Full repository access
   - Can modify settings and permissions
   - Responsible for final approvals on main branch

2. **Intern Developers** (Write)
   - Can create branches and pull requests
   - Can merge approved PRs to develop branch
   - Cannot directly push to main branch

3. **Mentors/Reviewers** (Maintain)
   - Can approve pull requests
   - Can merge to main branch
   - Can modify issues and project boards

### Adding Collaborators
1. Go to Settings → Collaborators and teams
2. Click "Add people" or "Add teams"
3. Search by GitHub username or email
4. Select appropriate permission level
5. Send invitation

---

## Issue and PR Templates

### Current Template Status
- ✅ Issue templates configured (`.github/ISSUE_TEMPLATE/`)
- ✅ PR template configured (`.github/PULL_REQUEST_TEMPLATE.md`)
- ✅ Config file for issue routing (`.github/ISSUE_TEMPLATE/config.yml`)

### Additional Templates Needed
Create these files in `.github/` directory:

#### `.github/dependabot.yml`
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

#### `.github/CODEOWNERS`
```
# Global owners
* @peermesh/project-leads

# Module-specific ownership (update with intern GitHub usernames)
/modules/module-1-ingestion/ @backend-intern
/modules/module-2-knowledge-graph/ @ai-ml-intern  
/modules/module-3-content-synthesis/ @ai-logic-intern
/modules/module-4-frontend/ @frontend-intern

# Documentation
/docs/ @peermesh/project-leads
*.md @peermesh/project-leads
```

---

## GitHub Actions Configuration

### Workflow Files to Create

#### `.github/workflows/ci.yml`
```yaml
name: Continuous Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Run tests
      run: |
        pytest --cov=./ --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

#### `.github/workflows/security.yml`
```yaml
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly scan

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        format: 'sarif'
        output: 'trivy-results.sarif'
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
```

---

## Project Integration

### Link Repository to Project
1. Go to repository Settings → General
2. Scroll to "Features" section
3. Check "Projects" if not already enabled
4. Navigate to repository Projects tab
5. Link to "Knowledge Graph Lab - 10-Week Development" project

### Automate Issue Creation
- Issues created in repository automatically appear in project backlog
- Labels and milestones sync between repository and project
- PR status updates reflect in project board

---

## Notification and Integration Settings

### Email Notifications
- **Repository owner**: All notifications enabled
- **Team members**: Participating conversations and @mentions
- **Collaborators**: Choose "Not watching" to reduce noise, but enable @mentions

### Webhook Configuration (Optional)
For integration with external tools:
- **Slack/Discord**: Configure webhooks for PR and issue updates
- **Project management**: Connect to external time tracking or project tools

---

## Environment and Secrets Management

### Repository Secrets
Navigate to Settings → Secrets and variables → Actions

#### Required Secrets (to be added later)
- `OPENAI_API_KEY`: For AI/ML module development
- `CLAUDE_API_KEY`: Alternative AI provider
- `DATABASE_URL`: For production deployment
- `SENDGRID_API_KEY`: For email functionality

#### Environment Variables
Create `.env.example` file (already exists) with:
```
OPENAI_API_KEY=your_openai_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
DATABASE_URL=postgresql://localhost/knowledge_graph_lab
REDIS_URL=redis://localhost:6379
```

---

## Compliance and Documentation

### Required Repository Files
- ✅ `LICENSE` - Open source license (already exists)
- ✅ `README.md` - Project overview (already exists)
- ✅ `CONTRIBUTING.md` - Contribution guidelines (already exists)
- ✅ `SECURITY.md` - Security policy (already exists)
- ✅ `.gitignore` - Ignore patterns (already exists)
- 🔲 `CODE_OF_CONDUCT.md` - Community standards (to be created)
- 🔲 `CHANGELOG.md` - Version history (to be created)

### Documentation Standards
- All new features require documentation updates
- API changes require README updates
- Security considerations documented in SECURITY.md
- Breaking changes logged in CHANGELOG.md

---

## Quick Setup Checklist

### Immediate Setup (Project Lead)
- [ ] Configure branch protection for main branch
- [ ] Add team members as collaborators with appropriate permissions
- [ ] Enable security features (Dependabot, code scanning)
- [ ] Create CODEOWNERS file with team assignments
- [ ] Link repository to project board

### Week 1 Setup (After Team Formation)
- [ ] Add intern GitHub usernames to CODEOWNERS
- [ ] Create development branch protection rules
- [ ] Set up GitHub Actions workflows for CI/CD
- [ ] Configure notification preferences for team
- [ ] Test issue creation and project board integration

### Ongoing Maintenance
- [ ] Review and approve Dependabot updates weekly
- [ ] Monitor security alerts and address promptly
- [ ] Update branch protection rules as team grows
- [ ] Maintain CODEOWNERS accuracy with team changes

---

**Next Steps**: Apply these settings to the repository, then proceed with creating the initial issues and project board setup.