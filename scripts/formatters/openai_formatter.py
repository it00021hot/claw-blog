"""
OpenAI formatter for generating Hugo Front Matter.
"""
import json
import logging
import re
import uuid
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timezone

from openai import OpenAI

from scripts.config import config

logger = logging.getLogger(__name__)

# Valid categories
VALID_CATEGORIES = ["安装", "进阶", "常见问题", "教程", "源码解析"]


class OpenAIFormatter:
    """Format articles using OpenAI API."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, api_base: Optional[str] = None):
        self.api_key = api_key or config.openai_api_key
        self.model = model or config.openai_model
        self.api_base = api_base or config.openai_api_base
        self.client = None
        if self.api_key:
            client_kwargs = {"api_key": self.api_key}
            if self.api_base:
                client_kwargs["base_url"] = self.api_base
            self.client = OpenAI(**client_kwargs)

    def format_article(self, article) -> Dict[str, any]:
        """Generate front matter using OpenAI."""
        if not self.client:
            logger.warning("OpenAI client not initialized, returning default front matter")
            return self._default_front_matter(article)

        # Truncate content to avoid exceeding token limits
        content_preview = article.content[:2000]

        prompt = f"""分析以下文章内容，生成 Hugo 文章的 Front Matter。

文章信息：
- 标题: {article.title}
- 来源: {article.source}
- URL: {article.url}

文章内容（前2000字）:
{content_preview}

请生成 JSON 格式的 Front Matter，包含以下字段：
- title: 文章标题
- date: 发布日期（格式: YYYY-MM-DD，使用今天日期 {datetime.now(timezone.utc).strftime('%Y-%m-%d')}）
- categories: 分类数组，必须为以下之一: {', '.join(VALID_CATEGORIES)}，选择最合适的
- tags: 标签数组，根据文章内容生成3-5个标签
- description: 文章描述，50-100字
- keywords: 关键词数组

请只返回 JSON，不要其他内容。"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个博客内容分析助手，擅长为技术文章生成合适的元数据。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500,
            )

            content = response.choices[0].message.content
            # Parse JSON from response
            front_matter = json.loads(content)
            return front_matter

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from OpenAI: {e}")
            return self._default_front_matter(article)
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return self._default_front_matter(article)

    def _default_front_matter(self, article) -> Dict[str, any]:
        """Generate default front matter."""
        return {
            "title": article.title,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "categories": ["教程"],
            "tags": [article.source],
            "description": article.content[:100] if article.content else "",
            "keywords": [article.source],
        }


def save_as_hugo_markdown(article, front_matter: Dict, output_dir: str) -> str:
    """Save article as Hugo Markdown file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate slug
    title = front_matter.get("title", article.title)
    slug = generate_slug(title)

    # Ensure unique filename
    filename = f"{slug}.md"
    file_path = output_path / filename

    # Handle duplicate filenames
    counter = 1
    while file_path.exists():
        filename = f"{slug}-{counter}.md"
        file_path = output_path / filename
        counter += 1

    # Build YAML front matter
    yaml_lines = ["---"]
    for key, value in front_matter.items():
        if isinstance(value, list):
            yaml_lines.append(f"{key}:")
            for item in value:
                yaml_lines.append(f"  - {item}")
        else:
            yaml_lines.append(f"{key}: {value}")
    yaml_lines.append("---\n")

    # Write file
    content = "\n".join(yaml_lines) + article.content
    file_path.write_text(content, encoding="utf-8")

    logger.info(f"Saved article to {file_path}")
    return str(file_path)


def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title."""
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower()
    # Replace Chinese characters with a hash (since we can't slugify Chinese)
    if re.search(r'[\u4e00-\u9fff]', slug):
        # If contains Chinese, add a hash prefix
        chinese_hash = str(uuid.uuid4())[:8]
        slug = re.sub(r'[\u4e00-\u9fff]+', '', slug)  # Remove Chinese
        slug = f"{chinese_hash}-{slug}" if slug.strip() else chinese_hash
    # Replace non-alphanumeric (except Chinese) with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug[:50]  # Limit length
