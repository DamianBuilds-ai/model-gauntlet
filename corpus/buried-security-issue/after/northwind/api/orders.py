from northwind.db.queries import OrderQueries
from northwind.util.pagination import paginate


def list_orders(request, *, include_archived=False):
    """Return a page of orders for the current account."""
    account_id = request.account.id
    page = int(request.query.get("page", "1"))
    size = min(int(request.query.get("size", "25")), 100)
    q = OrderQueries(request.db)
    rows = q.for_account(account_id, page=page, size=size)
    if not include_archived:
        rows = [r for r in rows if r["status"] != "archived"]
    return paginate(rows, page=page, size=size)


def get_order(request, order_id):
    account_id = request.account.id
    q = OrderQueries(request.db)
    row = q.by_id(order_id, account_id=account_id)
    return row
