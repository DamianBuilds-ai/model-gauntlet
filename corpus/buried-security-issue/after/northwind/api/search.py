from northwind.db.queries import OrderQueries
from northwind.util.pagination import paginate

ALLOWED_SORTS = {"created_at", "total", "status", "customer_name"}


def search_orders(request):
    """Saved-search endpoint. Supports a text term, a status filter, and a
    user-chosen sort column."""
    account_id = request.account.id
    term = request.query.get("q", "")
    status = request.query.get("status")
    sort = request.query.get("sort", "created_at")
    direction = request.query.get("dir", "desc").lower()
    if direction not in ("asc", "desc"):
        direction = "desc"
    page = int(request.query.get("page", "1"))
    size = min(int(request.query.get("size", "25")), 100)
    q = OrderQueries(request.db)
    rows = q.search(
        account_id,
        term,
        status=status,
        sort_column=sort,
        direction=direction,
    )
    return paginate(rows, page=page, size=size)
