import os

DEFAULT_SYSTEM_PROMPT = "You are an assistant who answers concisely and informatively."
DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com"
API_KEY = os.getenv('DIAL_API_KEY', "")  ## put your key here
DEPLOYMENT_NAME = "gpt-4o"  # You can change this to other available models