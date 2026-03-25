from flask import Flask, jsonify, request

app = Flask(__name__)

# Static sample response for the IFSC lookup endpoint.
SAMPLE_BANK_DETAILS = {
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


@app.get("/health")
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@app.get("/api/v1/ifsc/<ifsc_code>")
def search_ifsc(ifsc_code: str) -> tuple:
    """
    Returns the same sample bank details for any requested IFSC code.
    The requested IFSC is echoed back so clients can correlate requests.
    """
    response = SAMPLE_BANK_DETAILS.copy()
    response["requested_ifsc"] = ifsc_code.upper()
    return jsonify(response), 200


@app.post("/api/v1/fx-quote")
def sample_fx_quote() -> tuple:
    """
    Sample endpoint that returns a deterministic FX quote shape.
    Useful for OpenAI tool/API integration testing.
    """
    payload = request.get_json(silent=True) or {}

    base_currency = str(payload.get("base_currency", "USD")).upper()
    quote_currency = str(payload.get("quote_currency", "INR")).upper()
    amount = float(payload.get("amount", 100))

    rate = 83.25
    converted_amount = round(amount * rate, 2)

    return (
        jsonify(
            {
                "base_currency": base_currency,
                "quote_currency": quote_currency,
                "amount": amount,
                "rate": rate,
                "converted_amount": converted_amount,
                "quote_id": "FX-SAMPLE-0001",
                "disclaimer": "Sample quote for integration testing only.",
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
