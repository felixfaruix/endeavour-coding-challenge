import json
import os
import redis
from dotenv import load_dotenv

load_dotenv()

class ConversationMemory:
    
    def __init__(self):

        redis_host = os.getenv("redis_host", "localhost")
        redis_port = int(os.getenv("redis_port", 6379))
        redis_password = os.getenv("redis_password", None)

        print(f"Redis host: {redis_host}")
        print(f"Redis port: {redis_port}")

        self.redis = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

        # Conversations expiring after 24 hours
        self.ttl = 60 * 60 * 24
    
    def _make_key(self, conversation_id: str) -> str:
        
        return f"conv:{conversation_id}"
    
    def get_messages(self, conversation_id: str) -> list:

        key = self._make_key(conversation_id)
        data = self.redis.get(key)
        
        if data is None:
            return []

        return json.loads(data) # type: ignore

    def save_messages(self, conversation_id: str, messages: list) -> None:

        key = self._make_key(conversation_id)
        data = json.dumps(messages)
        self.redis.set(key, data, ex=self.ttl)
    
    def delete_conversation(self, conversation_id: str) -> None:

        key = self._make_key(conversation_id)
        self.redis.delete(key)

memory = ConversationMemory()