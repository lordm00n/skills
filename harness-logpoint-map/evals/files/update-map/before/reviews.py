import logging

logger = logging.getLogger("review")


def approve(cr, merge):
    try:
        merged = merge(cr)
    except Exception as error:
        logger.exception(
            "review_action action=approve cr_id=%s result=error error=%s",
            cr.id, error,
        )
        raise
    logger.debug("review_persisted cr_id=%s", cr.id)
    logger.info("review_finished cr_id=%s", cr.id)
    return merged
