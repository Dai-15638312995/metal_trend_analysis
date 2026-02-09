"""
News Sources Module
"""
from typing import List, Dict, Any
from loguru import logger

from ..utils.exceptions import ValidationError, ConfigurationError
from ..utils.common import validate_config


def get_news_sources_from_config(config: Dict[str, Any], enabled_only: bool = True) -> List[Dict[str, Any]]:
    """
    Get news sources from configuration

    Args:
        config: News configuration dictionary
        enabled_only: If True, only return enabled sources

    Returns:
        List of news source configurations

    Raises:
        ValidationError: If configuration is invalid
        ConfigurationError: If sources configuration is malformed
    """
    module_logger = logger.bind(name="news_sources")

    try:
        # Validate basic configuration structure
        validate_config(config, [], "News config")

        sources = config.get('sources', [])

        if not isinstance(sources, list):
            raise ConfigurationError("News sources must be a list")

        # Validate each source
        validated_sources = []
        for idx, source in enumerate(sources):
            try:
                validated_source = _validate_news_source(source, idx)
                if enabled_only and not validated_source.get('enabled', True):
                    continue
                validated_sources.append(validated_source)
            except ValidationError as e:
                module_logger.warning(f"Skipping invalid news source at index {idx}: {e}")
                continue

        module_logger.info(f"Loaded {len(validated_sources)} news sources (enabled_only={enabled_only})")
        return validated_sources

    except Exception as e:
        module_logger.error(f"Error loading news sources: {e}")
        if isinstance(e, (ValidationError, ConfigurationError)):
            raise
        raise ConfigurationError(f"Failed to load news sources: {e}")


def _validate_news_source(source: Dict[str, Any], index: int = None) -> Dict[str, Any]:
    """
    Validate a single news source configuration

    Args:
        source: News source configuration
        index: Source index for error messages

    Returns:
        Validated source configuration

    Raises:
        ValidationError: If source configuration is invalid
    """
    if not isinstance(source, dict):
        raise ValidationError(f"News source at index {index} must be a dictionary")

    # Required fields
    required_fields = ['name', 'url', 'type']
    missing_fields = [field for field in required_fields if not source.get(field)]
    if missing_fields:
        raise ValidationError(f"News source missing required fields: {missing_fields}")

    # Validate URL
    url = source['url']
    if not isinstance(url, str) or not url.strip():
        raise ValidationError("News source URL must be a non-empty string")

    if not url.startswith(('http://', 'https://')):
        raise ValidationError("News source URL must start with http:// or https://")

    # Validate type
    source_type = source['type']
    supported_types = ['rss']
    if source_type not in supported_types:
        raise ValidationError(f"News source type '{source_type}' not supported. Supported types: {supported_types}")

    # Validate optional fields
    validated_source = {
        'name': str(source['name']).strip(),
        'url': url.strip(),
        'type': source_type,
        'enabled': bool(source.get('enabled', True)),
        'timeout': max(1, int(source.get('timeout', 15))),  # Minimum 1 second
        'max_articles': max(1, int(source.get('max_articles', 10)))  # Minimum 1 article
    }

    return validated_source


def get_builtin_news_sources() -> List[Dict[str, Any]]:
    """
    Get built-in news sources as fallback

    Returns:
        List of built-in news source configurations
    """
    return [
        {
            'name': 'Bloomberg Markets',
            'url': 'https://feeds.bloomberg.com/markets/news.rss',
            'type': 'rss',
            'enabled': True,
            'timeout': 15,
            'max_articles': 10
        },
        {
            'name': 'Reuters Business',
            'url': 'https://feeds.reuters.com/reuters/businessNews',
            'type': 'rss',
            'enabled': True,
            'timeout': 15,
            'max_articles': 10
        }
    ]


def merge_sources_with_builtin(configured_sources: List[Dict[str, Any]], use_builtin: bool = False) -> List[Dict[str, Any]]:
    """
    Merge configured sources with built-in sources

    Args:
        configured_sources: Sources from configuration
        use_builtin: Whether to include built-in sources

    Returns:
        Merged list of sources
    """
    if not use_builtin:
        return configured_sources

    builtin_sources = get_builtin_news_sources()

    # Deduplicate by URL
    seen_urls = {source['url'] for source in configured_sources}
    unique_builtin = [source for source in builtin_sources if source['url'] not in seen_urls]

    return configured_sources + unique_builtin
