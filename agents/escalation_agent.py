import json
from datetime import datetime

class EscalationAgent:
    def __init__(self):
        self.escalation_triggers = [
            "angry", "furious", "terrible", "awful", "disgusting",
            "unacceptable", "ridiculous", "worst", "horrible", "scam",
            "fraud", "lawsuit", "lawyer", "never again",
            "social media", "complaint", "supervisor", "manager", "human",
            "escalate", "urgent", "right away", "immediately", "asap", "right now",
            "need now", "desperate", "emergency", "frustrated", "upset"
            "urgent", "right away", "immediately", "asap", "right now",
            "need now", "desperate", "emergency", "frustrated", "upset"
        ]

    def should_escalate(self, user_input):
        user_input_lower = user_input.lower()
        return any(trigger in user_input_lower for trigger in self.escalation_triggers)

    def handle(self, user_input, user_context={}):
        return self.process_escalation(user_input, user_context)

    def process_escalation(self, user_input, user_context):
        ticket_id = f"ESC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ticket = {
            "ticket_id": ticket_id,
            "timestamp": timestamp,
            "customer_message": user_input,
            "status": "pending",
            "priority": "high"
        }

        self.log_ticket(ticket)

        return (
            f"I completely understand your frustration and I sincerely apologize. "
            f"I have created an urgent support ticket for you (Ticket ID: {ticket_id}). "
            f"A senior member of our team will contact you within 2 hours. "
            f"Is there anything else I can note on your ticket?"
        )

    def log_ticket(self, ticket):
        try:
            with open('data/escalation_tickets.json', 'r') as f:
                tickets = json.load(f)
        except FileNotFoundError:
            tickets = []
        tickets.append(ticket)
        with open('data/escalation_tickets.json', 'w') as f:
            json.dump(tickets, f, indent=2)