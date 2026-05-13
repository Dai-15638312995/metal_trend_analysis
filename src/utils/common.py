"""
Common retry utilities for the Metal Trend Analysis project.
"""
import time
import functools
from typing import Callable, Type, Union, Tuple, Any
from loguru import logger

from .exceptions import RetryableError


def with_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = (RetryableError,),
    logger_name: str = None
):
    """
    Decorator that adds retry functionality to functions.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Factor to multiply delay by after each retry
        exceptions: Exception types to retry on
        logger_name: Name for logger (defaults to function name)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            func_logger = logger.bind(name=logger_name or func.__name__)

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        func_logger.error(f"Final attempt failed: {e}")
                        raise

                    func_logger.warning(f"Attempt {attempt + 1} failed: {e}, retrying in {current_delay}s")
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
                except Exception as e:
                    # Don't retry for non-retryable exceptions
                    func_logger.error(f"Non-retryable error: {e}")
                    raise

            return None  # Should never reach here

        return wrapper
    return decorator


def validate_config(config: dict, required_keys: list, config_name: str = "Configuration") -> None:
    """
    Validate that configuration contains required keys.

    Args:
        config: Configuration dictionary to validate
        required_keys: List of required key names
        config_name: Name of configuration for error messages

    Raises:
        ConfigurationError: If required keys are missing
    """
    from .exceptions import ConfigurationError

    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ConfigurationError(f"{config_name} missing required keys: {missing_keys}")


def safe_execute(func: Callable, default_value: Any = None, logger_name: str = None) -> Any:
    """
    Execute a function safely, returning a default value if it fails.

    Args:
        func: Function to execute
        default_value: Value to return if function fails
        logger_name: Name for logger

    Returns:
        Function result or default value
    """
    func_logger = logger.bind(name=logger_name or func.__name__)

    try:
        return func()
    except Exception as e:
        func_logger.warning(f"Function {func.__name__} failed: {e}, returning default value")
        return default_value
