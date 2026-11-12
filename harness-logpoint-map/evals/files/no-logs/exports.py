import logging

logger = logging.getLogger("export")


def preview(items):
    return items[:3]


def export(items):
    logger.info("export_started count=%s", len(items))
    return tuple(items)
