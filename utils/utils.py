from datetime import datetime

def log_request(message, agent='unknown'):
    print(f'[{datetime.now()}] {agent}: {message}')

def format_response(response, agent_used='unknown'):
    return {'response': response, 'agent_used': agent_used, 'status': 'success'}
