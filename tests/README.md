# Testing Guide

Comprehensive testing suite for the EVE-NG MCP Server, covering unit tests, integration tests, end-to-end tests, and performance testing.

## 🧪 Test Structure

```
tests/
├── unit/                   # Unit tests for individual components
│   ├── test_client.py     # EVE-NG client tests
│   ├── test_tools.py      # Tool implementation tests
│   ├── test_resources.py  # Resource handler tests
│   └── test_prompts.py    # Prompt handler tests
├── integration/           # Integration tests
│   ├── test_eveng_api.py  # EVE-NG API integration
│   ├── test_mcp_protocol.py # MCP protocol compliance
│   └── test_lab_workflow.py # Lab management workflow
├── e2e/                   # End-to-end tests
│   ├── test_complete_workflow.py # Full workflow tests
│   ├── test_mcp_inspector.py     # MCP Inspector integration
│   └── test_production_scenarios.py # Production scenarios
├── performance/           # Performance and load tests
│   ├── test_load.py      # Load testing
│   ├── test_stress.py    # Stress testing
│   └── test_benchmarks.py # Performance benchmarks
├── fixtures/              # Test data and fixtures
│   ├── lab_templates/    # Sample lab configurations
│   ├── mock_responses/   # Mock EVE-NG responses
│   └── test_configs/     # Test configurations
├── conftest.py           # Pytest configuration
├── requirements.txt      # Test dependencies
└── run_tests.py         # Main test runner
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Or with UV
uv sync --dev
```

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test categories
python tests/run_tests.py --unit
python tests/run_tests.py --integration
python tests/run_tests.py --e2e
python tests/run_tests.py --performance

# Run with coverage
python tests/run_tests.py --coverage

# Run specific test file
pytest tests/unit/test_client.py -v

# Run with live EVE-NG server
pytest tests/integration/ --eveng-host eve.local --eveng-user admin --eveng-pass eve
```

## 📋 Test Categories

### Unit Tests

Test individual components in isolation with mocked dependencies.

**Coverage:**
- EVE-NG client functionality
- Tool implementations
- Resource handlers
- Prompt generators
- Configuration management
- Error handling

**Example:**
```bash
# Run unit tests
pytest tests/unit/ -v --cov=eveng_mcp_server

# Run specific unit test
pytest tests/unit/test_client.py::TestEVENGClient::test_connect -v
```

### Integration Tests

Test component interactions and external API integration.

**Coverage:**
- EVE-NG API integration
- MCP protocol compliance
- Database operations
- Configuration loading
- Authentication flows

**Example:**
```bash
# Run integration tests (requires EVE-NG server)
pytest tests/integration/ --eveng-host eve.local

# Test specific integration
pytest tests/integration/test_eveng_api.py -v
```

### End-to-End Tests

Test complete workflows from start to finish.

**Coverage:**
- Complete lab creation workflows
- MCP Inspector integration
- Multi-tool operations
- Error recovery scenarios
- Production use cases

**Example:**
```bash
# Run E2E tests
pytest tests/e2e/ --eveng-host eve.local --slow

# Test specific workflow
pytest tests/e2e/test_complete_workflow.py::test_lab_lifecycle -v
```

### Performance Tests

Test system performance, load handling, and resource usage.

**Coverage:**
- Concurrent connection handling
- Memory usage patterns
- Response time benchmarks
- Stress testing
- Resource leak detection

**Example:**
```bash
# Run performance tests
pytest tests/performance/ --benchmark-only

# Load testing
python tests/performance/test_load.py --connections 50 --duration 300
```

## 🔧 Test Configuration

### Environment Variables

```bash
# Test configuration
export TEST_EVENG_HOST=eve.local
export TEST_EVENG_PORT=80
export TEST_EVENG_USERNAME=admin
export TEST_EVENG_PASSWORD=eve
export TEST_EVENG_PROTOCOL=http

# Test behavior
export TEST_TIMEOUT=30
export TEST_RETRIES=3
export TEST_PARALLEL=true
export TEST_CLEANUP=true
export TEST_VERBOSE=false
```

### Configuration File

Create `tests/config.json`:

```json
{
  "eveng": {
    "host": "eve.local",
    "port": 80,
    "protocol": "http",
    "username": "admin",
    "password": "eve",
    "timeout": 30
  },
  "test": {
    "cleanup": true,
    "parallel": true,
    "timeout": 60,
    "retries": 3,
    "lab_prefix": "test_",
    "node_prefix": "test_node_"
  },
  "performance": {
    "max_connections": 50,
    "test_duration": 300,
    "ramp_up_time": 30
  }
}
```

## 📊 Test Reports

### Coverage Reports

```bash
# Generate coverage report
pytest tests/ --cov=eveng_mcp_server --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Performance Reports

```bash
# Generate performance report
pytest tests/performance/ --benchmark-json=benchmark.json

# View benchmark results
python -m pytest_benchmark compare benchmark.json
```

### Test Results

```bash
# Generate JUnit XML report
pytest tests/ --junitxml=test-results.xml

# Generate detailed HTML report
pytest tests/ --html=test-report.html --self-contained-html
```

## 🎯 Test Scenarios

### Basic Functionality

1. **Connection Management**
   - Connect to EVE-NG server
   - Authentication validation
   - Connection error handling
   - Disconnect cleanup

2. **Lab Management**
   - Create lab
   - List labs
   - Get lab details
   - Delete lab

3. **Node Management**
   - Add nodes to lab
   - Start/stop nodes
   - Configure node properties
   - Delete nodes

4. **Network Management**
   - Create networks
   - Connect nodes to networks
   - Topology management
   - Network cleanup

### Advanced Scenarios

1. **Complex Topologies**
   - Multi-node networks
   - Hierarchical topologies
   - Mixed node types
   - Large-scale labs

2. **Error Handling**
   - Network failures
   - Authentication errors
   - Resource conflicts
   - Timeout scenarios

3. **Performance Testing**
   - Concurrent operations
   - Large lab handling
   - Memory usage
   - Response times

## 🔍 Debugging Tests

### Verbose Output

```bash
# Enable verbose logging
pytest tests/ -v -s --log-cli-level=DEBUG

# Show test output
pytest tests/ -s --capture=no
```

### Test Debugging

```bash
# Run single test with debugger
pytest tests/unit/test_client.py::test_connect --pdb

# Debug on failure
pytest tests/ --pdb-trace
```

### Log Analysis

```bash
# View test logs
tail -f tests/logs/test.log

# Filter specific test logs
grep "test_connect" tests/logs/test.log
```

## 🚨 Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install uv
        uv sync --dev
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ --cov=eveng_mcp_server
    
    - name: Run integration tests
      run: |
        pytest tests/integration/
      env:
        TEST_EVENG_HOST: ${{ secrets.TEST_EVENG_HOST }}
        TEST_EVENG_USERNAME: ${{ secrets.TEST_EVENG_USERNAME }}
        TEST_EVENG_PASSWORD: ${{ secrets.TEST_EVENG_PASSWORD }}
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: pytest tests/unit/
        language: system
        pass_filenames: false
        always_run: true
```

## 📝 Writing Tests

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from eveng_mcp_server.client import EVENGClient

class TestEVENGClient:
    @pytest.fixture
    def client(self):
        return EVENGClient()
    
    @pytest.fixture
    def mock_response(self):
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {"data": {"status": "success"}}
        return mock
    
    def test_connect_success(self, client, mock_response):
        with patch('httpx.post', return_value=mock_response):
            result = client.connect("eve.local", "admin", "eve")
            assert result is True
    
    def test_connect_failure(self, client):
        with patch('httpx.post', side_effect=Exception("Connection failed")):
            with pytest.raises(ConnectionError):
                client.connect("invalid.host", "admin", "eve")
```

### Test Fixtures

```python
# tests/conftest.py
import pytest
from eveng_mcp_server.client import EVENGClient

@pytest.fixture(scope="session")
def eveng_client():
    client = EVENGClient()
    yield client
    client.disconnect()

@pytest.fixture
def sample_lab():
    return {
        "name": "test_lab",
        "description": "Test lab for unit tests",
        "author": "Test Suite",
        "version": "1.0"
    }
```

## 🎯 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Mock External Dependencies**: Use mocks for EVE-NG API calls in unit tests
3. **Cleanup**: Always clean up test resources
4. **Descriptive Names**: Use clear, descriptive test names
5. **Test Data**: Use fixtures for consistent test data
6. **Error Testing**: Test both success and failure scenarios
7. **Performance**: Include performance assertions where relevant

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [MCP Testing Guidelines](https://modelcontextprotocol.io/testing)
- [EVE-NG API Documentation](https://www.eve-ng.net/documentation/api)
- [Performance Testing Best Practices](performance/README.md)
- [CI/CD Integration Guide](ci-cd/README.md)
