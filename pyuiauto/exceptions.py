
# ================== Component Exceptions ==================

class InvalidElement(RuntimeError):
    """Raises when an invalid element is passed"""
    pass


class ElementNotVisible(RuntimeError):
    """Raised when an element is not visible"""
    pass


class ElementNotFound(RuntimeError):
    """Raised when an element is not found"""
    pass

class WindowNotFound(RuntimeError):
    """Raised when a window is not found"""
    pass

# ================= Application Exceptions =================

class ProcessNotFoundError(Exception):
    """Could not find that process"""
    pass


class AppNotConnected(Exception):
    """Application has not been connected to a process yet"""
    pass

# ==========================================================
