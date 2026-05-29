class QueryAgent:
    def __init__(self):
        self.faqs = {
            "shipping": "We offer free shipping on orders over $50. Standard delivery takes 3-5 business days.",
            "payment": "We accept Visa, Mastercard, American Express, and PayPal.",
            "size guide": "Our sizes range from XS to XL. Check our size guide on each product page for measurements.",
            "store hours": "Our online store is open 24/7. Customer support is available Monday to Friday 9am-6pm.",
            "discount": "Sign up for our newsletter to receive 10% off your first order.",
        }

    def handle(self, user_input, user_context={}):
        return self.process_query(user_input)

    def process_query(self, user_input):
        user_input_lower = user_input.lower()

        for keyword, answer in self.faqs.items():
            if keyword in user_input_lower:
                return answer

        return (
            "Thank you for contacting Fashion Support. "
            "I am here to help with orders, returns, product recommendations, "
            "and general questions about our store. "
            "Could you please tell me more about what you need help with?"
        )