from typing import Union
from pydantic import BaseModel, validator
from decimal import Decimal


class MakeOrder(BaseModel):
    instrument_id: int
    price: Decimal


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
