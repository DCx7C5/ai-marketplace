"""
playwright-automation MCP Package
"""

from playwright_automation.tools import browser_launcher, page_navigator, element_finder, click_handler, type_handler, screenshot_taker, pdf_generator, cookie_manager, intercept_handler, wait_handler, keyboard_handler, mouse_handler, video_recorder

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "browser_launcher", "page_navigator", "element_finder", "click_handler", "type_handler", "screenshot_taker", "pdf_generator", "cookie_manager", "intercept_handler", "wait_handler", "keyboard_handler", "mouse_handler", "video_recorder"
]
