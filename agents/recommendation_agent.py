import json

class RecommendationAgent:
    def __init__(self):
        try:
            with open('data/sample_data.json', 'r') as f:
                data = json.load(f)
                self.products = data.get("products", [])
        except FileNotFoundError:
            self.products = []

    def handle(self, user_input, user_context={}):
        return self.generate_recommendations(user_input)

    def generate_recommendations(self, user_input):
        user_input_lower = user_input.lower()
        matched = [
            p for p in self.products
            if any(
                keyword in p["name"].lower() or keyword in p["category"].lower()
                for keyword in user_input_lower.split()
            )
        ]

        if matched:
            results = []
            for p in matched[:3]:
                stock = "In stock" if p["in_stock"] else "Out of stock"
                results.append(
                    f"{p['name']} - ${p['price']} "
                    f"(Sizes: {', '.join(p['sizes'])}) - {stock}"
                )
            return (
                "Here are some items that match your interest:\n" +
                "\n".join(results) +
                "\nWould you like more details on any of these?"
            )

        return (
            "I would love to help you find the perfect outfit. "
            "We have dresses, tops, bottoms, shoes, and outerwear. "
            "Could you tell me more about what you are looking for — "
            "occasion, style, or budget?"
        )