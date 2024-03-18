from fastapi import APIRouter, HTTPException
from .utils import carregar_dados, salvar_dados
from pydantic import BaseModel

router = APIRouter()

class Autor(BaseModel):
    nome: str
    nacionalidade: str

@router.get("/")
def listar_autores():
    autores = carregar_dados("autores.json")
    return {"autores": autores}

@router.get("/{autor_id}")
def buscar_autor_por_id(autor_id: int):
    autores = carregar_dados("autores.json")
    for autor in autores:
        if autor["autor_id"] == autor_id:
            return autor
    raise HTTPException(status_code=404, detail="Autor não encontrado")

@router.delete("/{autor_id}")
def excluir_autor(autor_id: int):
    autores = carregar_dados("autores.json")
    autor_encontrado = None
    for autor in autores:
        if autor["autor_id"] == autor_id:
            autor_encontrado = autor
            break

    if autor_encontrado:
        autores.remove(autor_encontrado)
        salvar_dados("autores.json", autores)
        return {"mensagem": "Autor excluído com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

@router.post("/")
def adicionar_autor(autor: Autor):
    autores = carregar_dados("autores.json")
    novo_id = max(autor["autor_id"] for autor in autores) + 1 if autores else 1
    novo_autor = {
        "autor_id": novo_id,
        "nome": autor.nome,
        "nacionalidade": autor.nacionalidade
    }
    autores.append(novo_autor)
    salvar_dados("autores.json", autores)
    return novo_autor
