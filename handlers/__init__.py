from .update_handler import register_handlers as register_update_handlers
from .list_handler import register_handlers as register_list_handlers
from .start_handler import register_handlers as register_start_handlers

def register_handlers(dp):
    register_list_handlers(dp)
    register_update_handlers(dp)
    register_start_handlers(dp)
