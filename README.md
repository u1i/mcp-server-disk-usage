# Disk Usage MCP Server (Demo)

## What is MCP?

Model Context Protocol (MCP) is a protocol that enables AI models like Claude to interact with external tools and services. It allows Claude to access real-time system information and perform actions on your behalf. 

Learn more about MCP:

- [MCP Documentation](https://modelcontextprotocol.io/docs/)
- [MCP Python SDK](https://modelcontextprotocol.io/docs/sdks/python)

## What You Get

When integrated with Claude Desktop, this demo MCP server enables Claude to check your disk usage (on the Mac) in real-time. Here's an example interaction:

User: "What is my current disk usage?"

Claude: "Let me check your current disk usage for you."

[approval to use disk-usage tool, user gives consent]

<details>
<summary>View result from ```get_disk_usage``` from ```disk-usage``` (local)</summary>

```json
{
    "device": "/dev/disk3s5",
    "total_gb": "228.0GB",
    "used_gb": "177.0GB",
    "available_gb": "27.0GB",
    "reserved_gb": "24.0GB",
    "percent_used": "87%",
    "mount": "/System/Volumes/Data",
    "summary": "Total: 228.0GB | Used: 177.0GB | Available: 27.0GB | Reserved: 24.0GB | Usage: 87%"
}
```
</details>

Claude: "Here's your current disk usage information:

Total Disk Space: 228.0GB   
Used Space: 177.0GB   
Available Space: 27.0GB   
Reserved Space: 24.0GB   
Usage Percentage: 87%   
Mount Point: /System/Volumes/Data   
Device: /dev/disk3s5

Your disk is currently at 87% capacity, with 27.0GB of space still available. If you're concerned about the high usage, you might want to consider cleaning up some files to free up more space."

## How It Works

### Server Capabilities

When the server starts, it advertises its capabilities to Claude through the MCP protocol. Here's what Claude sees:

```python
@mcp.tool()
def get_disk_usage() -> Dict[str, str]:
    """Get current disk usage information for the system disk
    
    Returns:
        A dictionary containing disk usage information with fields:
        - device: Device name
        - total_gb: Total size in GB
        - used_gb: Used space in GB
        - available_gb: Available space in GB
        - reserved_gb: Space reserved by system in GB
        - percent_used: Usage percentage
        - mount: Mount point
        - summary: Human-readable summary of disk usage
    """
```

This tells Claude that:

1. The server provides a tool called `get_disk_usage`
2. The tool returns a dictionary with detailed disk information
3. The docstring explains what each field means

### Communication Protocol

Unlike traditional REST APIs, MCP uses a bidirectional JSON-RPC protocol over WebSocket. Here's how it works:

1. **Initialization**:
   ```json
   // Claude -> Server
   {
     "jsonrpc": "2.0",
     "method": "initialize",
     "params": {
       "protocolVersion": "2024-11-05",
       "capabilities": {},
       "clientInfo": {
         "name": "claude-ai",
         "version": "0.1.0"
       }
     },
     "id": 0
   }
   ```

2. **Tool Advertisement**:
   The server responds with its capabilities, including the `get_disk_usage` tool and its schema.

3. **Tool Invocation**:
   ```json
   // Claude -> Server
   {
     "jsonrpc": "2.0",
     "method": "invoke",
     "params": {
       "tool": "get_disk_usage",
       "args": {}
     },
     "id": 1
   }
   ```

4. **Server Response**:
   ```json
   // Server -> Claude
   {
     "jsonrpc": "2.0",
     "result": {
       "device": "/dev/disk3s5",
       "total_gb": "228.0GB",
       "used_gb": "177.0GB",
       ...
     },
     "id": 1
   }
   ```

This WebSocket-based protocol allows for:
- Persistent connections
- Bidirectional communication
- Structured type information
- Tool discovery and documentation

### Implementation

1. The MCP server (`disk_usage_server.py`) uses Python's `subprocess` module to run the `df` command
2. It specifically looks at the `/System/Volumes/Data` partition (disk3s5 on macOS)
3. The server parses the output and returns structured data including:
   - Total disk space
   - Used space
   - Available space
   - Reserved space (space reserved by the system)
   - Usage percentage
   - Mount point and device information

## Requirements

- macOS (this tool is specifically designed for Mac's disk structure)
- Python 3.11+
- pip (Python package manager)

## Running the Server

1. Clone this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python disk_usage_server.py
```

**Note**: This server specifically looks for the `/System/Volumes/Data` partition (disk3s5) on macOS. It will not work on other operating systems.

## Claude Desktop Integration

1. Create a `claude-config.txt` file in your Claude Desktop configuration directory (usually `~/.config/claude-desktop/` on macOS) with:
```json
{
  "mcpServers": {
    "disk-usage": {
      "command": "python3",
      "args": [
        "<path-to-your-directory>/disk_usage_server.py"
      ]
    }
  }
}
```

2. Replace `<path-to-your-directory>` with the actual path to where you saved the server files

3. Restart Claude Desktop

## Learning Outcomes

This project demonstrates:
1. How to create a simple MCP server using Python
2. How to integrate system commands into an MCP tool
3. How to structure data for AI consumption
4. How to handle system-specific details (like disk partitions)
5. How to provide clear, human-readable summaries of technical data

## Files
- `disk_usage_server.py`: The main MCP server implementation
- `requirements.txt`: Python dependencies
- `claude-config.txt`: Example Claude Desktop configuration
