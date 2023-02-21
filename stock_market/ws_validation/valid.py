from typing import Union

from pydantic import BaseModel, validator
from decimal import Decimal

class MakeOrder(BaseModel):
    istr_id: int
    price: Decimal



class CancelOrder(BaseModel):
    order_id: int



class GetQuote(BaseModel):
    istr_id: int
    price: Decimal




class WsMessage(BaseModel):
    type: str
    payload: Union[MakeOrder, CancelOrder, GetQuote]

    @validator('type')
    def command_is_exist(cls, command):
        if command in {'MakeOrder', 'CancelOrder', 'GetQuote'}:
            return command
        raise ValueError('The command does not exist.')