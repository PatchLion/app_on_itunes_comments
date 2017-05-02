from enum import Enum
class RecordOpratorType(Enum):
    Error = -1
    Insert = 0
    Update = 1

from database_manager.database_manager import DataManager, Comments

data_manager = DataManager()