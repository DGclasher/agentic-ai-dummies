from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int, b:int) -> int:
    """
    It takes 2 integer input and returns the addition between them
    """
    return a + b

@mcp.tool()
def multiply(a:int, b:int) -> int:
    """
    It takes 2 integer input and returns the multiplication operation
    between them
    """
    return a*b

if __name__ == "__main__":
    mcp.run(transport="stdio")