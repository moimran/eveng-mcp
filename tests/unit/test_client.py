"""
Unit tests for EVE-NG client functionality
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import httpx
from eveng_mcp_server.client import EVENGClient
from eveng_mcp_server.exceptions import EVENGConnectionError, EVENGAuthenticationError


class TestEVENGClient:
    """Test EVE-NG client functionality"""
    
    @pytest.fixture
    def client(self):
        """Create EVE-NG client instance"""
        return EVENGClient()
    
    @pytest.fixture
    def mock_success_response(self):
        """Mock successful HTTP response"""
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {
            "status": "success",
            "data": {"message": "Operation successful"}
        }
        return mock
    
    @pytest.fixture
    def mock_auth_response(self):
        """Mock authentication response"""
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {
            "status": "success",
            "data": {"message": "User logged in"}
        }
        mock.cookies = {"session": "test_session_id"}
        return mock
    
    @pytest.fixture
    def mock_error_response(self):
        """Mock error HTTP response"""
        mock = Mock()
        mock.status_code = 401
        mock.json.return_value = {
            "status": "error",
            "message": "Authentication failed"
        }
        return mock
    
    def test_client_initialization(self, client):
        """Test client initialization"""
        assert client.base_url is None
        assert client.session is None
        assert client.cookies is None
        assert client.timeout == 30
        assert client.max_retries == 3
    
    @pytest.mark.asyncio
    async def test_connect_success(self, client, mock_auth_response):
        """Test successful connection to EVE-NG"""
        with patch('httpx.AsyncClient.post', return_value=mock_auth_response):
            result = await client.connect("eve.local", "admin", "eve")
            
            assert result is True
            assert client.base_url == "http://eve.local:80"
            assert client.cookies is not None
    
    @pytest.mark.asyncio
    async def test_connect_with_custom_port(self, client, mock_auth_response):
        """Test connection with custom port"""
        with patch('httpx.AsyncClient.post', return_value=mock_auth_response):
            result = await client.connect("eve.local", "admin", "eve", port=8080)
            
            assert result is True
            assert client.base_url == "http://eve.local:8080"
    
    @pytest.mark.asyncio
    async def test_connect_with_https(self, client, mock_auth_response):
        """Test connection with HTTPS"""
        with patch('httpx.AsyncClient.post', return_value=mock_auth_response):
            result = await client.connect("eve.local", "admin", "eve", protocol="https")
            
            assert result is True
            assert client.base_url == "https://eve.local:80"
    
    @pytest.mark.asyncio
    async def test_connect_authentication_failure(self, client, mock_error_response):
        """Test connection with authentication failure"""
        with patch('httpx.AsyncClient.post', return_value=mock_error_response):
            with pytest.raises(EVENGAuthenticationError):
                await client.connect("eve.local", "admin", "wrong_password")
    
    @pytest.mark.asyncio
    async def test_connect_network_error(self, client):
        """Test connection with network error"""
        with patch('httpx.AsyncClient.post', side_effect=httpx.ConnectError("Connection failed")):
            with pytest.raises(EVENGConnectionError):
                await client.connect("invalid.host", "admin", "eve")
    
    @pytest.mark.asyncio
    async def test_disconnect_success(self, client, mock_success_response):
        """Test successful disconnection"""
        # Setup connected state
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        with patch('httpx.AsyncClient.delete', return_value=mock_success_response):
            result = await client.disconnect()
            
            assert result is True
            assert client.cookies is None
    
    @pytest.mark.asyncio
    async def test_disconnect_not_connected(self, client):
        """Test disconnection when not connected"""
        result = await client.disconnect()
        assert result is True  # Should succeed even if not connected
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, client, mock_success_response):
        """Test connection test when connected"""
        # Setup connected state
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        with patch('httpx.AsyncClient.get', return_value=mock_success_response):
            result = await client.test_connection()
            assert result is True
    
    @pytest.mark.asyncio
    async def test_test_connection_not_connected(self, client):
        """Test connection test when not connected"""
        with pytest.raises(EVENGConnectionError):
            await client.test_connection()
    
    @pytest.mark.asyncio
    async def test_get_server_info_success(self, client):
        """Test getting server information"""
        # Setup connected state
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": {
                "version": "6.2.0-4",
                "qemu_version": "2.4.0",
                "ksm": "enabled"
            }
        }
        
        with patch('httpx.AsyncClient.get', return_value=mock_response):
            result = await client.get_server_info()
            
            assert result["version"] == "6.2.0-4"
            assert result["qemu_version"] == "2.4.0"
            assert result["ksm"] == "enabled"
    
    @pytest.mark.asyncio
    async def test_list_labs_success(self, client):
        """Test listing labs"""
        # Setup connected state
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": {
                "lab1.unl": {"name": "Lab 1"},
                "lab2.unl": {"name": "Lab 2"}
            }
        }
        
        with patch('httpx.AsyncClient.get', return_value=mock_response):
            result = await client.list_labs()
            
            assert len(result) == 2
            assert "lab1.unl" in result
            assert "lab2.unl" in result
    
    @pytest.mark.asyncio
    async def test_create_lab_success(self, client, sample_lab_config):
        """Test creating a lab"""
        # Setup connected state
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "status": "success",
            "data": {"message": "Lab created successfully"}
        }
        
        with patch('httpx.AsyncClient.post', return_value=mock_response):
            result = await client.create_lab(**sample_lab_config)
            
            assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_delete_lab_success(self, client):
        """Test deleting a lab"""
        # Setup connected state
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": {"message": "Lab deleted successfully"}
        }
        
        with patch('httpx.AsyncClient.delete', return_value=mock_response):
            result = await client.delete_lab("/test_lab.unl")
            
            assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_request_retry_on_failure(self, client):
        """Test request retry mechanism"""
        # Setup connected state
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        client.max_retries = 2
        
        # Mock first call to fail, second to succeed
        mock_responses = [
            httpx.RequestError("Network error"),
            Mock(status_code=200, json=lambda: {"status": "success", "data": {}})
        ]
        
        with patch('httpx.AsyncClient.get', side_effect=mock_responses):
            result = await client.get_server_info()
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_request_timeout(self, client):
        """Test request timeout handling"""
        # Setup connected state
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        client.timeout = 1  # Very short timeout
        
        with patch('httpx.AsyncClient.get', side_effect=httpx.TimeoutException("Request timed out")):
            with pytest.raises(EVENGConnectionError):
                await client.get_server_info()
    
    def test_build_url(self, client):
        """Test URL building"""
        client.base_url = "http://eve.local:80"
        
        url = client._build_url("/api/labs")
        assert url == "http://eve.local:80/api/labs"
        
        url = client._build_url("api/labs")  # Without leading slash
        assert url == "http://eve.local:80/api/labs"
    
    def test_build_url_not_connected(self, client):
        """Test URL building when not connected"""
        with pytest.raises(EVENGConnectionError):
            client._build_url("/api/labs")
    
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_auth_response, mock_success_response):
        """Test client as context manager"""
        with patch('httpx.AsyncClient.post', return_value=mock_auth_response), \
             patch('httpx.AsyncClient.delete', return_value=mock_success_response):
            
            async with EVENGClient() as client:
                await client.connect("eve.local", "admin", "eve")
                assert client.cookies is not None
            
            # Should be disconnected after context exit
            assert client.cookies is None
    
    @pytest.mark.asyncio
    async def test_session_management(self, client, mock_auth_response):
        """Test session management"""
        with patch('httpx.AsyncClient.post', return_value=mock_auth_response):
            await client.connect("eve.local", "admin", "eve")
            
            # Session should be established
            assert client.session is not None
            assert client.cookies is not None
            
            await client.disconnect()
            
            # Session should be cleared
            assert client.cookies is None


class TestEVENGClientEdgeCases:
    """Test edge cases and error conditions"""
    
    @pytest.fixture
    def client(self):
        return EVENGClient()
    
    @pytest.mark.asyncio
    async def test_malformed_response(self, client):
        """Test handling of malformed JSON response"""
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Invalid response"
        
        with patch('httpx.AsyncClient.get', return_value=mock_response):
            with pytest.raises(EVENGConnectionError):
                await client.get_server_info()
    
    @pytest.mark.asyncio
    async def test_empty_response(self, client):
        """Test handling of empty response"""
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        with patch('httpx.AsyncClient.get', return_value=mock_response):
            result = await client.get_server_info()
            assert result == {}
    
    @pytest.mark.asyncio
    async def test_server_error_response(self, client):
        """Test handling of server error response"""
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "status": "error",
            "message": "Internal server error"
        }
        
        with patch('httpx.AsyncClient.get', return_value=mock_response):
            with pytest.raises(EVENGConnectionError):
                await client.get_server_info()
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client):
        """Test concurrent request handling"""
        client.base_url = "http://eve.local:80"
        client.cookies = {"session": "test_session"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": {}}
        
        with patch('httpx.AsyncClient.get', return_value=mock_response):
            # Make multiple concurrent requests
            tasks = [client.get_server_info() for _ in range(5)]
            results = await asyncio.gather(*tasks)
            
            assert len(results) == 5
            assert all(result is not None for result in results)
