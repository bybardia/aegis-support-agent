from mcp.server.fastmcp import FastMCP

from src.tools import policy_lookup as _policy_lookup

mcp = FastMCP("aegis-policy-server")


@mcp.tool()
def policy_lookup(category: str) -> str:
    """Return the relevant support policy text for a given ticket category.

    Valid categories: billing, security, privacy, account_access,
    technical_bug, feature_request, general.
    """
    return _policy_lookup(category)


if __name__ == "__main__":
    # Runs over stdio by default (no ports) -> reproducible and easy to embed.
    mcp.run()