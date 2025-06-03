from .pending_handler import register_handlers as register_pending_handlers
from .list_handler import register_handlers as register_list_handlers
from .add_handler import register_handlers as register_add_handlers
from .start_handler import register_handlers as register_start_handlers

def register_handlers(dp):
    register_list_handlers(dp)
    register_pending_handlers(dp)
    register_add_handlers(dp)
    register_start_handlers(dp)  # URUTANNYA PENTING, jangan tumpuk def-nya
