from .sheet_services import register_sheet_services as register_sheet_services
from .sheet_google import register_google_services as register_google_services

def register_sheet(dp):
    register_sheet_services(dp)
    register_google_services(dp)
