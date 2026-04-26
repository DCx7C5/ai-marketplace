"""
incident-management MCP Package
"""

from incident_management.tools import incident_creator, incident_updater, incident_resolver, playbook_executor, escalation_handler, notification_sender

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "incident_creator", "incident_updater", "incident_resolver", "playbook_executor", "escalation_handler", "notification_sender"
]
