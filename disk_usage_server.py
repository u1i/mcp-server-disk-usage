from mcp.server.fastmcp import FastMCP
import subprocess
from typing import Dict
import asyncio

# Create an MCP server
mcp = FastMCP("DiskUsage")

@mcp.tool()
def get_disk_usage() -> Dict[str, str]:
    """Get current disk usage information for the system disk (disk3s1s1)
    
    Returns:
        A dictionary containing disk usage information with fields:
        - device: Device name
        - size: Total size
        - used: Used space
        - available: Available space
        - capacity: Usage percentage
        - mount: Mount point
    """
    try:
        cmd = "df -h | grep disk3s5"
        result = subprocess.check_output(cmd, shell=True, text=True)
        parts = result.split()
        # Add some calculated fields for clarity
        total_gb = float(parts[1].replace('Gi',''))
        used_gb = float(parts[2].replace('Gi',''))
        avail_gb = float(parts[3].replace('Gi',''))
        percent = int(parts[4].replace('%',''))
        
        # Calculate reserved space (total - used - available)
        reserved_gb = total_gb - used_gb - avail_gb
        
        return {
            "device": parts[0],
            "total_gb": f"{total_gb:.1f}GB",
            "used_gb": f"{used_gb:.1f}GB",
            "available_gb": f"{avail_gb:.1f}GB",
            "reserved_gb": f"{reserved_gb:.1f}GB",
            "percent_used": f"{percent}%",
            "mount": parts[8] if len(parts) > 8 else parts[5],
            "summary": f"Total: {total_gb:.1f}GB | Used: {used_gb:.1f}GB | Available: {avail_gb:.1f}GB | Reserved: {reserved_gb:.1f}GB | Usage: {percent}%"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
