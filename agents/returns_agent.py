import json
from datetime import datetime, timedelta

class ReturnsAgent:
    def __init__(self):
        self.return_window_days = 30
        self.refund_processing_days = 5
        try:
            with open('data/sample_data.json', 'r') as f:
                data = json.load(f)
                self.orders = data.get("orders", [])
        except FileNotFoundError:
            self.orders = []

    def handle(self, user_input, user_context={}):
        return self.process_return_query(user_input, user_context)

    def process_return_query(self, user_input, user_context):
        user_input_lower = user_input.lower()
        if any(word in user_input_lower for word in ["refund", "money back", "charge"]):
            return self.handle_refund_query()
        if any(word in user_input_lower for word in ["exchange", "swap", "different size", "different color"]):
            return self.handle_exchange_query()
        return self.handle_return_query()

    def handle_return_query(self):
        return (
            f"Our fashion store accepts returns within {self.return_window_days} days of purchase. "
            "Items must be unworn, unwashed, and have original tags attached. "
            "Please provide your order number and we will send you a prepaid return label."
        )

    def handle_refund_query(self):
        refund_date = (datetime.now() + timedelta(days=self.refund_processing_days)).strftime("%B %d, %Y")
        return (
            f"Refunds are processed within {self.refund_processing_days} business days. "
            f"If you initiate a return today, expect your refund by {refund_date}. "
            "Do you have an order number I can look up?"
        )

    def handle_exchange_query(self):
        return (
            "We offer free exchanges within 30 days of purchase. "
            "We can swap for a different size or color while stock lasts. "
            "Please share your order number and what you would like to exchange for."
        )