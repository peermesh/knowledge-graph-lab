from . import __init__  # noqa: F401
from ..workers.celery_app import celery_app
from ..services.publication_service import PublicationService


@celery_app.task(name="publishing.process_due_publications")
async def process_due_publications():
    service = PublicationService()
    due = await service.get_due_publications()
    for pub in due:
        await service.mark_publication_processing(str(pub.id))
        # Placeholder: trigger actual multi-channel delivery workflow
        await service.mark_publication_completed(str(pub.id), channel_results={})


@celery_app.task(name="publishing.retry_failed_publications")
async def retry_failed_publications():
    service = PublicationService()
    # Placeholder for retry logic scanning failed publications
    return True
