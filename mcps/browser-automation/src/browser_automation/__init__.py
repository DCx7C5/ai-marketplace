"""
browser-automation MCP Package
"""

from browser_automation.tools import headless_browser, screenshot_capture, click_element, type_text, navigate_url, wait_for_element

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "headless_browser", "screenshot_capture", "click_element", "type_text", "navigate_url", "wait_for_element"
]
