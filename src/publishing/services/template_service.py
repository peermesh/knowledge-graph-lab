from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime
from sqlalchemy import select

from ..core.config import settings
from ..core.database import get_async_session
from ..models.template import Template
from ..clients.redis_client import RedisClient


class TemplateService:
    def __init__(self):
        self.redis_client = RedisClient()

    async def create_template(self, name: str, template_type: str, content_structure: Dict[str, Any]) -> Dict[str, Any]:
        async for session in get_async_session():
            now = datetime.utcnow()
            template = Template(
                name=name,
                template_type=template_type,
                content_structure=content_structure,
                formatting_rules={},
                branding_elements={},
                variable_definitions={},
                usage_count=0,
                is_active=True,
            )
            session.add(template)
            await session.commit()
            await session.refresh(template)
            
            t = {
                "id": str(template.id),
                "name": template.name,
                "template_type": template.template_type,
                "content_structure": template.content_structure,
                "formatting_rules": template.formatting_rules,
                "branding_elements": template.branding_elements,
                "variable_definitions": template.variable_definitions,
                "usage_count": template.usage_count,
                "is_active": template.is_active,
                "created_at": template.created_at,
                "updated_at": template.updated_at,
            }
            
            # Cache in Redis
            await self.redis_client.set_json(f"template:{template.id}", t, ttl=3600)
            
            return t

    async def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        # Try Redis cache first
        cached = await self.redis_client.get_json(f"template:{template_id}")
        if cached:
            return cached
        
        # Fall back to database
        async for session in get_async_session():
            result = await session.execute(
                select(Template).where(Template.id == template_id)
            )
            template = result.scalar_one_or_none()
            
            if template:
                t = {
                    "id": str(template.id),
                    "name": template.name,
                    "template_type": template.template_type,
                    "content_structure": template.content_structure,
                    "formatting_rules": template.formatting_rules,
                    "branding_elements": template.branding_elements,
                    "variable_definitions": template.variable_definitions,
                    "usage_count": template.usage_count,
                    "is_active": template.is_active,
                    "created_at": template.created_at,
                    "updated_at": template.updated_at,
                }
                # Cache for next time
                await self.redis_client.set_json(f"template:{template_id}", t, ttl=3600)
                return t
            
            return None

    async def list_templates(self) -> List[Dict[str, Any]]:
        async for session in get_async_session():
            result = await session.execute(select(Template))
            templates = result.scalars().all()
            
            return [
                {
                    "id": str(t.id),
                    "name": t.name,
                    "template_type": t.template_type,
                    "content_structure": t.content_structure,
                    "formatting_rules": t.formatting_rules,
                    "branding_elements": t.branding_elements,
                    "variable_definitions": t.variable_definitions,
                    "usage_count": t.usage_count,
                    "is_active": t.is_active,
                    "created_at": t.created_at,
                    "updated_at": t.updated_at,
                }
                for t in templates
            ]

    def render(self, template: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, str]:
        # Minimal render: return simple merged strings
        title = context.get("title", "Newsletter")
        body = context.get("body", "")
        html = f"<html><body><h1>{title}</h1><div>{body}</div></body></html>"
        text = f"{title}\n\n{body}"
        return {"html": html, "text": text}

