import logging

logger = logging.getLogger("review")


def approve(cr, actor, merge):
    if cr is None:
        raise LookupError("missing change request")
    if not actor:
        raise PermissionError("missing actor")
    try:
        merged = merge(cr)
    except ValueError as error:
        logger.warning(
            "review_action action=approve cr_id=%s result=rejected_400 error=%s",
            cr.id, error,
        )
        raise
    except Exception as error:
        logger.exception(
            "review_action action=approve cr_id=%s result=error error=%s",
            cr.id, error,
        )
        raise
    logger.info(
        "review_action action=approve cr_id=%s result=merged version=%s",
        cr.id, merged.version,
    )
    return merged


def reject(cr):
    logger.info("review_action action=reject cr_id=%s", cr.id)


def batch_approve(ids):
    logger.info("review_action action=batch-approve count=%s", len(ids))


def export(job_id):
    logger.info("export_action job_id=%s result=ready", job_id)
