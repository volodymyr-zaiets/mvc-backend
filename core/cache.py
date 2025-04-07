import time
from threading import Lock
from typing import Any, Optional


class SimpleCache:
    """
    A thread-safe in-memory cache with a time-to-live (TTL) expiration mechanism.

    Attributes:
        ttl (int): Time-to-live in seconds for each cached entry.
        store (dict): Internal dictionary to hold cached items and their timestamps.
        lock (Lock): Thread lock to ensure safe concurrent access.
    """

    def __init__(self, ttl_seconds: int = 300):
        """
        Initializes the cache with a given TTL for items.

        Args:
            ttl_seconds (int): Time-to-live in seconds for each item (default is 300).
        """
        self.ttl = ttl_seconds
        self.store = {}
        self.lock = Lock()

    def set(self, key: Any, value: Any):
        """
        Stores a value in the cache under the given key.

        Args:
            key (Any): The key under which the value is stored.
            value (Any): The value to be cached.
        """
        with self.lock:
            self.store[key] = (value, time.time())

    def get(self, key: Any) -> Optional[Any]:
        """
        Retrieves a value from the cache if it has not expired.

        Args:
            key (Any): The key of the cached value to retrieve.

        Returns:
            Optional[Any]: The cached value if present and not expired, otherwise None.
        """
        with self.lock:
            item = self.store.get(key)
            if not item:
                return None

            value, timestamp = item
            # Check if the item is still valid based on TTL
            if time.time() - timestamp < self.ttl:
                return value
            else:
                # Expired item is removed from cache
                del self.store[key]
                return None

    def invalidate(self, key: Any):
        """
        Removes a key-value pair from the cache if it exists.

        Args:
            key (Any): The key to remove from the cache.
        """
        with self.lock:
            if key in self.store:
                del self.store[key]


# Global cache instance with 5-minute TTL
cache = SimpleCache(ttl_seconds=300)
