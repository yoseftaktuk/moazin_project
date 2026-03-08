from fastapi import FastAPI
import uvicorn
from route import route
app = FastAPI()
app.include_router(route)

if __name__ == "__main__":
    uvicorn.run(app , host='localhost', port=8000)