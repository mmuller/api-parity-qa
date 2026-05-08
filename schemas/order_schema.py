order_schema = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "order_id": {"type": "number"},
        "amount": {"type": "number"},
    },
    "required": ["success", "order_id", "amount"],
}
