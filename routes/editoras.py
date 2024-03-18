from fastapi import APIRouter, HTTPException
from .utils import carregar_dados, salvar_dados
from pydantic import BaseModel

router = APIRouter()

class Editora(BaseModel):
    nome: str
    endereco: str

@router.get("/")
def listar_editoras():
    editoras = carregar_dados("editoras.json")
    return {"editoras": editoras}

@router.get("/{editora_id}")
def buscar_editora_por_id(editora_id: int):
    editoras = carregar_dados("editoras.json")
    for editora in editoras:
        if editora["editora_id"] == editora_id:
            return editora
    raise HTTPException(status_code=404, detail="Editora não encontrada")

@router.delete("/{editora_id}")
def excluir_editora(editora_id: int):
    editoras = carregar_dados("editoras.json")
    editora_encontrada = None
    for editora in editoras:
        if editora["editora_id"] == editora_id:
            editora_encontrada = editora
            break

    if editora_encontrada:
        editoras.remove(editora_encontrada)
        salvar_dados("editoras.json", editoras)
        return {"mensagem": "Editora excluída com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Editora não encontrada")

@router.post("/")
def adicionar_editora(editora: Editora):
    editoras = carregar_dados("editoras.json")
    novo_id = max(editora["editora_id"] for editora in editoras) + 1 if editoras else 1
    nova_editora = {
        "editora_id": novo_id,
        "nome": editora.nome,
        "endereco": editora.endereco
    }
    editoras.append(nova_editora)
    salvar_dados("editoras.json", editoras)
    return nova_editora
