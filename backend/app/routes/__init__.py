from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.leads import router as leads_router
from app.routes.placeholders import register_placeholder
from app.routes.reports import router as reports_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(leads_router)
api_router.include_router(reports_router)

for prefix in ['/users', '/deals', '/followups', '/products', '/quotations', '/orders', '/payments', '/visits']:
    api_router.include_router(register_placeholder(prefix))
