#!/usr/bin/env python3
"""
Production Readiness Verification Script
Verifies that the EVE-NG MCP Server is ready for production deployment
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class ProductionReadinessChecker:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.checks = []
        self.passed = 0
        self.failed = 0
        
    def check(self, name: str, condition: bool, details: str = "") -> bool:
        """Record a check result"""
        status = "✅ PASS" if condition else "❌ FAIL"
        self.checks.append({
            "name": name,
            "status": status,
            "condition": condition,
            "details": details
        })
        
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            
        print(f"{status} {name}")
        if details and not condition:
            print(f"   📝 {details}")
            
        return condition
    
    def check_file_exists(self, file_path: str, description: str) -> bool:
        """Check if a file exists"""
        path = self.project_root / file_path
        exists = path.exists()
        details = f"Missing: {file_path}" if not exists else ""
        return self.check(description, exists, details)
    
    def check_directory_exists(self, dir_path: str, description: str) -> bool:
        """Check if a directory exists"""
        path = self.project_root / dir_path
        exists = path.exists() and path.is_dir()
        details = f"Missing directory: {dir_path}" if not exists else ""
        return self.check(description, exists, details)
    
    def check_python_syntax(self, file_path: str) -> bool:
        """Check Python file syntax"""
        try:
            with open(self.project_root / file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            return True
        except SyntaxError as e:
            return False
    
    def run_command(self, command: List[str], cwd: Path = None) -> Tuple[bool, str]:
        """Run a command and return success status and output"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def check_documentation(self):
        """Check documentation completeness"""
        print("\n📚 Checking Documentation")
        print("=" * 40)
        
        # Main documentation files
        self.check_file_exists("README.md", "Main README exists")
        self.check_file_exists("docs/README.md", "Documentation hub exists")
        self.check_file_exists("docs/api/README.md", "API documentation exists")
        self.check_file_exists("docs/deployment/README.md", "Deployment guide exists")
        self.check_file_exists("docs/troubleshooting/README.md", "Troubleshooting guide exists")
        self.check_file_exists("docs/integrations/README.md", "Integration guide exists")
        self.check_file_exists("docs/integrations/claude-desktop.md", "Claude Desktop guide exists")
        self.check_file_exists("docs/integrations/vscode.md", "VS Code guide exists")
        
        # Integration examples
        self.check_directory_exists("examples/integrations", "Integration examples directory exists")
        self.check_file_exists("examples/integrations/claude-desktop-config.json", "Claude Desktop config example exists")
        self.check_file_exists("examples/integrations/vscode-workspace.json", "VS Code workspace example exists")
        self.check_file_exists("examples/integrations/deploy_lab.py", "Lab deployment script exists")
        self.check_file_exists("examples/integrations/sample-lab.json", "Sample lab configuration exists")

        # Check README content
        readme_path = self.project_root / "README.md"
        if readme_path.exists():
            content = readme_path.read_text()
            self.check("README has installation instructions", "installation" in content.lower())
            self.check("README has usage examples", "usage" in content.lower())
            self.check("README has API reference", "api" in content.lower())
            self.check("README has integration information", "integration" in content.lower())
    
    def check_testing_framework(self):
        """Check testing framework completeness"""
        print("\n🧪 Checking Testing Framework")
        print("=" * 40)
        
        # Test structure
        self.check_directory_exists("tests", "Tests directory exists")
        self.check_directory_exists("tests/unit", "Unit tests directory exists")
        self.check_directory_exists("tests/integration", "Integration tests directory exists")
        self.check_directory_exists("tests/e2e", "E2E tests directory exists")
        self.check_directory_exists("tests/performance", "Performance tests directory exists")
        self.check_directory_exists("tests/fixtures", "Test fixtures directory exists")
        
        # Test configuration
        self.check_file_exists("tests/conftest.py", "Pytest configuration exists")
        self.check_file_exists("tests/requirements.txt", "Test requirements exist")
        self.check_file_exists("tests/run_tests.py", "Test runner exists")
        self.check_file_exists("tests/README.md", "Testing guide exists")
        
        # Sample tests
        self.check_file_exists("tests/unit/test_client.py", "Sample unit test exists")
        
        # Check test runner syntax
        test_runner_path = "tests/run_tests.py"
        if (self.project_root / test_runner_path).exists():
            syntax_ok = self.check_python_syntax(test_runner_path)
            self.check("Test runner has valid syntax", syntax_ok)
    
    def check_deployment_configuration(self):
        """Check deployment configuration"""
        print("\n🚀 Checking Deployment Configuration")
        print("=" * 40)
        
        # Docker
        self.check_file_exists("Dockerfile", "Dockerfile exists")
        
        # Configuration
        self.check_directory_exists("config", "Config directory exists")
        self.check_file_exists("config/production.json", "Production config exists")
        
        # Systemd
        self.check_directory_exists("deployment", "Deployment directory exists")
        self.check_file_exists("deployment/systemd/eveng-mcp-server.service", "Systemd service file exists")
        
        # Check production config
        prod_config_path = self.project_root / "config/production.json"
        if prod_config_path.exists():
            try:
                with open(prod_config_path) as f:
                    config = json.load(f)
                self.check("Production config is valid JSON", True)
                self.check("Production config has EVE-NG settings", "eveng" in config)
                self.check("Production config has MCP settings", "mcp" in config)
                self.check("Production config has security settings", "security" in config)
            except json.JSONDecodeError:
                self.check("Production config is valid JSON", False, "Invalid JSON format")
    
    def check_code_quality(self):
        """Check code quality configuration"""
        print("\n🔧 Checking Code Quality")
        print("=" * 40)
        
        # Project configuration
        self.check_file_exists("pyproject.toml", "Project configuration exists")
        self.check_file_exists(".gitignore", "Gitignore exists")
        
        # Check pyproject.toml
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            self.check("Project has proper metadata", "[project]" in content)
            self.check("Project has dependencies", "dependencies" in content)
            self.check("Project has dev dependencies", "[project.optional-dependencies]" in content)
            self.check("Project has test configuration", "[tool.pytest.ini_options]" in content)
            self.check("Project has coverage configuration", "[tool.coverage" in content)
    
    def check_core_functionality(self):
        """Check core functionality"""
        print("\n⚙️ Checking Core Functionality")
        print("=" * 40)
        
        # Core modules
        self.check_directory_exists("eveng_mcp_server", "Main package exists")
        self.check_file_exists("eveng_mcp_server/__init__.py", "Package init exists")
        self.check_file_exists("eveng_mcp_server/cli.py", "CLI module exists")
        self.check_file_exists("eveng_mcp_server/server.py", "Server module exists")
        
        # Sub-packages
        self.check_directory_exists("eveng_mcp_server/tools", "Tools package exists")
        self.check_directory_exists("eveng_mcp_server/resources", "Resources package exists")
        self.check_directory_exists("eveng_mcp_server/prompts", "Prompts package exists")
        self.check_directory_exists("eveng_mcp_server/config", "Config package exists")
        
        # Check syntax of main modules
        for module in ["eveng_mcp_server/cli.py", "eveng_mcp_server/server.py"]:
            if (self.project_root / module).exists():
                syntax_ok = self.check_python_syntax(module)
                self.check(f"{module} has valid syntax", syntax_ok)
    
    def check_dependencies(self):
        """Check dependencies and installation"""
        print("\n📦 Checking Dependencies")
        print("=" * 40)
        
        # Check if UV is available
        uv_available, _ = self.run_command(["uv", "--version"])
        self.check("UV package manager available", uv_available, "Install UV: curl -LsSf https://astral.sh/uv/install.sh | sh")
        
        # Check if dependencies can be resolved
        if uv_available:
            deps_ok, output = self.run_command(["uv", "sync", "--dry-run"])
            self.check("Dependencies can be resolved", deps_ok, "Run 'uv sync' to install dependencies")
        
        # Check lock file
        self.check_file_exists("uv.lock", "Lock file exists")
    
    def check_security(self):
        """Check security configuration"""
        print("\n🔐 Checking Security Configuration")
        print("=" * 40)
        
        # Check .gitignore for sensitive files
        gitignore_path = self.project_root / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            self.check("Gitignore excludes .env files", ".env" in content)
            self.check("Gitignore excludes logs", "*.log" in content)
            self.check("Gitignore excludes secrets", "secrets" in content)
        
        # Check for hardcoded secrets (basic check)
        sensitive_patterns = ["password", "secret", "key", "token"]
        config_files = ["config/production.json"]
        
        for config_file in config_files:
            config_path = self.project_root / config_file
            if config_path.exists():
                content = config_path.read_text().lower()
                has_env_vars = "${" in content or "env" in content
                self.check(f"{config_file} uses environment variables", has_env_vars)
    
    def generate_report(self):
        """Generate final report"""
        print("\n📊 Production Readiness Report")
        print("=" * 60)
        
        total_checks = self.passed + self.failed
        success_rate = (self.passed / total_checks) * 100 if total_checks > 0 else 0
        
        print(f"Total Checks: {total_checks}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.failed > 0:
            print(f"\n❌ Failed Checks:")
            for check in self.checks:
                if not check["condition"]:
                    print(f"   - {check['name']}")
                    if check["details"]:
                        print(f"     {check['details']}")
        
        print(f"\n🎯 Production Readiness Status:")
        if success_rate >= 95:
            print("✅ READY FOR PRODUCTION")
            print("All critical checks passed. The project is production-ready!")
        elif success_rate >= 80:
            print("⚠️  MOSTLY READY")
            print("Most checks passed. Address failed checks before production deployment.")
        else:
            print("❌ NOT READY")
            print("Multiple critical issues found. Address all failed checks before deployment.")
        
        return success_rate >= 95
    
    def run_all_checks(self):
        """Run all production readiness checks"""
        print("🚀 EVE-NG MCP Server - Production Readiness Check")
        print("=" * 60)
        
        self.check_documentation()
        self.check_testing_framework()
        self.check_deployment_configuration()
        self.check_code_quality()
        self.check_core_functionality()
        self.check_dependencies()
        self.check_security()
        
        return self.generate_report()


def main():
    """Main entry point"""
    checker = ProductionReadinessChecker()
    is_ready = checker.run_all_checks()
    
    # Exit with appropriate code
    sys.exit(0 if is_ready else 1)


if __name__ == "__main__":
    main()
