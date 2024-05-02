from pydantic import BaseModel


class QueryInput(BaseModel):
    text: str


class QueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]


# {'name': 'convert_currency', 'arguments': {'amount': 1, 'currency1': 'USD', 'currency2': 'BRL'}, 'output': {'amount': 1.0, 'base': 'USD', 'date': '2024-04-30', 'rates': {'BRL': 5.1248}}}
class ChainQueryOutput(BaseModel):
    name: str
    arguments: dict
    output: dict
