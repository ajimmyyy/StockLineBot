import requests
from langchain.agents import tool

@tool
def check_site_alive(site: str) -> bool:
    """Check a site is alive or not."""
    try:
        resp = requests.get(f'https://{site}')
        resp.raise_for_status()
        return True
    except Exception:
        return False