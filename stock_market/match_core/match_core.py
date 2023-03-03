from collections import deque
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Order:
    owner_id: int
    instrument: str
    side_of_deal: str
    amount: int
    price: Decimal


class IncreasedSortedLinkedList(deque):
    def sorted_insert(self, element_to_insert):
        # insert in a right possition in sorted list
        index = 0
        for element in self:
            if element > element_to_insert:
                self.insert(index, element_to_insert)
                return
            index += 1
        self.append(element_to_insert)



class DecreasedSortedLinkedList(deque):
    def sorted_insert(self, element_to_insert):
        # insert in a right possition in sorted list
        index = 0
        for element in self:
            if element < element_to_insert:
                self.insert(index, element_to_insert)
                return
            index += 1
        self.append(element_to_insert)



def make_deal(ask: Order, bid: Order):
    # make deal with two order
    minus = min(ask.amount, bid.amount)
    ask.amount -= minus
    bid.amount -= minus
    pass


class StocksGlass:
    def __init__(self):
        self.ask = {}
        self.ask_price_ordered = IncreasedSortedLinkedList()
        self.bid = {}
        self.bid_price_ordered = DecreasedSortedLinkedList()


list_of_isntrument = ['HP']  # list with all accessible instrument
all_instruments = {}  # dict with type structure:  instrument_name: StockGlass object


def fill_all_instruments(all_instruments: dict, list_of_isntrument: list):
    """
    add all accessible instruments in all_instruments
    """
    for instrument in list_of_isntrument:
        all_instruments[instrument] = StocksGlass()


def take_new_ask_order(ask_order: Order, stocks_glass: StocksGlass):
    bid_price_ordered = stocks_glass.bid_price_ordered
    while bid_price_ordered and ask_order.price <= bid_price_ordered[0]:
        deq_of_bid_lowest_price = stocks_glass.bid[bid_price_ordered[0]]
        while deq_of_bid_lowest_price and ask_order.amount:
            bid_order = deq_of_bid_lowest_price[0]
            make_deal(ask_order, bid_order)
            if bid_order.amount == 0:
                deq_of_bid_lowest_price.popleft()
        if ask_order.amount == 0:
            break
        if not deq_of_bid_lowest_price:
            del stocks_glass.bid[bid_price_ordered[0]]
            bid_price_ordered.popleft()

    if ask_order.amount:
        if ask_order.price in stocks_glass.ask:
            stocks_glass.ask[ask_order.price].append(ask_order)
        else:
            stocks_glass.ask_price_ordered.sorted_insert(ask_order.price)
            stocks_glass.ask[ask_order.price] = deque([ask_order])
    pass


def take_new_bid_order(bid_order: Order, stocks_glass: StocksGlass):
    ask_price_ordered = stocks_glass.ask_price_ordered
    while ask_price_ordered and bid_order.price >= ask_price_ordered[0]:
        deq_of_ask_lowest_price = stocks_glass.ask[ask_price_ordered[0]]
        while deq_of_ask_lowest_price and bid_order.amount:
            ask_order = deq_of_ask_lowest_price[0]
            make_deal(ask_order, bid_order)
            if ask_order.amount == 0:
                deq_of_ask_lowest_price.popleft()
        if bid_order.amount == 0:
            break
        if not deq_of_ask_lowest_price:
            del stocks_glass.ask[ask_price_ordered[0]]
            ask_price_ordered.popleft()

    if bid_order.amount:
        if bid_order.price in stocks_glass.bid:
            stocks_glass.bid[bid_order.price].append(bid_order)
        else:
            stocks_glass.bid_price_ordered.sorted_insert(bid_order.price)
            stocks_glass.bid[bid_order.price] = deque([bid_order])

    pass


def take_new_order(order: Order):
    stocks_glass = all_instruments[order.instrument]
    if order.side_of_deal == 'ask':
        take_new_ask_order(order, stocks_glass)
    elif order.side_of_deal == 'bid':
        take_new_bid_order(order, stocks_glass)



a = DecreasedSortedLinkedList()

a.append(1)
a.sorted_insert(4)
a.sorted_insert(3)
print(a)

order_obj = Order(owner_id=1, instrument='HP', side_of_deal='bid', amount=3, price=Decimal(100))

fill_all_instruments(all_instruments, list_of_isntrument)
take_new_order(order_obj)
print(all_instruments)
print((all_instruments['HP'].bid))

order_obj2 = Order(owner_id=1, instrument='HP', side_of_deal='bid', amount=3, price=Decimal(200))
take_new_order(order_obj2)

order_obj3 = Order(owner_id=1, instrument='HP', side_of_deal='bid', amount=3, price=Decimal(50))
order_obj5 = Order(owner_id=1, instrument='HP', side_of_deal='bid', amount=96, price=Decimal(200))
take_new_order(order_obj3)
take_new_order(order_obj5)
print((all_instruments['HP'].bid))
print((all_instruments['HP'].bid_price_ordered))


order_obj4 = Order(owner_id=1, instrument='HP', side_of_deal='ask', amount=100, price=Decimal(90))
take_new_order(order_obj4)

print((all_instruments['HP'].bid))
print((all_instruments['HP'].bid_price_ordered))
print((all_instruments['HP'].ask))