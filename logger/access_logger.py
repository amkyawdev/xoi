"""Access logging"""

from datetime import datetime


class AccessLogger:
    """Log access to resources"""
    
    def __init__(self, log_file: str | None = None):
        self.log_file = log_file
        self.logger = __import__("logger").logger.get_logger("access")
    
    def log_access(
        self,
        user: str | None,
        resource: str,
        action: str,
        ip: str | None = None,
        user_agent: str | None = None
    ) -> None:
        """Log access event"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user": user,
            "resource": resource,
            "action": action,
            "ip": ip,
            "user_agent": user_agent
        }
        
        self.logger.info("access", **entry)
        
        if self.log_file:
            self._write_to_file(entry)
    
    def _write_to_file(self, entry: dict) -> None:
        """Write access log to file"""
        import json
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
