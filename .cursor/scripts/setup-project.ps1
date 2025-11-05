# SpecKit Project Setup Script for Cursor
# This script sets up a new project with SpecKit integration

param(
    [string]$ProjectName = "New Project",
    [string]$ProjectPath = ".",
    [switch]$Force = $false
)

Write-Host "Setting up SpecKit project: $ProjectName" -ForegroundColor Green

# Check if .cursor directory exists
if (Test-Path ".cursor") {
    if (-not $Force) {
        Write-Host "Error: .cursor directory already exists. Use -Force to overwrite." -ForegroundColor Red
        exit 1
    }
    Write-Host "Removing existing .cursor directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".cursor"
}

# Create directory structure
Write-Host "Creating directory structure..." -ForegroundColor Blue
New-Item -ItemType Directory -Force -Path ".cursor/commands" | Out-Null
New-Item -ItemType Directory -Force -Path ".cursor/scripts" | Out-Null
New-Item -ItemType Directory -Force -Path "memory" | Out-Null

# Create constitution if it doesn't exist
$constitutionPath = "memory/constitution.md"
if (-not (Test-Path $constitutionPath)) {
    Write-Host "Creating project constitution..." -ForegroundColor Blue
    $constitution = @"
# Project Constitution: $ProjectName

## Vision
[Define your project vision here]

## Values
- Quality: Deliver high-quality, reliable software
- Innovation: Embrace new technologies and approaches
- Transparency: Open communication and decision-making
- Collaboration: Work together effectively as a team

## Operating Principles
- Spec-Driven Development: Plan before implementing
- Test-First Approach: Write tests before code
- Continuous Integration: Regular integration and testing
- Incremental Delivery: Deliver value in small increments

## Quality Standards
- All code must have tests
- Specifications must be implementation-ready
- Documentation must be comprehensive and current
- Performance must meet defined targets

## Success Criteria
- [Define measurable success criteria]
"@

    $constitution | Out-File -FilePath $constitutionPath -Encoding UTF8
}

Write-Host "SpecKit project setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit memory/constitution.md with your project vision and values"
Write-Host "2. Use /speckit.constitution to establish project guidelines"
Write-Host "3. Use /speckit.specify to create specifications"
Write-Host "4. Use /speckit.plan to generate implementation plans"


