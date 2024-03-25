from fastapi import APIRouter, UploadFile

from app.main.factories import make_process_billing_file_use_case


router = APIRouter()


@router.post('/billing-file')
async def process_billing_file_route(file: UploadFile):
    response = await make_process_billing_file_use_case().execute(file.file)

    return response
