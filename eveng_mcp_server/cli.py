"""Command-line interface for EVE-NG MCP Server."""

import asyncio
import sys
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table

from .config import get_config, reload_config, configure_logging
from .server import create_server
from .core import get_eveng_client


app = typer.Typer(
    name="eveng-mcp-server",
    help="EVE-NG MCP Server - Comprehensive MCP server for EVE-NG network emulation platform"
)
console = Console()


@app.command()
def run(
    transport: str = typer.Option(
        "stdio", 
        "--transport", 
        "-t",
        help="Transport type (stdio/sse)"
    ),
    host: str = typer.Option(
        "localhost",
        "--host",
        "-h", 
        help="Host for SSE transport"
    ),
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Port for SSE transport"
    ),
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Configuration file path"
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug mode"
    )
):
    """Run the EVE-NG MCP server."""
    
    # Load configuration
    if config_file:
        reload_config(config_file)
    
    config = get_config()
    
    # Override config with CLI arguments
    if debug:
        config.debug = True
        config.mcp.log_level = "DEBUG"
    
    config.mcp.transport = transport
    config.mcp.host = host
    config.mcp.port = port
    
    # Configure logging
    configure_logging()
    
    console.print(f"🚀 Starting EVE-NG MCP Server", style="bold green")
    console.print(f"Transport: {transport}")
    if transport == "sse":
        console.print(f"Server will be available at: http://{host}:{port}")
    
    # Create and run server
    async def run_server():
        server = create_server()
        
        if transport == "stdio":
            await server.run_stdio()
        else:
            await server.run_sse(host, port)
    
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        console.print("\n👋 Server stopped", style="yellow")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)


@app.command()
def test_connection(
    host: str = typer.Option(
        "eve.local",
        "--host",
        "-h",
        help="EVE-NG server hostname"
    ),
    username: str = typer.Option(
        "admin",
        "--username",
        "-u",
        help="Username"
    ),
    password: str = typer.Option(
        "eve",
        "--password",
        "-p",
        help="Password"
    ),
    port: int = typer.Option(
        80,
        "--port",
        help="Server port"
    ),
    protocol: str = typer.Option(
        "http",
        "--protocol",
        help="Protocol (http/https)"
    )
):
    """Test connection to EVE-NG server."""
    
    async def test():
        configure_logging()
        
        console.print("🔍 Testing EVE-NG connection...", style="blue")
        
        # Update configuration
        config = get_config()
        config.eveng.host = host
        config.eveng.username = username
        config.eveng.password = password
        config.eveng.port = port
        config.eveng.protocol = protocol
        
        client = get_eveng_client()
        
        try:
            # Test connection
            await client.connect()
            status = await client.get_server_status()
            
            console.print("✅ Connection successful!", style="bold green")
            
            # Display server info in a table
            table = Table(title="EVE-NG Server Information")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Server", f"{protocol}://{host}:{port}")
            table.add_row("Username", username)
            table.add_row("Version", status.get('version', 'Unknown'))
            table.add_row("Status", status.get('status', 'Unknown'))
            table.add_row("Uptime", status.get('uptime', 'Unknown'))
            
            console.print(table)
            
        except Exception as e:
            console.print(f"❌ Connection failed: {e}", style="bold red")
            sys.exit(1)
        
        finally:
            await client.disconnect()
    
    asyncio.run(test())


@app.command()
def config_info(
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Configuration file path"
    )
):
    """Display current configuration."""
    
    if config_file:
        reload_config(config_file)
    
    config = get_config()
    
    console.print("📋 Current Configuration", style="bold blue")
    
    # EVE-NG Configuration
    table = Table(title="EVE-NG Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Host", config.eveng.host)
    table.add_row("Port", str(config.eveng.port))
    table.add_row("Protocol", config.eveng.protocol)
    table.add_row("Username", config.eveng.username)
    table.add_row("Password", "***" if config.eveng.password else "Not set")
    table.add_row("SSL Verify", str(config.eveng.ssl_verify))
    table.add_row("Timeout", f"{config.eveng.timeout}s")
    
    console.print(table)
    
    # MCP Configuration
    table = Table(title="MCP Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Name", config.mcp.name)
    table.add_row("Version", config.mcp.version)
    table.add_row("Transport", config.mcp.transport)
    table.add_row("Host", config.mcp.host)
    table.add_row("Port", str(config.mcp.port))
    table.add_row("Log Level", config.mcp.log_level)
    table.add_row("Log Format", config.mcp.log_format)
    
    console.print(table)


@app.command()
def version():
    """Show version information."""
    config = get_config()
    
    console.print(f"EVE-NG MCP Server v{config.mcp.version}", style="bold green")
    console.print(f"Description: {config.mcp.description}")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
