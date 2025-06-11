#!/usr/bin/env python3
"""
Main test runner for EVE-NG MCP Server
Orchestrates all test suites and generates comprehensive reports
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pytest


class TestRunner:
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.project_root = self.test_dir.parent
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    def setup_environment(self):
        """Setup test environment"""
        # Add project root to Python path
        sys.path.insert(0, str(self.project_root))
        
        # Set test environment variables
        os.environ.setdefault('TESTING', 'true')
        os.environ.setdefault('TEST_TIMEOUT', '30')
        os.environ.setdefault('TEST_RETRIES', '3')
        
    def run_unit_tests(self, coverage: bool = False, verbose: bool = False) -> Dict:
        """Run unit tests"""
        print("🧪 Running Unit Tests")
        print("=" * 50)
        
        cmd = [
            'pytest',
            str(self.test_dir / 'unit'),
            '--tb=short',
            '--durations=10'
        ]
        
        if coverage:
            cmd.extend([
                '--cov=eveng_mcp_server',
                '--cov-report=term-missing',
                '--cov-report=html:htmlcov',
                '--cov-report=json:coverage.json'
            ])
        
        if verbose:
            cmd.append('-v')
        
        # Add JUnit XML output
        cmd.extend(['--junitxml=test-results-unit.xml'])
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start_time
        
        return {
            'category': 'unit',
            'success': result.returncode == 0,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    
    def run_integration_tests(self, eveng_host: Optional[str] = None, 
                            eveng_user: Optional[str] = None,
                            eveng_pass: Optional[str] = None,
                            verbose: bool = False) -> Dict:
        """Run integration tests"""
        print("\n🔗 Running Integration Tests")
        print("=" * 50)
        
        cmd = [
            'pytest',
            str(self.test_dir / 'integration'),
            '--tb=short',
            '--durations=10'
        ]
        
        if verbose:
            cmd.append('-v')
        
        # Add EVE-NG connection parameters if provided
        if eveng_host:
            cmd.extend(['--eveng-host', eveng_host])
        if eveng_user:
            cmd.extend(['--eveng-user', eveng_user])
        if eveng_pass:
            cmd.extend(['--eveng-pass', eveng_pass])
        
        # Add JUnit XML output
        cmd.extend(['--junitxml=test-results-integration.xml'])
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start_time
        
        return {
            'category': 'integration',
            'success': result.returncode == 0,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    
    def run_e2e_tests(self, eveng_host: Optional[str] = None,
                     eveng_user: Optional[str] = None,
                     eveng_pass: Optional[str] = None,
                     verbose: bool = False) -> Dict:
        """Run end-to-end tests"""
        print("\n🎯 Running End-to-End Tests")
        print("=" * 50)
        
        cmd = [
            'pytest',
            str(self.test_dir / 'e2e'),
            '--tb=short',
            '--durations=10',
            '-m', 'not slow'  # Skip slow tests by default
        ]
        
        if verbose:
            cmd.append('-v')
        
        # Add EVE-NG connection parameters if provided
        if eveng_host:
            cmd.extend(['--eveng-host', eveng_host])
        if eveng_user:
            cmd.extend(['--eveng-user', eveng_user])
        if eveng_pass:
            cmd.extend(['--eveng-pass', eveng_pass])
        
        # Add JUnit XML output
        cmd.extend(['--junitxml=test-results-e2e.xml'])
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start_time
        
        return {
            'category': 'e2e',
            'success': result.returncode == 0,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    
    def run_performance_tests(self, verbose: bool = False) -> Dict:
        """Run performance tests"""
        print("\n⚡ Running Performance Tests")
        print("=" * 50)
        
        cmd = [
            'pytest',
            str(self.test_dir / 'performance'),
            '--tb=short',
            '--benchmark-only',
            '--benchmark-json=benchmark.json'
        ]
        
        if verbose:
            cmd.append('-v')
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start_time
        
        return {
            'category': 'performance',
            'success': result.returncode == 0,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    
    def run_mcp_inspector_tests(self) -> Dict:
        """Run MCP Inspector integration tests"""
        print("\n🔍 Running MCP Inspector Tests")
        print("=" * 50)
        
        # Run the existing MCP Inspector test script
        script_path = self.test_dir / 'integration' / 'test_mcp_inspector_integration.py'
        
        cmd = ['python', str(script_path)]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start_time
        
        return {
            'category': 'mcp_inspector',
            'success': result.returncode == 0,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    
    def run_legacy_tests(self) -> Dict:
        """Run legacy test scripts for compatibility"""
        print("\n🔄 Running Legacy Tests")
        print("=" * 50)
        
        legacy_scripts = [
            'working_demo.py',
            'test_mcp_http.py'
        ]
        
        results = []
        total_duration = 0
        
        for script in legacy_scripts:
            script_path = self.project_root / script
            if script_path.exists():
                print(f"Running {script}...")
                start_time = time.time()
                result = subprocess.run(['python', str(script_path)], 
                                      capture_output=True, text=True)
                duration = time.time() - start_time
                total_duration += duration
                
                results.append({
                    'script': script,
                    'success': result.returncode == 0,
                    'duration': duration,
                    'stdout': result.stdout[:500],  # Truncate output
                    'stderr': result.stderr[:500]
                })
        
        overall_success = all(r['success'] for r in results)
        
        return {
            'category': 'legacy',
            'success': overall_success,
            'duration': total_duration,
            'results': results,
            'stdout': f"Ran {len(results)} legacy scripts",
            'stderr': "",
            'returncode': 0 if overall_success else 1
        }
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n📊 Test Summary")
        print("=" * 60)
        
        total_duration = sum(r.get('duration', 0) for r in self.results.values())
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r.get('success', False))
        failed_tests = total_tests - passed_tests
        
        print(f"Total Test Suites: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⏱️  Total Duration: {total_duration:.2f}s")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Detailed results
        print("\n📋 Detailed Results:")
        for category, result in self.results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            duration = result.get('duration', 0)
            print(f"  {category:15} {status:8} ({duration:.2f}s)")
        
        # Failed tests details
        failed_categories = [cat for cat, res in self.results.items() if not res['success']]
        if failed_categories:
            print(f"\n❌ Failed Test Categories:")
            for category in failed_categories:
                result = self.results[category]
                print(f"  - {category}: {result.get('stderr', 'No error details')[:200]}")
        
        # Save detailed report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_suites': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'success_rate': (passed_tests/total_tests)*100,
                'total_duration': total_duration
            },
            'results': self.results
        }
        
        with open('test-report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: test-report.json")
        
        return passed_tests == total_tests
    
    def run_all_tests(self, **kwargs):
        """Run all test suites"""
        self.start_time = time.time()
        
        print("🚀 EVE-NG MCP Server - Comprehensive Test Suite")
        print("=" * 60)
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # Setup environment
        self.setup_environment()
        
        # Run test suites
        if kwargs.get('unit', True):
            self.results['unit'] = self.run_unit_tests(
                coverage=kwargs.get('coverage', False),
                verbose=kwargs.get('verbose', False)
            )
        
        if kwargs.get('integration', True):
            self.results['integration'] = self.run_integration_tests(
                eveng_host=kwargs.get('eveng_host'),
                eveng_user=kwargs.get('eveng_user'),
                eveng_pass=kwargs.get('eveng_pass'),
                verbose=kwargs.get('verbose', False)
            )
        
        if kwargs.get('e2e', True):
            self.results['e2e'] = self.run_e2e_tests(
                eveng_host=kwargs.get('eveng_host'),
                eveng_user=kwargs.get('eveng_user'),
                eveng_pass=kwargs.get('eveng_pass'),
                verbose=kwargs.get('verbose', False)
            )
        
        if kwargs.get('performance', False):
            self.results['performance'] = self.run_performance_tests(
                verbose=kwargs.get('verbose', False)
            )
        
        if kwargs.get('mcp_inspector', True):
            self.results['mcp_inspector'] = self.run_mcp_inspector_tests()
        
        if kwargs.get('legacy', False):
            self.results['legacy'] = self.run_legacy_tests()
        
        self.end_time = time.time()
        
        # Generate report
        success = self.generate_report()
        
        return success


def main():
    parser = argparse.ArgumentParser(description='EVE-NG MCP Server Test Runner')
    
    # Test categories
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--e2e', action='store_true', help='Run end-to-end tests only')
    parser.add_argument('--performance', action='store_true', help='Run performance tests')
    parser.add_argument('--mcp-inspector', action='store_true', help='Run MCP Inspector tests')
    parser.add_argument('--legacy', action='store_true', help='Run legacy test scripts')
    parser.add_argument('--all', action='store_true', help='Run all test suites')
    
    # Test options
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # EVE-NG connection
    parser.add_argument('--eveng-host', help='EVE-NG server host')
    parser.add_argument('--eveng-user', help='EVE-NG username')
    parser.add_argument('--eveng-pass', help='EVE-NG password')
    
    args = parser.parse_args()
    
    # If no specific test category is selected, run all except performance and legacy
    if not any([args.unit, args.integration, args.e2e, args.performance, 
                args.mcp_inspector, args.legacy, args.all]):
        args.unit = True
        args.integration = True
        args.e2e = True
        args.mcp_inspector = True
    
    if args.all:
        args.unit = True
        args.integration = True
        args.e2e = True
        args.performance = True
        args.mcp_inspector = True
        args.legacy = True
    
    # Create test runner
    runner = TestRunner()
    
    # Run tests
    success = runner.run_all_tests(
        unit=args.unit,
        integration=args.integration,
        e2e=args.e2e,
        performance=args.performance,
        mcp_inspector=args.mcp_inspector,
        legacy=args.legacy,
        coverage=args.coverage,
        verbose=args.verbose,
        eveng_host=args.eveng_host,
        eveng_user=args.eveng_user,
        eveng_pass=args.eveng_pass
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
