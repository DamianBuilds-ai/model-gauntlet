def paginate(rows, page, size):
    start = (page - 1) * size
    end = start + size
    return {
        "items": rows[start:end],
        "page": page,
        "size": size,
        "total": len(rows),
    }
