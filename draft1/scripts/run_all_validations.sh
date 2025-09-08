#!/bin/bash
"""
Master Validation Script for Knowledge Graph Lab
Runs all validation checks in sequence and provides comprehensive report.
"""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BOLD}${BLUE}🚀 Knowledge Graph Lab - Complete Validation Suite${NC}"
echo -e "Running all validation checks for intern onboarding readiness...\n"
echo -e "Project root: ${PROJECT_ROOT}"
echo -e "Timestamp: $(date)\n"

# Track results
TOTAL_CHECKS=4
PASSED_CHECKS=0
FAILED_CHECKS=0

# Function to run a validation and track results
run_validation() {
    local name="$1"
    local script="$2"
    local description="$3"
    
    echo -e "\n${BOLD}📋 $name${NC}"
    echo -e "   $description"
    echo -e "   Running: $script"
    echo -e "${YELLOW}${'='*60}${NC}"
    
    if python3 "$script"; then
        echo -e "${GREEN}✅ $name: PASSED${NC}"
        ((PASSED_CHECKS++))
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 1 ]; then
            echo -e "${YELLOW}⚠️  $name: PARTIAL (minor issues)${NC}"
            ((PASSED_CHECKS++))
        else
            echo -e "${RED}❌ $name: FAILED${NC}"
            ((FAILED_CHECKS++))
        fi
        return $exit_code
    fi
}

# Initialize results tracking
declare -A RESULTS
RESULTS[repository]=0
RESULTS[code]=0
RESULTS[health]=0
RESULTS[integration]=0

echo -e "\n${BOLD}Starting validation sequence...${NC}\n"

# 1. Repository Structure Validation
run_validation \
    "Repository Structure" \
    "$SCRIPT_DIR/validate_repository.py" \
    "Checking directory structure, documentation, and configuration files"
RESULTS[repository]=$?

# 2. Starter Code Validation
run_validation \
    "Starter Code Quality" \
    "$SCRIPT_DIR/validate_starter_code.py" \
    "Validating Python/Node.js code syntax, dependencies, and module structure"
RESULTS[code]=$?

# 3. System Health Check
run_validation \
    "System Health Check" \
    "$SCRIPT_DIR/health_check.py" \
    "Testing Docker services, API endpoints, and database connectivity"
RESULTS[health]=$?

# 4. Integration Test (if available)
if [ -f "$SCRIPT_DIR/test_integration.py" ]; then
    run_validation \
        "Integration Testing" \
        "$SCRIPT_DIR/test_integration.py" \
        "Running end-to-end integration tests"
    RESULTS[integration]=$?
else
    echo -e "\n${BOLD}📋 Integration Testing${NC}"
    echo -e "   End-to-end integration tests"
    echo -e "   ${YELLOW}⚠️  Integration test script not found (optional)${NC}"
    RESULTS[integration]=1
fi

# Calculate overall results
SUCCESS_RATE=$(( (PASSED_CHECKS * 100) / TOTAL_CHECKS ))

echo -e "\n\n${BOLD}📊 COMPREHENSIVE VALIDATION REPORT${NC}"
echo -e "${'='*80}"

# Individual Results
echo -e "\n${BOLD}Individual Check Results:${NC}"
for check in repository code health integration; do
    case ${RESULTS[$check]} in
        0) echo -e "  ${GREEN}✅ ${check^}: PASSED${NC}" ;;
        1) echo -e "  ${YELLOW}⚠️  ${check^}: PARTIAL${NC}" ;;
        *) echo -e "  ${RED}❌ ${check^}: FAILED${NC}" ;;
    esac
done

# Summary Statistics
echo -e "\n${BOLD}Summary Statistics:${NC}"
echo -e "  Total Checks: $TOTAL_CHECKS"
echo -e "  Passed/Partial: $PASSED_CHECKS"
echo -e "  Failed: $FAILED_CHECKS"
echo -e "  Success Rate: ${SUCCESS_RATE}%"

# Overall Assessment
echo -e "\n${BOLD}🎯 LAUNCH READINESS ASSESSMENT:${NC}"

if [ $FAILED_CHECKS -eq 0 ]; then
    if [ $SUCCESS_RATE -eq 100 ]; then
        echo -e "${GREEN}${BOLD}🎉 PERFECT! System is 100% ready for intern onboarding.${NC}"
        echo -e "${GREEN}   All systems operational, documentation complete, code quality excellent.${NC}"
        OVERALL_STATUS="READY"
        EXIT_CODE=0
    else
        echo -e "${YELLOW}${BOLD}✅ GOOD! System is ready with minor improvements recommended.${NC}"
        echo -e "${YELLOW}   All critical systems working, some optimization opportunities identified.${NC}"
        OVERALL_STATUS="READY_WITH_NOTES"
        EXIT_CODE=0
    fi
elif [ $FAILED_CHECKS -eq 1 ]; then
    echo -e "${YELLOW}${BOLD}⚠️  MOSTLY READY! One area needs attention but launch can proceed.${NC}"
    echo -e "${YELLOW}   Consider addressing the failed check but intern onboarding can start.${NC}"
    OVERALL_STATUS="CAUTION"
    EXIT_CODE=1
else
    echo -e "${RED}${BOLD}🚨 NOT READY! Multiple critical issues must be resolved before launch.${NC}"
    echo -e "${RED}   Address failed checks before intern onboarding begins.${NC}"
    OVERALL_STATUS="BLOCKED"
    EXIT_CODE=2
fi

# Detailed Recommendations
echo -e "\n${BOLD}📋 NEXT STEPS & RECOMMENDATIONS:${NC}"

case $OVERALL_STATUS in
    "READY")
        echo -e "${GREEN}1. ✅ Proceed with intern onboarding as planned${NC}"
        echo -e "${GREEN}2. ✅ All systems are operational and documented${NC}"
        echo -e "${GREEN}3. ✅ Monitor setup process on Day 1 for any edge cases${NC}"
        ;;
    "READY_WITH_NOTES")
        echo -e "${YELLOW}1. ✅ Proceed with intern onboarding${NC}"
        echo -e "${YELLOW}2. ⚠️  Review warnings from validation checks${NC}"
        echo -e "${YELLOW}3. ✅ Address minor issues during Week 1 if needed${NC}"
        ;;
    "CAUTION")
        echo -e "${YELLOW}1. ⚠️  Review the failed validation check carefully${NC}"
        echo -e "${YELLOW}2. ⚠️  Consider if the issue will block intern progress${NC}"
        echo -e "${YELLOW}3. ✅ Proceed if workarounds are available${NC}"
        ;;
    "BLOCKED")
        echo -e "${RED}1. 🚨 Do not start intern onboarding yet${NC}"
        echo -e "${RED}2. 🚨 Address all failed validation checks${NC}"
        echo -e "${RED}3. 🚨 Re-run validations after fixes${NC}"
        ;;
esac

# Time and Resource Estimates
echo -e "\n${BOLD}⏱️  ESTIMATED RESOLUTION TIME:${NC}"
if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "  Ready now - no action required"
elif [ $FAILED_CHECKS -eq 1 ]; then
    echo -e "  1-3 hours to address remaining issues"
else
    echo -e "  4-8 hours to resolve all critical issues"
fi

# Save results for monitoring
RESULTS_FILE="$PROJECT_ROOT/validation_results.json"
cat > "$RESULTS_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "overall_status": "$OVERALL_STATUS",
    "success_rate": $SUCCESS_RATE,
    "total_checks": $TOTAL_CHECKS,
    "passed_checks": $PASSED_CHECKS,
    "failed_checks": $FAILED_CHECKS,
    "individual_results": {
        "repository": ${RESULTS[repository]},
        "code": ${RESULTS[code]},
        "health": ${RESULTS[health]},
        "integration": ${RESULTS[integration]}
    },
    "exit_code": $EXIT_CODE
}
EOF

echo -e "\n${BLUE}ℹ️  Detailed results saved to: validation_results.json${NC}"
echo -e "${BLUE}ℹ️  Re-run this script after making changes: ./scripts/run_all_validations.sh${NC}"

# Footer
echo -e "\n${'='*80}"
echo -e "${BOLD}Knowledge Graph Lab Validation Suite Complete${NC}"
echo -e "For support: Check troubleshooting guide or contact project team"

exit $EXIT_CODE