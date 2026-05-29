import json

class OrderAgent:
    def __init__(self):
        try:
            with open('data/sample_data.json', 'r') as f:
                data = json.load(f)
                self.orders = data.get("orders", [])
        except FileNotFoundError:
            self.orders = []

    def handle(self, user_input, user_context={}):
        return self.process_order_query(user_input)

    def process_order_query(self, user_input):
        for order in self.orders:
            if order["order_id"].lower() in user_input.lower():
                return (
                    f"Order {order['order_id']} for {order['customer_name']}: "
                    f"Status is {order['status'].upper()}. "
                    f"Items: {', '.join(order['items'])}. "
                    f"Estimated delivery: {order['estimated_delivery']}."
                )
        return (
            "Please provide your order number (example: ORD-001) "
            "and I will look it up for you right away."
        )