from northwind.db.queries import OrderQueries
from northwind.util.pagination import paginate


def search_orders(request):
    account_id = request.account.id
    term = request.query.get("q", "")
    q = OrderQueries(request.db)
    rows = q.search(account_id, term)
    return paginate(rows, page=1, size=25)
