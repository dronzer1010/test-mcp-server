"""MCP-compliant sample server for IFSC lookup and FX quote tools.

Designed for container deployments (e.g., Azure Container Apps) using
Streamable HTTP transport at /mcp.
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "ifsc-fx-mcp-server",
    instructions=(
        "Sample MCP server exposing deterministic banking tools for testing: "
        "IFSC lookup and FX quote."
    ),
    stateless_http=True,
    json_response=True,
)

SAMPLE_BANK_DETAILS: dict[str, str] = {
    "ifsc": "SBIN0000123",
    "bank_name": "State Bank of India",
    "branch": "Connaught Place",
    "address": "Parliament Street, New Delhi, Delhi 110001",
    "city": "New Delhi",
    "district": "New Delhi",
    "state": "Delhi",
    "micr": "110002087",
    "swift": "SBININBB104",
}


@mcp.tool()
def search_ifsc(ifsc_code: str) -> dict[str, Any]:
    """Return deterministic sample bank details for any IFSC code."""
    return {
        **SAMPLE_BANK_DETAILS,
        "requested_ifsc": ifsc_code.upper(),
        "note": "Sample static response for integration testing.",
    }


@mcp.tool()
def sample_fx_quote(
    amount: float = 100,
    base_currency: str = "USD",
    quote_currency: str = "INR",
) -> dict[str, Any]:
    """Return a deterministic sample FX quote."""
    rate = 83.25
    return {
        "base_currency": base_currency.upper(),
        "quote_currency": quote_currency.upper(),
        "amount": amount,
        "rate": rate,
        "converted_amount": round(amount * rate, 2),
        "quote_id": "FX-SAMPLE-0001",
        "disclaimer": "Sample quote for integration testing only.",
    }


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    transport = os.getenv("MCP_TRANSPORT", "streamable-http")
    mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    main()
