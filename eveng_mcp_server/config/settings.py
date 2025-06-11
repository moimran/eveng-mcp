"""Configuration management for EVE-NG MCP Server."""

import os
from typing import Optional, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class EVENGConfig(BaseSettings):
    """EVE-NG server configuration."""
    
    host: str = Field(default="eve.local", description="EVE-NG server hostname or IP")
    port: int = Field(default=80, description="EVE-NG server port")
    protocol: str = Field(default="http", description="Protocol (http/https)")
    username: str = Field(default="admin", description="EVE-NG username")
    password: str = Field(default="eve", description="EVE-NG password")
    ssl_verify: bool = Field(default=False, description="Verify SSL certificates")
    timeout: int = Field(default=30, description="Connection timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum connection retries")
    
    @field_validator('protocol')
    @classmethod
    def validate_protocol(cls, v):
        if v not in ['http', 'https']:
            raise ValueError('Protocol must be http or https')
        return v

    @field_validator('port')
    @classmethod
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
    
    @property
    def base_url(self) -> str:
        """Get the base URL for EVE-NG API."""
        return f"{self.protocol}://{self.host}:{self.port}"
    
    class Config:
        env_prefix = "EVENG_"
        case_sensitive = False


class MCPConfig(BaseSettings):
    """MCP server configuration."""
    
    name: str = Field(default="EVE-NG MCP Server", description="Server name")
    version: str = Field(default="1.0.0", description="Server version")
    description: str = Field(
        default="Comprehensive MCP server for EVE-NG network emulation platform",
        description="Server description"
    )
    
    # Transport configuration
    transport: str = Field(default="stdio", description="Transport type (stdio/sse)")
    host: str = Field(default="localhost", description="Host for SSE transport")
    port: int = Field(default=8000, description="Port for SSE transport")
    
    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json/console)")
    
    @field_validator('transport')
    @classmethod
    def validate_transport(cls, v):
        if v not in ['stdio', 'sse']:
            raise ValueError('Transport must be stdio or sse')
        return v

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of {valid_levels}')
        return v.upper()
    
    class Config:
        env_prefix = "MCP_"
        case_sensitive = False


class SecurityConfig(BaseSettings):
    """Security configuration."""
    
    disable_ssl_warnings: bool = Field(
        default=True, 
        description="Disable SSL warnings for self-signed certificates"
    )
    max_concurrent_connections: int = Field(
        default=10, 
        description="Maximum concurrent connections to EVE-NG"
    )
    session_timeout: int = Field(
        default=3600, 
        description="Session timeout in seconds"
    )
    
    class Config:
        env_prefix = "SECURITY_"
        case_sensitive = False


class AppConfig(BaseSettings):
    """Main application configuration."""
    
    eveng: EVENGConfig = Field(default_factory=EVENGConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    
    # Development settings
    debug: bool = Field(default=False, description="Enable debug mode")
    testing: bool = Field(default=False, description="Enable testing mode")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @classmethod
    def load_config(cls, config_file: Optional[str] = None) -> "AppConfig":
        """Load configuration from file and environment variables."""
        if config_file and os.path.exists(config_file):
            return cls(_env_file=config_file)
        return cls()


# Global configuration instance
config = AppConfig.load_config()


def get_config() -> AppConfig:
    """Get the global configuration instance."""
    return config


def reload_config(config_file: Optional[str] = None) -> AppConfig:
    """Reload configuration from file and environment variables."""
    global config
    config = AppConfig.load_config(config_file)
    return config
