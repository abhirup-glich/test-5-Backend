import logging
import os
from datetime import datetime

# Setup logging configuration
log_directory = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_directory, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_directory, 'audit.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AuditService:
    @staticmethod
    def log_action(user_id, action, details=None):
        """
        Log an admin action.
        :param user_id: ID of the user performing the action
        :param action: Description of the action (e.g., "REGISTER_STUDENT")
        :param details: Dictionary containing additional details
        """
        timestamp = datetime.now().isoformat()
        log_entry = f"User: {user_id} | Action: {action}"
        if details:
            log_entry += f" | Details: {details}"
        
        # Log to file
        logging.info(log_entry)
        
        # Print to console for immediate visibility during dev
        print(f"[AUDIT] {log_entry}")

        # Future: Insert into database (AuditLogs table)
