#!/bin/bash

# Manus Agent System - Pre-Deployment Verification Script
# Checks that all files are in place and configuration is correct

echo "🔍 Manus Agent System - Pre-Deployment Verification"
echo "===================================================="
echo ""

FAILED=0
PASSED=0

# Function to check file exists
check_file() {
    local file=$1
    local description=$2
    if [ -f "$file" ]; then
        echo "✅ $description"
        ((PASSED++))
    else
        echo "❌ $description - MISSING: $file"
        ((FAILED++))
    fi
}

# Function to check directory exists
check_dir() {
    local dir=$1
    local description=$2
    if [ -d "$dir" ]; then
        echo "✅ $description"
        ((PASSED++))
    else
        echo "❌ $description - MISSING: $dir"
        ((FAILED++))
    fi
}

# Check core application files
echo "📁 Core Application Files:"
check_file "app/main.py" "FastAPI entry point"
check_file "app/config.py" "Configuration management"
check_file "app/api/routes.py" "API routes"
check_file "app/db/database.py" "Database configuration"
check_file "app/models/models.py" "Database models"
check_file "app/services/llm_service.py" "LLM service"
echo ""

# Check agent files
echo "🤖 Agent Files:"
check_file "app/agents/orchestrator.py" "Orchestrator agent"
check_file "app/agents/news_agent.py" "News agent"
check_file "app/agents/seo_agent.py" "SEO agent"
check_file "app/agents/content_agent.py" "Content agent"
echo ""

# Check tool files
echo "🔧 Tool Files:"
check_file "app/tools/base.py" "Base tool class"
check_file "app/tools/news_fetch.py" "News fetching tool"
echo ""

# Check configuration files
echo "⚙️  Configuration Files:"
check_file "requirements.txt" "Python dependencies"
check_file "render.yaml" "Render deployment config"
check_file "vercel.json" "Vercel deployment config"
check_file "Procfile" "Process definitions"
check_file "runtime.txt" "Python version specification"
check_file ".env.example" "Environment template"
echo ""

# Check documentation
echo "📚 Documentation Files:"
check_file "README.md" "Main documentation"
check_file "DEPLOYMENT_GUIDE.md" "Deployment guide"
check_file "PROJECT_OVERVIEW.md" "Project overview"
check_file "AUDIT_REPORT.md" "Audit report"
check_file "DEPLOYMENT_CHECKLIST.md" "Deployment checklist"
check_file "AUDIT_AND_DEPLOYMENT_SUMMARY.md" "Audit summary"
echo ""

# Check directories
echo "📂 Directory Structure:"
check_dir "app" "Application directory"
check_dir "app/agents" "Agents directory"
check_dir "app/api" "API directory"
check_dir "app/db" "Database directory"
check_dir "app/models" "Models directory"
check_dir "app/services" "Services directory"
check_dir "app/tools" "Tools directory"
echo ""

# Check for duplicate files (should NOT exist)
echo "🚫 Checking for Duplicate Files (should not exist):"
if [ ! -f "routes.py" ]; then
    echo "✅ No duplicate routes.py in root"
    ((PASSED++))
else
    echo "❌ Found duplicate routes.py in root - should be deleted"
    ((FAILED++))
fi

if [ ! -f "content_agent.py" ]; then
    echo "✅ No duplicate content_agent.py in root"
    ((PASSED++))
else
    echo "❌ Found duplicate content_agent.py in root - should be deleted"
    ((FAILED++))
fi
echo ""

# Check Git status
echo "📦 Git Repository Status:"
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "✅ Git repository initialized"
    ((PASSED++))
    
    if [ -z "$(git status --porcelain)" ]; then
        echo "✅ Working tree clean (no uncommitted changes)"
        ((PASSED++))
    else
        echo "⚠️  Uncommitted changes detected:"
        git status --short
    fi
else
    echo "❌ Not a git repository"
    ((FAILED++))
fi
echo ""

# Check Python syntax
echo "🐍 Python Syntax Check (sampling):"
if python3 -m py_compile app/main.py 2>/dev/null; then
    echo "✅ app/main.py - syntax OK"
    ((PASSED++))
else
    echo "❌ app/main.py - syntax error"
    ((FAILED++))
fi

if python3 -m py_compile app/config.py 2>/dev/null; then
    echo "✅ app/config.py - syntax OK"
    ((PASSED++))
else
    echo "❌ app/config.py - syntax error"
    ((FAILED++))
fi
echo ""

# Check requirements.txt
echo "📋 Dependency Check:"
if grep -q "fastapi" requirements.txt && grep -q "uvicorn" requirements.txt; then
    echo "✅ Core dependencies present"
    ((PASSED++))
else
    echo "❌ Missing core dependencies"
    ((FAILED++))
fi

if grep -q "sqlalchemy" requirements.txt && grep -q "psycopg2" requirements.txt; then
    echo "✅ Database dependencies present"
    ((PASSED++))
else
    echo "❌ Missing database dependencies"
    ((FAILED++))
fi

if grep -q "openai\|anthropic" requirements.txt; then
    echo "✅ LLM dependencies present"
    ((PASSED++))
else
    echo "❌ Missing LLM dependencies"
    ((FAILED++))
fi
echo ""

# Summary
echo "===================================================="
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo "===================================================="
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 All checks passed! System is ready for deployment."
    echo ""
    echo "Next steps:"
    echo "1. Review DEPLOYMENT_CHECKLIST.md"
    echo "2. Ensure you have API keys ready"
    echo "3. Push to GitHub: git push origin main"
    echo "4. Deploy to Render.com following the checklist"
    exit 0
else
    echo "⚠️  Some checks failed. Please review the issues above."
    echo ""
    echo "Common issues:"
    echo "- Missing files: Verify you've downloaded the complete package"
    echo "- Duplicate files: Delete routes.py and content_agent.py from root"
    echo "- Syntax errors: Review Python files for errors"
    echo "- Missing dependencies: Update requirements.txt"
    exit 1
fi
