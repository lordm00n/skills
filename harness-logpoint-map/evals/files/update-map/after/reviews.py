import logging

logger = logging.getLogger("review")


def approve(cr, enqueue):
    try:
        ticket = enqueue(cr)
    except Exception as error:
        logger.exception(
            "review_failure action=approve cr_id=%s error=%s",
            cr.id, error,
        )
        raise
    logger.info("review_finished cr_id=%s", cr.id)
    return ticket
