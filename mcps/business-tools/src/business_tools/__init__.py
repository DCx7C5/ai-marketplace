"""
business-tools MCP Package
"""

from business_tools.tools import email_client, calendar_manager, document_processor, report_generator, task_manager, notification_service

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "email_client", "calendar_manager", "document_processor", "report_generator", "task_manager", "notification_service"
]
