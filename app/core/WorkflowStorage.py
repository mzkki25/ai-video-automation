from typing import Dict, Any
from app.core.Setting import setting

import redis
import json

class WorkflowStorage:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkflowStorage, cls).__new__(cls)
            import os
            cls._instance.redis_client = redis.Redis(
                host=setting.REDIS_HOST,
                port=int(setting.REDIS_PORT),
                decode_responses=True
            )
        return cls._instance
    
    def set(self, workflow_id: str, data: Dict[str, Any]):
        self.redis_client.set(f"workflow:{workflow_id}", json.dumps(data), ex=86400)  # 24 hours TTL
    
    def get(self, workflow_id: str) -> Dict[str, Any]:
        data = self.redis_client.get(f"workflow:{workflow_id}")
        return json.loads(data) if data else None
    
    def delete(self, workflow_id: str):
        self.redis_client.delete(f"workflow:{workflow_id}")

workflow_storage = WorkflowStorage()
