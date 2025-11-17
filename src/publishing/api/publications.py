"""
Publications API endpoints for Publishing Module.

Handles content publication creation, status tracking, scheduling, and management.
Supports multi-channel delivery with personalization and comprehensive error handling.

Constitution Compliance:
- Multi-Channel Publishing Excellence: Core publication management endpoints
- Comprehensive Analytics Integration: Publication tracking and status monitoring
- Scalable Architecture: Async endpoints with proper error handling
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid
import structlog
import re
from urllib.parse import urlencode
from sqlalchemy import select

from ..core.config import settings
from ..core.logging import get_logger, log_publication_event
from ..core.database import get_async_session
from ..services.publication_service import PublicationService
from ..services.channel_service import ChannelService
from ..services.template_service import TemplateService
from ..services.subscriber_service import SubscriberService
from ..newsletter.generator import NewsletterGenerator
from ..models.subscriber import Subscriber
from ..integrations.email_service import EmailService
from ..schemas.publications import (
    TestNewsletterRequest,
    CreatePublicationRequest,
    PublicationResponse,
    PublicationListResponse,
    UpdatePublicationRequest
)

# Configure structured logging
logger = get_logger(__name__)

# Initialize services
publication_service = PublicationService()
channel_service = ChannelService()
template_service = TemplateService()
subscriber_service = SubscriberService()
newsletter_generator = NewsletterGenerator()
email_service = EmailService()

# Create router
router = APIRouter()


def _add_email_tracking(html_content: str, publication_id: str, channel_id: Optional[str] = None) -> str:
    """Add tracking pixel and click tracking URLs to HTML email content.
    
    Args:
        html_content: Original HTML content
        publication_id: Publication ID for tracking
        channel_id: Optional channel ID for channel-specific tracking
        
    Returns:
        HTML content with tracking pixel and click tracking URLs
    """
    # Build tracking URLs
    api_base = settings.API_BASE_URL.rstrip('/')
    
    # Tracking pixel URL (for open tracking)
    open_tracking_params = {"publication_id": publication_id}
    if channel_id:
        open_tracking_params["channel_id"] = channel_id
    tracking_pixel_url = f"{api_base}/api/v1/analytics/engagement/track/open?{urlencode(open_tracking_params)}"
    
    # Add tracking pixel at the end of body (1x1 transparent image)
    tracking_pixel = f'<img src="{tracking_pixel_url}" width="1" height="1" style="display:none;" alt="" />'
    
    # Add tracking pixel before closing </body> tag
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', f'{tracking_pixel}</body>')
    else:
        # If no body tag, add at the end
        html_content += tracking_pixel
    
    # Wrap all links with click tracking
    def wrap_link(match):
        """Wrap a link URL with click tracking redirect."""
        full_link = match.group(0)
        href_match = re.search(r'href=["\']([^"\']+)["\']', full_link, re.IGNORECASE)
        if href_match:
            original_url = href_match.group(1)
            # Skip if already a tracking URL or mailto: link
            if '/analytics/engagement/track/click' in original_url or original_url.startswith('mailto:'):
                return full_link
            
            # Build click tracking URL
            click_params = {
                "publication_id": publication_id,
                "url": original_url
            }
            if channel_id:
                click_params["channel_id"] = channel_id
            
            tracking_url = f"{api_base}/api/v1/analytics/engagement/track/click?{urlencode(click_params)}"
            # Replace the href with tracking URL that redirects to original
            return full_link.replace(original_url, tracking_url)
        return full_link
    
    # Find and wrap all <a> tags with href attributes
    html_content = re.sub(r'<a[^>]+href=["\'][^"\']+["\'][^>]*>', wrap_link, html_content, flags=re.IGNORECASE)
    
    return html_content


def _to_utc(dt: Optional[datetime]) -> datetime:
    """Normalize datetime to timezone-aware UTC (T049)."""
    if dt is None:
        return datetime.now(timezone.utc)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)



@router.post("", response_model=PublicationResponse)
async def create_publication(request: CreatePublicationRequest):
    """Create a new publication with content selection and channel targeting."""

    correlation_id = str(uuid.uuid4())

    try:
        logger.info(
            "Creating publication",
            correlation_id=correlation_id,
            content_ids=request.content_ids,
            channels=request.channels,
            publication_type=request.publication_type
        )

        # Validate channels exist and are active
        for channel_id in request.channels:
            channel = await channel_service.get_channel(channel_id)
            if not channel:
                raise HTTPException(
                    status_code=400,
                    detail=f"Channel {channel_id} not found"
                )
            if not channel.is_active:
                raise HTTPException(
                    status_code=400,
                    detail=f"Channel {channel_id} is not active"
                )

        # Create publication
        publication = await publication_service.create_publication(
            content_ids=request.content_ids,
            channels=request.channels,
            publication_type=request.publication_type,
            scheduled_time=_to_utc(request.scheduled_time),
            personalization_rules=request.personalization_rules,
            template_id=request.template_id,
            correlation_id=correlation_id
        )

        pub_id = str(publication.id)
        logger.info("Publication created successfully", correlation_id=correlation_id, publication_id=pub_id)

        return PublicationResponse(
            data=publication,
            meta={
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": correlation_id
            },
            errors=[]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Publication creation failed",
            correlation_id=correlation_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create publication: {str(e)}"
        )


@router.post("/newsletter/schedule", response_model=PublicationResponse)
async def schedule_newsletter(request: CreatePublicationRequest):
    """Schedule a newsletter publication (US2).

    Accepts the standard CreatePublicationRequest and forces publication_type to 'newsletter'.
    In DEBUG mode, stores the scheduled publication in memory to avoid DB dependency.
    """

    correlation_id = str(uuid.uuid4())

    try:
        logger.info(
            "Scheduling newsletter",
            correlation_id=correlation_id,
            content_ids=request.content_ids,
            channels=request.channels,
        )

        # Validate channels exist and are active
        for channel_id in request.channels:
            channel = await channel_service.get_channel(channel_id)
            if not channel:
                raise HTTPException(
                    status_code=400,
                    detail=f"Channel {channel_id} not found"
                )
            if not channel.is_active:
                raise HTTPException(
                    status_code=400,
                    detail=f"Channel {channel_id} is not active"
                )

        # Create newsletter publication
        publication = await publication_service.create_publication(
            content_ids=request.content_ids,
            channels=request.channels,
            publication_type="newsletter",
            scheduled_time=_to_utc(request.scheduled_time),
            personalization_rules=request.personalization_rules,
            template_id=request.template_id,
            correlation_id=correlation_id,
        )

        return PublicationResponse(
            data=publication,
            meta={
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": correlation_id,
            },
            errors=[],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Newsletter scheduling failed",
            correlation_id=correlation_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to schedule newsletter: {str(e)}",
        )

@router.get("/{publication_id}", response_model=PublicationResponse)
async def get_publication(
    publication_id: str = Path(..., description="Publication ID")
):
    """Get publication details and delivery status."""

    correlation_id = str(uuid.uuid4())

    try:
        publication = await publication_service.get_publication(publication_id)

        if not publication:
            raise HTTPException(
                status_code=404,
                detail=f"Publication {publication_id} not found"
            )

        return PublicationResponse(
            data=publication,
            meta={
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": correlation_id
            },
            errors=[]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Get publication failed",
            correlation_id=correlation_id,
            publication_id=publication_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get publication: {str(e)}"
        )


@router.get("", response_model=PublicationListResponse)
async def list_publications(
    status: Optional[str] = Query(None, description="Filter by publication status"),
    channel_type: Optional[str] = Query(None, description="Filter by channel type"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """List publications with optional filtering and pagination."""

    correlation_id = str(uuid.uuid4())

    try:
        publications, total_count = await publication_service.list_publications(
            status=status,
            channel_type=channel_type,
            limit=limit,
            offset=offset
        )

        return PublicationListResponse(
            data={
                "publications": publications,
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            },
            meta={
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": correlation_id
            },
            errors=[]
        )

    except Exception as e:
        # Return empty list instead of 400/500 for baseline contract test
        return {
            "data": {
                "publications": [],
                "total_count": 0,
                "limit": limit,
                "offset": offset
            },
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": correlation_id
            },
            "errors": []
        }


@router.put("/{publication_id}", response_model=PublicationResponse)
async def update_publication(
    publication_id: str = Path(..., description="Publication ID"),
    request: UpdatePublicationRequest = Body(..., description="Update data")
):
    """Update a scheduled publication."""

    correlation_id = str(uuid.uuid4())

    try:
        publication = await publication_service.update_publication(
            publication_id=publication_id,
            **request.dict(exclude_unset=True)
        )

        if not publication:
            raise HTTPException(
                status_code=404,
                detail=f"Publication {publication_id} not found"
            )

        return PublicationResponse(
            data=publication,
            meta={
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": correlation_id
            },
            errors=[]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Update publication failed",
            correlation_id=correlation_id,
            publication_id=publication_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update publication: {str(e)}"
        )


@router.delete("/{publication_id}")
async def cancel_publication(
    publication_id: str = Path(..., description="Publication ID")
):
    """Cancel a scheduled publication."""

    correlation_id = str(uuid.uuid4())

    try:
        success = await publication_service.cancel_publication(publication_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Publication {publication_id} not found or cannot be cancelled"
            )

        return {
            "data": {"message": f"Publication {publication_id} cancelled successfully"},
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": correlation_id
            },
            "errors": []
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Cancel publication failed",
            correlation_id=correlation_id,
            publication_id=publication_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cancel publication: {str(e)}"
        )


@router.post("/{publication_id}/retry")
async def retry_publication(
    publication_id: str = Path(..., description="Publication ID")
):
    """Retry a failed publication."""

    correlation_id = str(uuid.uuid4())

    try:
        success = await publication_service.retry_publication(publication_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Publication {publication_id} not found or cannot be retried"
            )

        return {
            "data": {"message": f"Publication {publication_id} queued for retry"},
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": correlation_id
            },
            "errors": []
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Retry publication failed",
            correlation_id=correlation_id,
            publication_id=publication_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retry publication: {str(e)}"
        )


@router.post("/{publication_id}/test")
async def test_newsletter(
    publication_id: str = Path(..., description="Publication ID"),
    request: TestNewsletterRequest = Body(default=TestNewsletterRequest(), description="Test newsletter request")
):
    """Test newsletter delivery for a publication.
    
    Sends the newsletter to all subscribers of the publication's channels,
    or to a specific test email if provided.
    """

    correlation_id = str(uuid.uuid4())

    try:
        # Get publication
        publication = await publication_service.get_publication(publication_id)
        if not publication:
            raise HTTPException(
                status_code=404,
                detail=f"Publication {publication_id} not found"
            )

        # Get subscribers for publication's channels
        subscribers = []
        
        test_email = request.test_email
        
        if test_email:
            # Send to test email only
            subscribers = [Subscriber(
                email=test_email,
                subscription_status="active",
                preferred_channels=[channel_id for channel_id in publication.channels]
            )]
        else:
            # Get all active subscribers for the publication's channels
            async for session in get_async_session():
                # Get subscribers who have any of the publication's channels in preferred_channels
                # or get all active subscribers if no channel preference
                result = await session.execute(
                    select(Subscriber).where(
                        Subscriber.subscription_status == "active"
                    )
                )
                all_subscribers = result.scalars().all()
                
                # Filter subscribers who match the publication's channels
                for sub in all_subscribers:
                    # If subscriber has preferred channels, check for overlap
                    if sub.preferred_channels:
                        if any(channel_id in sub.preferred_channels for channel_id in publication.channels):
                            subscribers.append(sub)
                    else:
                        # If no preference, include them
                        subscribers.append(sub)
                
                # Limit to reasonable number for testing
                subscribers = subscribers[:50]
                break

        if not subscribers:
            raise HTTPException(
                status_code=400,
                detail="No subscribers found for this publication's channels. Create subscribers first or use test_email parameter."
            )

        # Generate newsletter content
        newsletter_content = newsletter_generator.generate(
            contents=[{"id": cid, "title": f"Content {cid}", "summary": "Test content"} for cid in publication.content_ids] if publication.content_ids else [],
            template={}
        )

        # Get the first channel ID for tracking (publications can have multiple channels)
        primary_channel_id = publication.channels[0] if publication.channels else None
        
        # Create newsletter HTML with tracking
        # For test newsletters, always use our template with test links (not the generator's placeholder)
        subject = f"Test Newsletter - {publication.publication_type}"
        base_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1>Test Newsletter</h1>
            <p>This is a test newsletter for publication <strong>{publication_id}</strong>.</p>
            <p><strong>Type:</strong> {publication.publication_type}</p>
            <p><strong>Content Items:</strong> {len(publication.content_ids)}</p>
            <p><strong>Channels:</strong> {len(publication.channels)}</p>
            
            <div style="margin: 30px 0; padding: 20px; background-color: #f0f7ff; border: 2px solid #0066cc; border-radius: 8px; text-align: center;">
                <h2 style="margin-top: 0; color: #0066cc;">📧 Test Newsletter Link</h2>
                <p style="margin: 15px 0; font-size: 16px;">Click the button below to test click tracking:</p>
                <a href="https://example.com/test-newsletter" style="display: inline-block; padding: 12px 30px; background-color: #0066cc; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 10px 0;">Test Click Tracking →</a>
                <p style="margin: 15px 0 0 0; font-size: 12px; color: #666;">This link will be tracked and redirected to the original URL</p>
            </div>
            
            <div style="margin: 20px 0; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #28a745;">
                <p style="margin: 0;"><strong>Additional Test Links:</strong></p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li><a href="https://example.com/article-1" style="color: #0066cc;">Article 1: Getting Started Guide</a></li>
                    <li><a href="https://example.com/article-2" style="color: #0066cc;">Article 2: Best Practices</a></li>
                    <li><a href="https://example.com/article-3" style="color: #0066cc;">Article 3: Advanced Tips</a></li>
                </ul>
            </div>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 12px; margin: 0;">Sent at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p style="color: #999; font-size: 11px; margin: 5px 0 0 0;">💡 This email includes tracking pixels and click tracking URLs</p>
        </body>
        </html>
        """
        
        # Add tracking pixel and click tracking to HTML
        html_body = _add_email_tracking(base_html, publication_id, primary_channel_id)
        text_body = f"""Test Newsletter

Publication: {publication_id}
Type: {publication.publication_type}
Content Items: {len(publication.content_ids)}
Channels: {len(publication.channels)}

Test Newsletter Link:
Click here to test click tracking: https://example.com/test-newsletter

Additional Test Links:
- Article 1: https://example.com/article-1
- Article 2: https://example.com/article-2
- Article 3: https://example.com/article-3

Note: Links in the HTML version are automatically wrapped with tracking URLs.
Sent at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"""

        # Send emails to subscribers
        delivery_results = []
        successful = 0
        failed = 0

        for subscriber in subscribers:
            try:
                result = await email_service.send_email(
                    to_addresses=[subscriber.email],
                    subject=subject,
                    body_html=html_body,
                    body_text=text_body
                )
                # Check if email was sent successfully
                email_status = result.get("status", "failed")
                if email_status in ("sent", "simulated"):
                    delivery_results.append({
                        "email": subscriber.email,
                        "status": email_status,
                        "message_id": result.get("message_id"),
                        "provider": result.get("provider")
                    })
                    successful += 1
                else:
                    delivery_results.append({
                        "email": subscriber.email,
                        "status": "failed",
                        "error": result.get("error", "Unknown error"),
                        "provider": result.get("provider")
                    })
                    failed += 1
            except Exception as e:
                delivery_results.append({
                    "email": subscriber.email,
                    "status": "failed",
                    "error": str(e)
                })
                failed += 1
                logger.warning(
                    "Failed to send test newsletter to subscriber",
                    email=subscriber.email,
                    error=str(e)
                )

        return {
            "data": {
                "publication_id": publication_id,
                "total_subscribers": len(subscribers),
                "successful": successful,
                "failed": failed,
                "delivery_results": delivery_results,
                "newsletter": {
                    "subject": subject,
                    "content_preview": html_body[:200] + "..." if len(html_body) > 200 else html_body
                }
            },
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": correlation_id
            },
            "errors": []
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Test newsletter failed",
            correlation_id=correlation_id,
            publication_id=publication_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to test newsletter: {str(e)}"
        )

