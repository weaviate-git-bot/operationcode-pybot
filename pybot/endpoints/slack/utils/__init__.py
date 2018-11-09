import os

from dotenv import load_dotenv

load_dotenv()

MENTOR_CHANNEL = os.environ.get("MENTOR_CHANNEL") or "G1DRT62UC"
COMMUNITY_CHANNEL = os.environ.get("COMMUNITY_CHANNEL") or "G12343"
MODERATOR_CHANNEL = os.environ.get('REPORT_CHANNEL') or 'G8NDRJJF9'
TICKET_CHANNEL = os.environ.get('TICKET_CHANNEL') or 'G8NDRJJF9'
APP_TOKEN = os.environ.get('APP_TOKEN') or "123"
YELP_TOKEN = os.environ.get('YELP_TOKEN') or 'token'
PYBACK_HOST = os.environ.get('PYBACK_HOST') or 'pyback'
PYBACK_PORT = os.environ.get('PYBACK_PORT') or 8000
PYBACK_TOKEN = os.environ.get('PYBACK_TOKEN') or 'token'