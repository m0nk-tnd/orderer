from flask import Blueprint

from common.models import Order, Session

from .schemas import OrderOutputSchema

bp = Blueprint("admin", __name__, url_prefix="/api/v1")


@bp.route("/order", methods=["GET"])
def hello():
    session = Session()
    orders = session.query(Order).all()
    orders = OrderOutputSchema().dump(orders, many=True)
    result = {"orders": orders, "total": sum(x["cost"] for x in orders)}
    return result
