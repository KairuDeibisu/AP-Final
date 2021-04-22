import logging

logger = logging.getLogger(__name__)


def _format_tags_callback(tags: str) -> list:

    return [tag.strip().lower().replace(" ", "-") for tag in tags]
