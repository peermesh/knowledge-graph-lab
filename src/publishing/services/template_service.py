from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime

from ..core.config import settings
from ..state import IN_MEMORY_TEMPLATES


class TemplateService:
    def create_template(self, name: str, template_type: str, content_structure: Dict[str, Any]) -> Dict[str, Any]:
        if settings.DEBUG:
            now = datetime.utcnow()
            t = {
                "id": str(uuid.uuid4()),
                "name": name,
                "template_type": template_type,
                "content_structure": content_structure,
                "formatting_rules": {},
                "branding_elements": {},
                "variable_definitions": {},
                "usage_count": 0,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            }
            IN_MEMORY_TEMPLATES.append(t)
            return t
        raise NotImplementedError

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        if settings.DEBUG:
            return next((t for t in IN_MEMORY_TEMPLATES if t["id"] == template_id), None)
        raise NotImplementedError

    def list_templates(self) -> List[Dict[str, Any]]:
        if settings.DEBUG:
            return list(IN_MEMORY_TEMPLATES)
        raise NotImplementedError

    def render(self, template: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, str]:
        # Minimal render: return simple merged strings
        title = context.get("title", "Newsletter")
        body = context.get("body", "")
        html = f"<html><body><h1>{title}</h1><div>{body}</div></body></html>"
        text = f"{title}\n\n{body}"
        return {"html": html, "text": text}

