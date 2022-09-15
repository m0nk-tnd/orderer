import asyncio
import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree

import requests
import telebot
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from common.config import Config
from common.models import Order, Session, check_and_create_tables
from grabber.schemas import OrderInputSchema


bot = telebot.TeleBot(Config.BOT_TOKEN)


def connect_and_read() -> Optional[List[List[Any]]]:
    """connects to google doc and read data"""
    try:
        service = build("sheets", "v4", developerKey=Config.API_KEY)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=Config.SPREADSHEET_ID, range=Config.RANGE_NAME)
            .execute()
        )
        return result.get("values", [])
    except HttpError as err:
        print(err)
        return None


def write_orders(values: List[List[Any]], rate: Decimal) -> None:
    """write orders into DB"""
    session = Session()

    # reformat and validate new values
    orders = [
        {"id": val[0], "order_number": val[1], "cost": val[2], "delivery_date": val[3]}
        for val in values
    ]
    orders = OrderInputSchema(many=True).load(orders)

    # get orders from DB
    existed_orders = session.query(Order.id, Order.hash).all()
    existed_orders = {x.id: x.hash for x in existed_orders}
    order_ids = set([x["id"] for x in orders])

    # create id lists of new orders and orders for delete
    to_create = order_ids.difference(existed_orders.keys())
    to_delete = set(existed_orders.keys()).difference(order_ids)
    orders_to_create = []
    # create new orders entities
    for order in orders:
        if order["id"] in to_create:
            orders_to_create.append(
                Order(
                    **order, cost_rub=calc_cost_rub(order, rate), hash=calc_hash(order)
                )
            )
            continue
        # check if order change and update it
        existed_order_hash = existed_orders[order["id"]]
        order_hash = calc_hash(order)
        if order_hash != existed_order_hash:
            session.query(Order).where(Order.id == order["id"]).update(
                {
                    Order.order_number: order["order_number"],
                    Order.cost: order["cost"],
                    Order.delivery_date: order["delivery_date"],
                    Order.cost_rub: calc_cost_rub(order, rate),
                    Order.hash: order_hash,
                }
            )
    # delete old and create new orders
    session.query(Order).filter(Order.id.in_(to_delete)).delete()
    session.add_all(orders_to_create)
    session.commit()


def calc_hash(order: Dict) -> str:
    return f"{order['id']}*{order['order_number']}*{order['delivery_date']}*{order['cost']}"


def calc_cost_rub(order: Dict, rate: Decimal) -> Decimal:
    return Decimal(
        order["cost"] * rate,
    )


def get_rate_from_server() -> Optional[Decimal]:
    """Connects to the rate server and gets the rate"""
    try:
        res = requests.get(Config.RATE_SERVER, timeout=10)
        if res:
            usd = ElementTree.fromstring(res.text).find(Config.CURRENCY_SEARCH_STRING)
            if usd:
                return Decimal(usd.find("Value").text.replace(",", "."))
    except (TimeoutError, ElementTree.ParseError):
        pass


def check_and_send_notifications() -> None:
    """Check if there are new orders and send notifications"""
    # select orders to notify
    session = Session()
    orders_for_notifications = (
        session.query(Order.order_number)
        .filter(
            Order.is_message_sent == False,
            Order.delivery_date < datetime.datetime.now(),
        )
        .all()
    )
    orders_for_notifications = [
        order.order_number for order in orders_for_notifications
    ]

    for order in orders_for_notifications:
        bot.send_message(Config.CHAT_ID, f"Order #{order} out of date")

    # update notification flag
    session.query(Order).filter(
        Order.order_number.in_(orders_for_notifications)
    ).update({Order.is_message_sent: True})
    session.commit()


async def main() -> None:

    while True:
        print("run sync")
        rate = get_rate_from_server()
        values = connect_and_read()
        if values is not None:
            write_orders(values, rate)
        check_and_send_notifications()
        print("wait...")
        await asyncio.sleep(Config.PROGRAM_DELAY_SEC)


if __name__ == "__main__":
    check_and_create_tables()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
