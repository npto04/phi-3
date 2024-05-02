from typing import Optional, Type

import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

HOST = "api.frankfurter.app"


def convert_currency(amount: float, currency1: str, currency2: str) -> str:
    """Converts currency.
    amount (float): The amount of currency to convert. It must be always numeric.
    currency1 (str): The currency to convert from. It must be a valid currency code. Examples: USD, EUR, GBP.
    currency2 (str): The currency to convert to. It must be a valid currency code. Examples: USD, EUR, GBP.
    """
    try:
        url = f"https://{HOST}/latest?amount={amount}&from={currency1.upper()}&to={currency2.upper()}"
        resp = requests.get(url=url)

        return resp.text
    except Exception as e:
        return str(e)


class ConvertCurrencyInput(BaseModel):
    amount: float = Field(
        ...,
        title="Amount",
        description="The amount of currency to convert. It must be always numeric.",
    )
    currency1: str = Field(
        ...,
        title="Currency 1",
        description="The currency to convert from. It must be a valid currency code. Examples: USD, EUR, GBP.",
    )
    currency2: str = Field(
        ...,
        title="Currency 2",
        description="The currency to convert to. It must be a valid currency code. Examples: USD, EUR, GBP.",
    )


class ConvertCurrencyTool(BaseTool):
    name = "convert_currency"
    description = "Converts currency."
    args_schema: Type[BaseModel] = ConvertCurrencyInput
    return_direct = True

    def _run(
        self,
        amount: float,
        currency1: str,
        currency2: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Tool to convert currency."""
        return convert_currency(amount, currency1, currency2)

    async def _run_async(
        self,
        amount: float,
        currency1: str,
        currency2: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Tool to convert currency."""
        return convert_currency(amount, currency1, currency2)


tools = [ConvertCurrencyTool()]
