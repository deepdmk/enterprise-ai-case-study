"""Retry utilities with exponential backoff for network-dependent operations.

Provides decorators and helpers for retrying operations that may fail due to
transient network or service errors (database connections, HTTP calls, etc.).

Usage:
    from config.retry import with_retry, async_with_retry

    @with_retry(max_attempts=3, base_delay=1.0)
    def fetch_data():
        return requests.get("http://example.com/api")

    @async_with_retry(max_attempts=3, base_delay=1.0)
    async def async_fetch():
        async with httpx.AsyncClient() as client:
            return await client.get("http://example.com/api")
"""

import asyncio
import functools
import random
import time
from collections.abc import Callable
from typing import Any, TypeVar

import structlog

logger = structlog.get_logger(__name__)

T = TypeVar("T")

# Default retryable exceptions
RETRYABLE_EXCEPTIONS: tuple[type[Exception], ...] = (
    ConnectionError,
    TimeoutError,
    OSError,
)


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: tuple[type[Exception], ...] | None = None,
) -> Callable:
    """Decorator for retrying synchronous functions with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts (including the first one)
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Add random jitter to prevent thundering herd
        retryable_exceptions: Tuple of exception types to retry on.
            Defaults to ConnectionError, TimeoutError, OSError.
    """
    exceptions = retryable_exceptions or RETRYABLE_EXCEPTIONS

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            delay = base_delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(
                            "retry_exhausted",
                            function=func.__name__,
                            attempts=max_attempts,
                            error=str(e),
                        )
                        raise

                    actual_delay = delay
                    if jitter:
                        actual_delay = delay * (0.5 + random.random())
                    actual_delay = min(actual_delay, max_delay)

                    logger.warning(
                        "retry_attempt",
                        function=func.__name__,
                        attempt=attempt,
                        max_attempts=max_attempts,
                        delay=round(actual_delay, 2),
                        error=str(e),
                    )
                    time.sleep(actual_delay)
                    delay *= backoff_factor

            raise last_exception  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]
    return decorator


def async_with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: tuple[type[Exception], ...] | None = None,
) -> Callable:
    """Decorator for retrying async functions with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts (including the first one)
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Add random jitter to prevent thundering herd
        retryable_exceptions: Tuple of exception types to retry on.
            Defaults to ConnectionError, TimeoutError, OSError.
    """
    exceptions = retryable_exceptions or RETRYABLE_EXCEPTIONS

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            delay = base_delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(
                            "retry_exhausted",
                            function=func.__name__,
                            attempts=max_attempts,
                            error=str(e),
                        )
                        raise

                    actual_delay = delay
                    if jitter:
                        actual_delay = delay * (0.5 + random.random())
                    actual_delay = min(actual_delay, max_delay)

                    logger.warning(
                        "retry_attempt",
                        function=func.__name__,
                        attempt=attempt,
                        max_attempts=max_attempts,
                        delay=round(actual_delay, 2),
                        error=str(e),
                    )
                    await asyncio.sleep(actual_delay)
                    delay *= backoff_factor

            raise last_exception  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]
    return decorator
