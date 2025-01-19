from fastapi import FastAPI
from app.api.routers.auth import router as auth_router
from app.api.routers.user import router as user_router
from app.api.routers.books import router as books_router
from app.api.routers.loans import router as loans_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gerenciamento de Livros do sexo")

app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(user_router, prefix="/api/v1/users")
app.include_router(books_router, prefix="/api/v1/books")
app.include_router(loans_router, prefix="/api/v1/loans")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "sexo"}


