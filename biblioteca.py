from fastapi import FastAPI
from routes import livros, autores, emprestimos, editoras, membros  

app = FastAPI()

app.include_router(autores.router, prefix="/autores", tags=["Autores"])
app.include_router(editoras.router, prefix="/editoras", tags=["Editoras"])
app.include_router(emprestimos.router, prefix="/emprestimos", tags=["Emprestimos"])
app.include_router(livros.router, prefix="/livros", tags=["Livros"])
app.include_router(membros.router, prefix="/membros", tags=["Membros"])
