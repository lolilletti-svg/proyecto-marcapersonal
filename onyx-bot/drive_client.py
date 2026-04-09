"""
Google Drive client — guarda drafts aprobados en /Onyx/LinkedIn/ o /Onyx/Substack/

Setup (una vez):
1. Ir a console.cloud.google.com
2. Crear proyecto → activar Google Drive API
3. Crear Service Account → bajar JSON de credenciales
4. Guardar el JSON como GOOGLE_CREDENTIALS_JSON en las env vars de Railway
5. Crear carpeta "Onyx" en Drive → compartirla con el email de la service account
"""

import os
import json
import io
from datetime import datetime

# Solo se importa si las credenciales están disponibles
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
    from google.oauth2.service_account import Credentials
    DRIVE_AVAILABLE = True
except ImportError:
    DRIVE_AVAILABLE = False


def _get_service():
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
        return None
    creds_data = json.loads(creds_json)
    creds = Credentials.from_service_account_info(
        creds_data,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)


def _get_or_create_folder(service, name: str, parent_id: str = None) -> str:
    """Get folder ID by name, create if doesn't exist."""
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    # Create
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def save_to_drive(content: str, title: str, content_type: str = "linkedin") -> str:
    """
    Save content to Drive.
    content_type: "linkedin" or "substack"
    Returns: file URL or error message
    """
    if not DRIVE_AVAILABLE:
        return "⚠️ Google Drive no configurado aún (falta instalar google-api-python-client)"

    service = _get_service()
    if not service:
        return "⚠️ Google Drive: falta GOOGLE_CREDENTIALS_JSON en env vars"

    try:
        # Get/create folder structure: Onyx/LinkedIn/ or Onyx/Substack/
        onyx_folder_id = _get_or_create_folder(service, "Onyx")
        subfolder_name = "LinkedIn" if content_type == "linkedin" else "Substack"
        subfolder_id = _get_or_create_folder(service, subfolder_name, onyx_folder_id)

        # Create filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = title.lower()[:40].replace(" ", "-").replace("/", "-")
        filename = f"{content_type}-{date_str}-{slug}.md"

        # Upload
        file_content = f"# {title}\n\n*{datetime.now().strftime('%d/%m/%Y')}*\n\n---\n\n{content}"
        media = MediaIoBaseUpload(
            io.BytesIO(file_content.encode("utf-8")),
            mimetype="text/plain"
        )
        file_metadata = {"name": filename, "parents": [subfolder_id]}
        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink"
        ).execute()

        return uploaded.get("webViewLink", "✅ Guardado en Drive")

    except Exception as e:
        return f"❌ Error Drive: {str(e)[:100]}"
