import io
import json
from fastapi import Response
from zipfile import ZipFile


def generate_zip_and_response(buffer, remaining_contact_members):
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        # Добавляем XLSX файл
        xlsx_data = buffer.getvalue()
        zip_file.writestr("Companies_contacts_members.xlsx", xlsx_data)

        # Добавляем JSON файл
        if remaining_contact_members:
            json_data = json.dumps([member.model_dump() for member in remaining_contact_members])
            zip_file.writestr("remaining_contact_members.json", json_data)

    return Response(
        zip_buffer.getvalue(),
        media_type='application/zip',
        headers={"Content-Disposition": "attachment;filename=Companies_contacts_members.zip"}
    )