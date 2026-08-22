from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(city:str):
    """
    This function takes city as input and gives the weather details as output in string
    """
    return "Its raining bitch"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")