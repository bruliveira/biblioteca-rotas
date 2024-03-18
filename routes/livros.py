from fastapi import APIRouter, HTTPException
from .utils import carregar_dados, salvar_dados  
from pydantic import BaseModel

router = APIRouter()

class Livro(BaseModel):
    titulo: str
    autor: str
    editora: str

@router.get("/")
def listar_livros():
    livros = carregar_dados("livros.json")
    return {"livros": livros}

@router.get("/")
def listar_livros():
    livros = carregar_dados("livros.json")
    return {"livros": livros}

@router.get("/{livro_id}")
def buscar_livro_por_id(livro_id: int):
    livros = carregar_dados("livros.json")
    for livro in livros:
        if livro["livro_id"] == livro_id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@router.delete("/{livro_id}")
def excluir_livro(livro_id: int):
    livros = carregar_dados("livros.json")
    livro_encontrado = None
    for livro in livros:
        if livro["livro_id"] == livro_id:
            livro_encontrado = livro
            break

    if livro_encontrado:
        livros.remove(livro_encontrado)
        salvar_dados("livros.json", livros)
        return {"mensagem": "Livro excluído com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

@router.post("/")
def adicionar_livro(livro: Livro):
    livros = carregar_dados("livros.json")

    # Gera um novo ID para o livro
    novo_id = max(livro["livro_id"] for livro in livros) + 1 if livros else 1

    novo_livro = {
        "livro_id": novo_id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "editora": livro.editora
    }

    livros.append(novo_livro)
    salvar_dados("livros.json", livros)

    return novo_livro

@router.put("/{livro_id}")
def atualizar_livro(livro_id: int, livro: Livro):
    livros = carregar_dados("livros.json")
    for index, livro_existente in enumerate(livros):
        if livro_existente["livro_id"] == livro_id:
            livros[index] = {
                "livro_id": livro_id,
                "titulo": livro.titulo,
                "autor": livro.autor,
                "editora": livro.editora
            }
            salvar_dados("livros.json", livros)
            return {"mensagem": "Livro atualizado com sucesso"}
    raise HTTPException(status_code=404, detail="Livro não encontrado")
