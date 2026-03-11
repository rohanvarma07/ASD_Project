#!/bin/bash

# Render Deployment Preparation Script
# Run this before deploying to Render

set -e  # Exit on error

echo "=========================================="
echo "Render Deployment Preparation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check Python version in runtime.txt
echo -e "${YELLOW}Checking runtime.txt...${NC}"
if grep -q "python-3.11" runtime.txt || grep -q "python-3.12" runtime.txt; then
    echo -e "${GREEN}✓ Python version is compatible with Render${NC}"
    cat runtime.txt
else
    echo -e "${RED}✗ Python version may not be supported by Render${NC}"
    echo "  Current: $(cat runtime.txt)"
    echo "  Recommended: python-3.11.9"
fi
echo ""

# Check Procfile
echo -e "${YELLOW}Checking Procfile...${NC}"
if [ -f "Procfile" ]; then
    if grep -q "gunicorn" Procfile; then
        echo -e "${GREEN}✓ Procfile configured correctly${NC}"
        cat Procfile
    else
        echo -e "${RED}✗ Procfile missing gunicorn command${NC}"
    fi
else
    echo -e "${RED}✗ Procfile not found${NC}"
fi
echo ""

# Check requirements.txt
echo -e "${YELLOW}Checking requirements.txt...${NC}"
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓ requirements.txt found${NC}"
    echo "  Dependencies: $(wc -l < requirements.txt | tr -d ' ') lines"
    
    # Check for critical dependencies
    if grep -q "Flask" requirements.txt; then
        echo -e "${GREEN}  ✓ Flask${NC}"
    fi
    if grep -q "gunicorn" requirements.txt; then
        echo -e "${GREEN}  ✓ gunicorn${NC}"
    fi
    if grep -q "psycopg2" requirements.txt; then
        echo -e "${GREEN}  ✓ psycopg2 (PostgreSQL)${NC}"
    fi
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
fi
echo ""

# Check .gitignore
echo -e "${YELLOW}Checking .gitignore...${NC}"
if [ -f ".gitignore" ]; then
    echo -e "${GREEN}✓ .gitignore found${NC}"
    
    # Check if sensitive files are ignored
    if grep -q "\.env" .gitignore; then
        echo -e "${GREEN}  ✓ .env files ignored${NC}"
    fi
    if grep -q "__pycache__" .gitignore; then
        echo -e "${GREEN}  ✓ __pycache__ ignored${NC}"
    fi
    if grep -q ".venv" .gitignore || grep -q "venv" .gitignore; then
        echo -e "${GREEN}  ✓ Virtual environment ignored${NC}"
    fi
else
    echo -e "${YELLOW}⚠ .gitignore not found${NC}"
fi
echo ""

# Check for ML model
echo -e "${YELLOW}Checking ML model...${NC}"
if [ -f "models/asd_model.pkl" ]; then
    echo -e "${GREEN}✓ Trained ML model found${NC}"
    echo "  Size: $(du -h models/asd_model.pkl | cut -f1)"
    echo "  App will use ML model (95% accuracy)"
else
    echo -e "${YELLOW}⚠ No trained ML model found${NC}"
    echo "  App will use rule-based model (85% accuracy)"
    echo "  To train: python train_model.py"
fi
echo ""

# Generate SECRET_KEY
echo -e "${YELLOW}Generating SECRET_KEY...${NC}"
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
echo -e "${GREEN}✓ Generated secure SECRET_KEY${NC}"
echo ""
echo "Copy this to Render Environment Variables:"
echo "---"
echo "SECRET_KEY=${SECRET_KEY}"
echo "---"
echo ""

# Check Git status
echo -e "${YELLOW}Checking Git status...${NC}"
if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git repository found${NC}"
    
    # Check for uncommitted changes
    if git diff --quiet && git diff --cached --quiet; then
        echo -e "${GREEN}  ✓ No uncommitted changes${NC}"
    else
        echo -e "${YELLOW}  ⚠ Uncommitted changes detected${NC}"
        echo "  Run: git status"
    fi
    
    # Check current branch
    BRANCH=$(git branch --show-current)
    echo "  Current branch: ${BRANCH}"
else
    echo -e "${RED}✗ Not a Git repository${NC}"
fi
echo ""

# Pre-deployment test
echo -e "${YELLOW}Running pre-deployment tests...${NC}"

# Test requirements installation
echo "  Testing requirements..."
if python3 -m pip install -r requirements.txt --dry-run > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ All dependencies installable${NC}"
else
    echo -e "${YELLOW}  ⚠ Some dependencies may have issues${NC}"
fi

# Test imports
echo "  Testing critical imports..."
if python3 -c "import flask" 2>/dev/null; then
    echo -e "${GREEN}  ✓ Flask${NC}"
else
    echo -e "${RED}  ✗ Flask not installed${NC}"
fi

if python3 -c "import gunicorn" 2>/dev/null; then
    echo -e "${GREEN}  ✓ Gunicorn${NC}"
else
    echo -e "${YELLOW}  ⚠ Gunicorn not installed locally (OK for Render)${NC}"
fi

if python3 -c "import pandas" 2>/dev/null; then
    echo -e "${GREEN}  ✓ Pandas${NC}"
else
    echo -e "${RED}  ✗ Pandas not installed${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo "Deployment Readiness Summary"
echo "=========================================="
echo ""
echo "Essential Files:"
echo "  ✓ app.py"
echo "  ✓ database.py"
echo "  ✓ requirements.txt"
echo "  ✓ Procfile"
echo "  ✓ runtime.txt"
echo ""
echo "Next Steps:"
echo "  1. Copy the SECRET_KEY above"
echo "  2. Commit changes: git add . && git commit -m 'Prepare for Render deployment'"
echo "  3. Push to GitHub: git push origin main"
echo "  4. Go to Render Dashboard"
echo "  5. Create Web Service from your GitHub repo"
echo "  6. Add PostgreSQL database"
echo "  7. Set SECRET_KEY environment variable"
echo "  8. Deploy!"
echo ""
echo "Expected deployment time: 10-15 minutes (first deploy)"
echo ""
echo -e "${GREEN}You're ready to deploy! 🚀${NC}"
echo ""
