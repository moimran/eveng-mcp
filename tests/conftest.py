"""
Pytest configuration and fixtures for EVE-NG MCP Server tests
"""

import asyncio
import json
import os
import pytest
from pathlib import Path
from typing import Dict, Any, Optional
from unittest.mock import Mock, AsyncMock

# Add project root to Python path
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from eveng_mcp_server.client import EVENGClient
from eveng_mcp_server.config.settings import Settings


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--eveng-host",
        action="store",
        default="eve.local",
        help="EVE-NG server host"
    )
    parser.addoption(
        "--eveng-user",
        action="store",
        default="admin",
        help="EVE-NG username"
    )
    parser.addoption(
        "--eveng-pass",
        action="store",
        default="eve",
        help="EVE-NG password"
    )
    parser.addoption(
        "--eveng-port",
        action="store",
        default=80,
        type=int,
        help="EVE-NG port"
    )
    parser.addoption(
        "--eveng-protocol",
        action="store",
        default="http",
        help="EVE-NG protocol"
    )


def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_config(pytestconfig):
    """Test configuration from command line options"""
    return {
        "eveng": {
            "host": pytestconfig.getoption("--eveng-host"),
            "username": pytestconfig.getoption("--eveng-user"),
            "password": pytestconfig.getoption("--eveng-pass"),
            "port": pytestconfig.getoption("--eveng-port"),
            "protocol": pytestconfig.getoption("--eveng-protocol"),
            "timeout": 30,
            "max_retries": 3
        },
        "test": {
            "cleanup": True,
            "timeout": 60,
            "lab_prefix": "test_",
            "node_prefix": "test_node_"
        }
    }


@pytest.fixture
def mock_eveng_client():
    """Mock EVE-NG client for unit tests"""
    client = Mock(spec=EVENGClient)
    client.connect = AsyncMock(return_value=True)
    client.disconnect = AsyncMock(return_value=True)
    client.test_connection = AsyncMock(return_value=True)
    client.get_server_info = AsyncMock(return_value={
        "version": "6.2.0-4",
        "qemu_version": "2.4.0",
        "ksm": "enabled"
    })
    client.list_labs = AsyncMock(return_value={})
    client.create_lab = AsyncMock(return_value={"success": True})
    client.get_lab_details = AsyncMock(return_value={
        "name": "test_lab",
        "description": "Test lab",
        "author": "Test",
        "version": "1.0"
    })
    client.delete_lab = AsyncMock(return_value={"success": True})
    return client


@pytest.fixture
def sample_lab_config():
    """Sample lab configuration for testing"""
    return {
        "name": "test_lab",
        "description": "Test lab for unit tests",
        "author": "Test Suite",
        "version": "1.0",
        "path": "/"
    }


@pytest.fixture
def sample_node_config():
    """Sample node configuration for testing"""
    return {
        "template": "vios",
        "name": "test_router",
        "left": 25,
        "top": 25,
        "ram": 512,
        "ethernet": 4,
        "delay": 0,
        "console": "telnet"
    }


@pytest.fixture
def sample_network_config():
    """Sample network configuration for testing"""
    return {
        "network_type": "bridge",
        "name": "test_network",
        "left": 50,
        "top": 75
    }


@pytest.fixture
def mock_eveng_responses():
    """Mock EVE-NG API responses"""
    return {
        "login": {
            "status": "success",
            "data": {
                "message": "User logged in"
            }
        },
        "status": {
            "status": "success",
            "data": {
                "version": "6.2.0-4",
                "qemu_version": "2.4.0",
                "ksm": "enabled",
                "cpu": "Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz",
                "memory": "32GB"
            }
        },
        "labs": {
            "status": "success",
            "data": {}
        },
        "templates": {
            "status": "success",
            "data": {
                "vios": {
                    "name": "Cisco vIOS",
                    "type": "qemu",
                    "ethernet": 16,
                    "ram": 512,
                    "cpu": 1
                },
                "linux": {
                    "name": "Linux",
                    "type": "qemu",
                    "ethernet": 4,
                    "ram": 256,
                    "cpu": 1
                }
            }
        },
        "create_lab": {
            "status": "success",
            "data": {
                "message": "Lab created successfully"
            }
        },
        "lab_details": {
            "status": "success",
            "data": {
                "name": "test_lab",
                "description": "Test lab",
                "author": "Test",
                "version": "1.0",
                "nodes": {},
                "networks": {}
            }
        }
    }


@pytest.fixture
async def eveng_client(test_config):
    """Real EVE-NG client for integration tests"""
    client = EVENGClient()
    
    # Only connect if we're running integration tests
    if os.environ.get('PYTEST_CURRENT_TEST', '').find('integration') != -1:
        try:
            await client.connect(
                host=test_config["eveng"]["host"],
                username=test_config["eveng"]["username"],
                password=test_config["eveng"]["password"],
                port=test_config["eveng"]["port"],
                protocol=test_config["eveng"]["protocol"]
            )
        except Exception:
            pytest.skip("EVE-NG server not available")
    
    yield client
    
    # Cleanup
    try:
        await client.disconnect()
    except Exception:
        pass


@pytest.fixture
def test_lab_name():
    """Generate unique test lab name"""
    import uuid
    return f"test_lab_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def test_node_name():
    """Generate unique test node name"""
    import uuid
    return f"test_node_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def test_network_name():
    """Generate unique test network name"""
    import uuid
    return f"test_net_{uuid.uuid4().hex[:8]}"


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables"""
    original_env = os.environ.copy()
    
    # Set test environment variables
    os.environ['TESTING'] = 'true'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    os.environ['EVENG_SSL_VERIFY'] = 'false'
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def temp_lab_cleanup(eveng_client, test_config):
    """Cleanup test labs after test completion"""
    created_labs = []
    
    def register_lab(lab_path: str):
        created_labs.append(lab_path)
    
    yield register_lab
    
    # Cleanup created labs
    if test_config["test"]["cleanup"]:
        for lab_path in created_labs:
            try:
                asyncio.run(eveng_client.delete_lab(lab_path))
            except Exception:
                pass  # Ignore cleanup errors


@pytest.fixture
def performance_timer():
    """Timer for performance tests"""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def duration(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return Timer()


@pytest.fixture
def test_data_dir():
    """Path to test data directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def load_test_data(test_data_dir):
    """Load test data from JSON files"""
    def _load(filename: str) -> Dict[str, Any]:
        file_path = test_data_dir / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
    
    return _load


# Async fixtures for async tests
@pytest.fixture
async def async_mock_eveng_client():
    """Async mock EVE-NG client"""
    client = AsyncMock(spec=EVENGClient)
    client.connect.return_value = True
    client.disconnect.return_value = True
    client.test_connection.return_value = True
    return client
