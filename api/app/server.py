import sys, os
sys.path.append(os.path.abspath(os.path.dirname("packages"))) # import package
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from packages.rag import chain

app = FastAPI(
    title="MakariosAI"
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.get("/home")
async def root():
    return {'info' : 'MakariosAI'}

# Edit this to add the chain you want to add
add_routes(app, chain, path="/ask")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8000)