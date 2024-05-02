import requests
from langchain_core.tools import tool

# The host for the currency conversion API
HOST = "api.frankfurter.app"


@tool
def convert_currency(amount: float, currency1: str, currency2: str) -> dict:
    """
    Converts one currency to another using the Frankfurter API.

    Parameters:
    amount (float): The amount of money to convert.
    currency1 (str): The currency to convert from.
    currency2 (str): The currency to convert to.

    Returns:
    dict: A dictionary containing the conversion result.
    """
    try:
        url = f"https://{HOST}/latest?amount={amount}&from={currency1.upper()}&to={currency2.upper()}"
        resp = requests.get(url=url)

        return resp.json()
    except Exception as e:
        return {"error": str(e)}


# A list of all the tools available in this module
tools = [convert_currency]
