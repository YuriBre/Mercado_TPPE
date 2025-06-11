from fastapi import APIRouter
from app.controllers.produto_controller import router as produto_router

router = APIRouter()
router.include_router(produto_router, prefix="/produtos", tags=["Produtos"])