from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Import routers
from src.routers import auth, books, borrow, search, sort, recommendations, requests, admin

app = FastAPI(
    title="BookOps API",
    description="A comprehensive book management system API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(borrow.router, prefix="/borrow", tags=["Borrowing"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(sort.router, prefix="/sort", tags=["Sorting"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(requests.router, prefix="/requests", tags=["Customer Requests"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to BookOps API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "BookOps API is running"}