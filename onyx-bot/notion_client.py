import requests
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DB_POSTS = "32e6e736-4ef7-81d3-8666-c3c54b5ba19e"
DB_SUBSTACK = "32e6e736-4ef7-8118-a183-cc34da56f593"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def save_linkedin_post(title: str, content: str, hook: str = "", cta: str = "") -> str:
    """Save a LinkedIn post to Notion and return the page URL."""
    payload = {
        "parent": {"database_id": DB_POSTS},
        "properties": {
            "Título": {"title": [{"text": {"content": title}}]},
            "Estado": {"select": {"name": "Listo"}},
            "Hook": {"rich_text": [{"text": {"content": hook[:2000] if hook else ""}}]},
            "CTA": {"rich_text": [{"text": {"content": cta[:2000] if cta else ""}}]},
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": content[:2000]}}]}
            }
        ]
    }
    resp = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if resp.status_code == 200:
        page = resp.json()
        return page.get("url", "✅ Guardado en Notion")
    return f"❌ Error Notion: {resp.status_code}"


def save_substack_article(title: str, content: str, resumen: str = "") -> str:
    """Save a Substack article to Notion and return the page URL."""
    payload = {
        "parent": {"database_id": DB_SUBSTACK},
        "properties": {
            "Título": {"title": [{"text": {"content": title}}]},
            "Estado": {"select": {"name": "Listo"}},
            "Resumen": {"rich_text": [{"text": {"content": resumen[:2000] if resumen else ""}}]},
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": content[:2000]}}]}
            }
        ]
    }
    resp = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if resp.status_code == 200:
        page = resp.json()
        return page.get("url", "✅ Guardado en Notion")
    return f"❌ Error Notion: {resp.status_code}"
