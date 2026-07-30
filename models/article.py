from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Article:
    id: str
    title: str
    slug: str

    url: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

    display_date: Optional[str] = None
    published_at: Optional[str] = None

    author: Optional[str] = None
    category: Optional[str] = None

    body: Optional[str] = None

    tags: list[str] = field(default_factory=list)
