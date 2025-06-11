# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the EVE-NG MCP Server.

## 🔍 Quick Diagnostics

### Health Check Commands

```bash
# Check server status
uv run eveng-mcp-server version

# Test EVE-NG connection
uv run eveng-mcp-server test-connection --host eve.local --username admin --password eve

# View configuration
uv run eveng-mcp-server config-info

# Check logs
tail -f logs/eveng-mcp-server.log
```

### System Requirements Check

```bash
# Check Python version (requires 3.10+)
python --version

# Check UV installation
uv --version

# Check network connectivity to EVE-NG
ping eve.local
curl -I http://eve.local:80

# Check port availability
netstat -tuln | grep 8000
```

## 🚨 Common Issues

### Connection Issues

#### Issue: "Connection refused" to EVE-NG server

**Symptoms:**
- `EVENGConnectionError: Failed to connect to EVE-NG server`
- Connection timeouts
- Network unreachable errors

**Solutions:**

1. **Check EVE-NG server status:**
   ```bash
   # Test basic connectivity
   ping eve.local
   
   # Test HTTP service
   curl -I http://eve.local:80
   
   # Check if EVE-NG web interface is accessible
   curl http://eve.local:80/api/status
   ```

2. **Verify network configuration:**
   ```bash
   # Check DNS resolution
   nslookup eve.local
   
   # Check routing
   traceroute eve.local
   
   # Test different ports
   telnet eve.local 80
   ```

3. **Check firewall settings:**
   ```bash
   # On EVE-NG server
   sudo ufw status
   sudo iptables -L
   
   # On client machine
   sudo ufw allow out 80
   sudo ufw allow out 443
   ```

#### Issue: "Authentication failed"

**Symptoms:**
- `EVENGAuthenticationError: Invalid credentials`
- 401 Unauthorized responses
- Login failures

**Solutions:**

1. **Verify credentials:**
   ```bash
   # Test credentials manually
   curl -X POST http://eve.local:80/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"eve"}'
   ```

2. **Check user account:**
   - Verify username and password in EVE-NG web interface
   - Ensure account is not locked or expired
   - Check user permissions

3. **Reset EVE-NG password:**
   ```bash
   # On EVE-NG server
   sudo /opt/unetlab/wrappers/unl_wrapper -a fixpermissions
   ```

### MCP Server Issues

#### Issue: "Port already in use"

**Symptoms:**
- `OSError: [Errno 98] Address already in use`
- Server fails to start
- Port binding errors

**Solutions:**

1. **Find process using the port:**
   ```bash
   # Check what's using port 8000
   sudo lsof -i :8000
   sudo netstat -tulpn | grep 8000
   ```

2. **Kill existing process:**
   ```bash
   # Kill process by PID
   sudo kill -9 <PID>
   
   # Or kill by name
   sudo pkill -f eveng-mcp-server
   ```

3. **Use different port:**
   ```bash
   # Start on different port
   uv run eveng-mcp-server run --port 8001
   ```

#### Issue: "Module not found" errors

**Symptoms:**
- `ModuleNotFoundError: No module named 'eveng_mcp_server'`
- Import errors
- Package not found

**Solutions:**

1. **Reinstall dependencies:**
   ```bash
   # Clean install
   rm -rf .venv
   uv sync
   
   # Or with pip
   pip install -e .
   ```

2. **Check Python path:**
   ```bash
   # Verify installation
   python -c "import eveng_mcp_server; print(eveng_mcp_server.__file__)"
   
   # Check sys.path
   python -c "import sys; print('\n'.join(sys.path))"
   ```

3. **Virtual environment issues:**
   ```bash
   # Activate virtual environment
   source .venv/bin/activate
   
   # Or use UV directly
   uv run python -m eveng_mcp_server.cli version
   ```

### Performance Issues

#### Issue: Slow response times

**Symptoms:**
- High latency in API calls
- Timeouts
- Poor performance

**Solutions:**

1. **Check system resources:**
   ```bash
   # CPU and memory usage
   top
   htop
   
   # Disk I/O
   iotop
   
   # Network usage
   iftop
   ```

2. **Optimize configuration:**
   ```json
   {
     "eveng": {
       "timeout": 60,
       "max_retries": 5,
       "connection_pool_size": 20
     },
     "performance": {
       "connection_pool": {
         "max_size": 20,
         "min_size": 5
       },
       "caching": {
         "enabled": true,
         "ttl": 300
       }
     }
   }
   ```

3. **Monitor performance:**
   ```bash
   # Enable performance logging
   export LOG_LEVEL=DEBUG
   
   # Use performance profiler
   python -m cProfile -o profile.stats -m eveng_mcp_server.cli run
   ```

### MCP Inspector Issues

#### Issue: Cannot connect to MCP Inspector

**Symptoms:**
- Inspector web interface not loading
- Connection refused to inspector
- Blank or error pages

**Solutions:**

1. **Check inspector status:**
   ```bash
   # Verify inspector is running
   curl http://127.0.0.1:6274
   
   # Check process
   ps aux | grep inspector
   ```

2. **Restart inspector:**
   ```bash
   # Kill existing inspector
   pkill -f inspector
   
   # Start new instance
   npx @modelcontextprotocol/inspector
   ```

3. **Check browser console:**
   - Open browser developer tools
   - Look for JavaScript errors
   - Check network tab for failed requests

#### Issue: MCP server not responding to inspector

**Symptoms:**
- Inspector shows "Connection failed"
- Tools/resources not loading
- Timeout errors

**Solutions:**

1. **Verify MCP server is running:**
   ```bash
   # Check SSE server
   curl http://localhost:8000/health
   
   # Check stdio mode
   echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | \
     uv run eveng-mcp-server run --transport stdio
   ```

2. **Test different transport modes:**
   ```bash
   # Try SSE mode
   uv run eveng-mcp-server run --transport sse --host 0.0.0.0 --port 8000
   
   # Try stdio mode
   npx @modelcontextprotocol/inspector --cli "uv run eveng-mcp-server run --transport stdio"
   ```

## 🔧 Advanced Debugging

### Enable Debug Logging

```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or in configuration
{
  "logging": {
    "level": "DEBUG",
    "format": "json"
  }
}
```

### Network Debugging

```bash
# Capture network traffic
sudo tcpdump -i any -w eveng-mcp.pcap host eve.local

# Monitor HTTP requests
mitmproxy --mode transparent --showhost

# Test with curl
curl -v -X POST http://eve.local:80/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"eve"}'
```

### Memory and Performance Profiling

```bash
# Memory profiling
python -m memory_profiler eveng_mcp_server/cli.py

# CPU profiling
python -m cProfile -o profile.stats eveng_mcp_server/cli.py

# Analyze profile
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

### Log Analysis

```bash
# Real-time log monitoring
tail -f logs/eveng-mcp-server.log | jq '.'

# Filter error logs
grep "ERROR" logs/eveng-mcp-server.log | jq '.'

# Count error types
grep "ERROR" logs/eveng-mcp-server.log | jq -r '.message' | sort | uniq -c
```

## 📊 Monitoring and Alerting

### Health Checks

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed status
curl http://localhost:8000/status

# Metrics endpoint
curl http://localhost:8000/metrics
```

### Log Monitoring

```bash
# Set up log rotation
sudo logrotate -f /etc/logrotate.d/eveng-mcp-server

# Monitor log size
du -h logs/eveng-mcp-server.log

# Archive old logs
find logs/ -name "*.log" -mtime +7 -exec gzip {} \;
```

## 🆘 Getting Help

### Collect Diagnostic Information

```bash
# System information
uname -a
python --version
uv --version

# Service status
systemctl status eveng-mcp-server

# Recent logs
journalctl -u eveng-mcp-server --since "1 hour ago"

# Configuration
uv run eveng-mcp-server config-info

# Network connectivity
ping eve.local
curl -I http://eve.local:80
```

### Create Support Bundle

```bash
#!/bin/bash
# Create support bundle
mkdir -p support-bundle
cp logs/eveng-mcp-server.log support-bundle/
cp config/*.json support-bundle/
systemctl status eveng-mcp-server > support-bundle/service-status.txt
uv run eveng-mcp-server config-info > support-bundle/config-info.txt
tar -czf support-bundle-$(date +%Y%m%d-%H%M%S).tar.gz support-bundle/
```

### Contact Support

- **GitHub Issues**: [Report a bug](https://github.com/your-org/eveng-mcp-server/issues)
- **Discussions**: [Ask questions](https://github.com/your-org/eveng-mcp-server/discussions)
- **Email**: support@your-org.com

### Useful Resources

- [EVE-NG Documentation](https://www.eve-ng.net/documentation/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Python Debugging Guide](https://docs.python.org/3/library/pdb.html)
- [Network Troubleshooting](https://www.cyberciti.biz/tips/linux-network-troubleshooting-and-debugging.html)
