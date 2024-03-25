from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.main.routes import billing_router


billing_system_api_router = APIRouter(prefix='/api')
billing_system_api_router.include_router(billing_router)

origins = ['http://localhost:8888']

app = FastAPI(title='Billing System API', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(billing_system_api_router)
