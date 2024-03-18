from fastapi import APIRouter, HTTPException
from .utils import carregar_dados, salvar_dados
from pydantic import BaseModel

router = APIRouter()

class Membro(BaseModel):
    nome: str
    email: str

@router.get("/")
def listar_membros():
    membros = carregar_dados("membros.json")
    return {"membros": membros}

@router.get("/{membro_id}")
def buscar_membro_por_id(membro_id: int):
    membros = carregar_dados("membros.json")
    for membro in membros:
        if membro["membro_id"] == membro_id:
            return membro
    raise HTTPException(status_code=404, detail="Membro não encontrado")

@router.delete("/{membro_id}")
def excluir_membro(membro_id: int):
    membros = carregar_dados("membros.json")
    membro_encontrado = None
    for membro in membros:
        if membro["membro_id"] == membro_id:
            membro_encontrado = membro
            break

    if membro_encontrado:
        membros.remove(membro_encontrado)
        salvar_dados("membros.json", membros)
        return {"mensagem": "Membro excluído com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Membro não encontrado")

@router.post("/")
def adicionar_membro(membro: Membro):
    membros = carregar_dados("membros.json")
    novo_id = max(membro["membro_id"] for membro in membros) + 1 if membros else 1
    novo_membro = {
        "membro_id": novo_id,
        "nome": membro.nome,
        "email": membro.email
    }
    membros.append(novo_membro)
    salvar_dados("membros.json", membros)
    return novo_membro
