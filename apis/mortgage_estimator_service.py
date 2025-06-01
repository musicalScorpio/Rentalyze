from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv('../env/relatize.env')

FRED_API_KEY = os.getenv("FRED_API_KEY")


def get_10_year_yield(api_key):
    """Fetch current 10-year Treasury yield from FRED."""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "DGS10",  # 10-Year Treasury Constant Maturity
        "api_key": api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "observations" in data and data["observations"]:
        return float(data["observations"][0]["value"])
    return None
# === Investor Mortgage ===
def investor_credit_spread_by_score(credit_score):
    if credit_score >= 760:
        return 2.0
    elif credit_score >= 700:
        return 2.25
    elif credit_score >= 680:
        return 2.5
    elif credit_score >= 660:
        return 2.75
    elif credit_score >= 620:
        return 3.25
    else:
        return 3.75

def estimate_investor_rate_from_yield(yield_10y, credit_score):
    spread = investor_credit_spread_by_score(credit_score)
    return yield_10y + spread

def get_investor_mortgage_pi(credit_score, loan_amount, years):
    yield_10y = get_10_year_yield(FRED_API_KEY)
    if yield_10y is None:
        return {"error": "Failed to retrieve 10-Year Treasury Yield"}
    rate = estimate_investor_rate_from_yield(yield_10y, credit_score)
    monthly_payment = calculate_monthly_payment(loan_amount, rate, years)
    return {"yield_10y": yield_10y, "rate": rate, "monthly_payment": monthly_payment}

def credit_spread_by_score(credit_score):
    """Map credit score to spread over 10Y yield."""
    if credit_score >= 760:
        return 1.5
    elif credit_score >= 700:
        return 1.75
    elif credit_score >= 680:
        return 2.0
    elif credit_score >= 660:
        return 2.25
    elif credit_score >= 620:
        return 2.5
    else:
        return 3.0

def estimate_rate_from_yield(yield_10y, credit_score):
    spread = credit_spread_by_score(credit_score)
    return yield_10y + spread

def calculate_monthly_payment(principal, annual_rate, years):
    """Calculate monthly mortgage payment (Principal + Interest)."""
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * r * (1 + r)**n / ((1 + r)**n - 1)

@app.route("/api/mortgage-estimate", methods=["GET"])
def pricipal_interest_estimate():
    try:
        principal = float(request.args.get("principal", 0))
        years = int(request.args.get("term_years", 30))
        credit_score =int(request.args.get("credit_score", 700))
        debt_service = get_mortgage_pi(credit_score,principal, years )
        yield_10y = debt_service['yield_10y']
        rate =debt_service['rate']
        monthly_payment=debt_service['monthly_payment']
        return jsonify({
            "principal": principal,
            "term_years": years,
            "credit_score": credit_score,
            "10_year_yield": round(yield_10y, 3),
            "estimated_rate": round(rate, 3),
            "monthly_principal_interest": round(monthly_payment, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/investor-mortgage-estimate", methods=["GET"])
def investor_principal_interest_estimate():
    try:
        principal = float(request.args.get("principal", 0))
        years = int(request.args.get("term_years", 30))
        credit_score = int(request.args.get("credit_score", 700))

        result = get_investor_mortgage_pi(credit_score, principal, years)
        if "error" in result:
            return jsonify(result), 503

        return jsonify({
            "principal": principal,
            "term_years": years,
            "credit_score": credit_score,
            "10_year_yield": round(result['yield_10y'], 3),
            "estimated_investor_rate": round(result['rate'], 3),
            "monthly_principal_interest": round(result['monthly_payment'], 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_mortgage_pi(credit_score, loan_amount, years):
    # Get real-time 10-year yield
    yield_10y = get_10_year_yield(FRED_API_KEY)
    if yield_10y is None:
        return jsonify({"error": "Failed to retrieve 10-Year Treasury Yield"}), 503
    # Estimate mortgage rate and calculate monthly PI
    rate = estimate_rate_from_yield(yield_10y, credit_score)
    monthly_payment = calculate_monthly_payment(loan_amount, rate, years)

    debt_service = {'yield_10y': yield_10y, 'rate': rate, 'monthly_payment': monthly_payment}

    return debt_service


if __name__ == "__main__":
    pricipal_interest_estimate()
    #app.run(debug=True, port=5000)