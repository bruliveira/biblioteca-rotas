from fastapi import APIRouter, HTTPException
from .utils import carregar_dados, salvar_dados
from pydantic import BaseModel

router = APIRouter()

class Emprestimo(BaseModel):
    livro_id: int
    membro_id: int
    data_emprestimo: str
    data_devolucao: str

@router.get("/")
def listar_emprestimos():
    emprestimos = carregar_dados("emprestimos.json")
    return {"emprestimos": emprestimos}

@router.get("/{emprestimo_id}")
def buscar_emprestimo_por_id(emprestimo_id: int):
    emprestimos = carregar_dados("emprestimos.json")
    for emprestimo in emprestimos:
        if emprestimo["emprestimo_id"] == emprestimo_id:
            return emprestimo
    raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

@router.delete("/{emprestimo_id}")
def excluir_emprestimo(emprestimo_id: int):
    emprestimos = carregar_dados("emprestimos.json")
    emprestimo_encontrado = None
    for emprestimo in emprestimos:
        if emprestimo["emprestimo_id"] == emprestimo_id:
            emprestimo_encontrado = emprestimo
            break

    if emprestimo_encontrado:
        emprestimos.remove(emprestimo_encontrado)
        salvar_dados("emprestimos.json", emprestimos)
        return {"mensagem": "Empréstimo excluído com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

@router.post("/")
def adicionar_emprestimo(emprestimo: Emprestimo):
    emprestimos = carregar_dados("emprestimos.json")
    novo_id = max(emprestimo["emprestimo_id"] for emprestimo in emprestimos) + 1 if emprestimos else 1
    novo_emprestimo = {
        "emprestimo_id": novo_id,
        "livro_id": emprestimo.livro_id,
        "membro_id": emprestimo.membro_id,
        "data_emprestimo": emprestimo.data_emprestimo,
        "data_devolucao": emprestimo.data_devolucao
    }
    emprestimos.append(novo_emprestimo)
    salvar_dados("emprestimos.json", emprestimos)
    return novo_emprestimo
