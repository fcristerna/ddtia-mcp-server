from dotenv import load_dotenv
import os

load_dotenv()

# GHL Credentials
GHL_API_KEY        = os.getenv("GHL_API_KEY")
GHL_LOCATION_ID    = os.getenv("GHL_LOCATION_ID")
GHL_CALENDAR_ID    = os.getenv("GHL_CALENDAR_ID")
GHL_ASSIGNED_USER  = os.getenv("GHL_ASSIGNED_USER")

API_SECRET_KEY     = os.getenv("API_SECRET_KEY", "cambia-esto-en-produccion")

TIMEZONE           = os.getenv("TIMEZONE", "America/Mexico_City")

# Slots config
SLOT_DURATION_MIN  = int(os.getenv("SLOT_DURATION_MIN", "30"))
DAYS_AHEAD         = int(os.getenv("DAYS_AHEAD", "7"))

GHL_BASE_URL = "https://services.leadconnectorhq.com"

VAULT_PATH = os.getenv("VAULT_PATH", "/app/data/vault")
