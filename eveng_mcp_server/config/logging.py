"""Logging configuration for EVE-NG MCP Server."""

import sys
import structlog
from typing import Any, Dict
from .settings import get_config


def configure_logging(transport: str = "sse") -> None:
    """Configure structured logging for the application."""
    config = get_config()
    
    # Configure structlog
    if config.mcp.log_format.lower() == "json":
        # JSON logging for production
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    else:
        # Console logging for development
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.dev.ConsoleRenderer(colors=True)
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    
    # Set log level - use stderr for stdio transport to avoid interfering with JSON-RPC
    import logging
    log_stream = sys.stderr if transport == "stdio" else sys.stdout
    logging.basicConfig(
        format="%(message)s",
        stream=log_stream,
        level=getattr(logging, config.mcp.log_level)
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a configured logger instance."""
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    @property
    def logger(self) -> structlog.BoundLogger:
        """Get a logger instance for this class."""
        return get_logger(self.__class__.__name__)


def log_function_call(func_name: str, **kwargs: Any) -> Dict[str, Any]:
    """Create a log context for function calls."""
    return {
        "function": func_name,
        "parameters": {k: v for k, v in kwargs.items() if not k.startswith('_')}
    }


def log_api_call(method: str, url: str, status_code: int = None, **kwargs: Any) -> Dict[str, Any]:
    """Create a log context for API calls."""
    context = {
        "api_call": True,
        "method": method,
        "url": url,
    }
    
    if status_code is not None:
        context["status_code"] = status_code
    
    context.update(kwargs)
    return context


def log_error(error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a log context for errors."""
    error_context = {
        "error": True,
        "error_type": error.__class__.__name__,
        "error_message": str(error),
    }
    
    if context:
        error_context.update(context)
    
    return error_context
