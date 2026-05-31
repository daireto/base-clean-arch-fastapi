from fastmcp import FastMCP
from fastmcp.tools import tool

mcp = FastMCP('Demo 🚀')


@tool
def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a (int): The first number
        b (int): The second number

    """
    return a + b


mcp.add_tool(add)

# TODO: To be continued with more tools and LLM integration

if __name__ == '__main__':
    mcp.run()
