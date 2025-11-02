#!/usr/bin/env python3
"""
Manus Agent System - Installation Verification Script
Checks that all required files are present and properly configured
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    exists = Path(filepath).exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    required_text = "(required)" if required else "(optional)"
    print(f"{status} {filepath} {required_text}")
    return exists

def check_directory_exists(dirpath):
    """Check if a directory exists"""
    exists = Path(dirpath).is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {dirpath}/")
    return exists

def main():
    """Run verification checks"""
    print("🔍 Manus Agent System - Installation Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check core files
    print("📄 Core Files:")
    core_files = [
        "app/main.py",
        "app/config.py",
        "requirements.txt",
        "README.md",
        "DEPLOYMENT_GUIDE.md"
    ]
    for f in core_files:
        if not check_file_exists(f):
            all_good = False
    print()
    
    # Check agents
    print("🤖 Agent Files:")
    agent_files = [
        "app/agents/orchestrator.py",
        "app/agents/news_agent.py",
        "app/agents/seo_agent.py",
        "app/agents/content_agent.py"
    ]
    for f in agent_files:
        if not check_file_exists(f):
            all_good = False
    print()
    
    # Check tools
    print("🔧 Tool Files:")
    tool_files = [
        "app/tools/base.py",
        "app/tools/news_fetch.py",
        "app/tools/web_scrape.py"
    ]
    for f in tool_files:
        if not check_file_exists(f):
            all_good = False
    print()
    
    # Check database
    print("🗄️ Database Files:")
    db_files = [
        "app/db/database.py",
        "app/models/models.py"
    ]
    for f in db_files:
        if not check_file_exists(f):
            all_good = False
    print()
    
    # Check API
    print("📡 API Files:")
    api_files = [
        "app/api/routes.py",
        "app/services/llm_service.py"
    ]
    for f in api_files:
        if not check_file_exists(f):
            all_good = False
    print()
    
    # Check deployment
    print("🚀 Deployment Files:")
    deploy_files = [
        "Dockerfile",
        "render.yaml",
        ".env.example"
    ]
    for f in deploy_files:
        if not check_file_exists(f):
            all_good = False
    print()
    
    # Check optional files
    print("📚 Documentation Files:")
    doc_files = [
        "PROJECT_OVERVIEW.md",
        "QUICK_REFERENCE.md",
        "GETTING_STARTED.md"
    ]
    for f in doc_files:
        check_file_exists(f, required=False)
    print()
    
    # Check directories
    print("📁 Required Directories:")
    directories = [
        "app",
        "app/agents",
        "app/api",
        "app/db",
        "app/models",
        "app/services",
        "app/tools",
        "app/workers",
        "app/jobs",
        "tests",
        "scripts"
    ]
    for d in directories:
        if not check_directory_exists(d):
            all_good = False
    print()
    
    # Check .env file
    print("⚙️ Configuration:")
    if Path(".env").exists():
        print("✅ .env file found")
        # Check for required keys
        with open(".env") as f:
            content = f.read()
            has_openai = "OPENAI_API_KEY" in content and "sk-" in content
            has_anthropic = "ANTHROPIC_API_KEY" in content and "sk-ant-" in content
            
            if has_openai or has_anthropic:
                print("✅ API key configured")
            else:
                print("⚠️ No API key found in .env (add OPENAI_API_KEY or ANTHROPIC_API_KEY)")
    else:
        print("⚠️ .env file not found (copy from .env.example)")
        all_good = False
    print()
    
    # Final status
    print("=" * 60)
    if all_good:
        print("✅ Installation verification PASSED")
        print()
        print("🎉 You're ready to start!")
        print()
        print("Next steps:")
        print("1. Configure .env with your API keys")
        print("2. Run: ./start.sh (for local dev)")
        print("3. Or deploy to Render (see DEPLOYMENT_GUIDE.md)")
        return 0
    else:
        print("❌ Installation verification FAILED")
        print()
        print("Some files are missing. Please ensure you have:")
        print("1. Downloaded the complete manus-agent package")
        print("2. Extracted all files")
        print("3. Placed all files in the correct directories")
        return 1

if __name__ == "__main__":
    sys.exit(main())
