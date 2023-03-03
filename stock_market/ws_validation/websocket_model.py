from typing import Union
from pydantic import BaseModel, validator
from decimal import Decimal


class MakeOrder(BaseModel):
    instrument_id: int
    side_of_deal: str
    price: Decimal

    @validator('side_of_deal')
    def command_exist(cls, side: str):
        if side in {'Ask', 'Bid'}:
            return side
        raise ValueError('Incorrect side of deal.')


class CancelOrder(BaseModel):
    order_id: int


class WsMessage(BaseModel):
    type: str
    payload: Union[MakeOrder, CancelOrder]

    @validator('type')
    def command_exist(cls, command):
        if command in {'MakeOrder', 'CancelOrder'}:
            return command
        raise ValueError('The command does not exist.')



input_json = """
{   
    "type": "MakeOrder",
    "payload": { "instrument_id": 11, "price": 14.88 }
}
"""

input_json_make_ord = """
{
    "instrument_id": 11,
    "price": 14.88
}
"""
order = MakeOrder.parse_raw(input_json_make_ord)
print(order)

ws_mes = WsMessage.parse_raw(input_json)
print(ws_mes)