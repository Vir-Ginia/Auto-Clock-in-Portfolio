from fastapi import FastAPI
from .database import Base, engine
from .api_routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from .admin_routes import router as admin_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automatic Attendance System")

# Create tables on startup (move inside event to avoid import issues)
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automatic Attendance System")

# CORS middleware—allows Flutter app to hit from emulator/phone
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")  # Ensures /api/sync/buildings works
app.include_router(admin_router)  # For /buildings HTML

# Root test endpoint
@app.get("/")
def root():
    return {"message": "Attendance API ready! Try /api/sync/buildings"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)