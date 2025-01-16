from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Inicializando a aplicação FastAPI
app = FastAPI()

# --- Estruturas de dados ---
class Vacina(BaseModel):
    nome: str
    fabricante: str
    validade: date
    quantidade: int
    intervalo: str
    doses: int

class Usuario(BaseModel):
    nome: str
    cpf: str
    rua: str
    numero: int
    bairro: str
    cep: str
    estado: str
    uf: str

class Agendamento(BaseModel):
    data: date
    hora: str
    vacina: str
    usuario_cpf: str

# Bases de dados em memória
vacinas: List[Vacina] = []
usuarios: List[Usuario] = []
agendamentos: List[Agendamento] = []

# --- Endpoints Vacinas ---
@app.post("/vacinas", response_model=Vacina)
def criar_vacina(vacina: Vacina):
    if any(v.nome == vacina.nome for v in vacinas):
        raise HTTPException(status_code=400, detail="Vacina já cadastrada.")
    vacinas.append(vacina)
    return vacina

@app.get("/vacinas", response_model=List[Vacina])
def listar_vacinas():
    return vacinas

@app.put("/vacinas/{nome}")
def alterar_vacina(nome: str, vacina: Vacina):
    for i, v in enumerate(vacinas):
        if v.nome == nome:
            vacinas[i] = vacina
            return vacina
    raise HTTPException(status_code=404, detail="Vacina não encontrada.")

@app.delete("/vacinas/{nome}")
def excluir_vacina(nome: str):
    global vacinas
    vacinas = [v for v in vacinas if v.nome != nome]
    return {"message": f"Vacina {nome} excluída com sucesso."}

# --- Endpoints Usuários ---
@app.post("/usuarios", response_model=Usuario)
def criar_usuario(usuario: Usuario):
    if any(u.cpf == usuario.cpf for u in usuarios):
        raise HTTPException(status_code=400, detail="Usuário já cadastrado.")
    usuarios.append(usuario)
    return usuario

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    return usuarios

@app.put("/usuarios/{cpf}")
def alterar_usuario(cpf: str, usuario: Usuario):
    for i, u in enumerate(usuarios):
        if u.cpf == cpf:
            usuarios[i] = usuario
            return usuario
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

@app.delete("/usuarios/{cpf}")
def excluir_usuario(cpf: str):
    global usuarios
    usuarios = [u for u in usuarios if u.cpf != cpf]
    return {"message": f"Usuário com CPF {cpf} excluído com sucesso."}

# --- Endpoints Agendamentos ---
@app.post("/agendamentos", response_model=Agendamento)
def criar_agendamento(agendamento: Agendamento):
    if any(
        a.usuario_cpf == agendamento.usuario_cpf and 
        a.data == agendamento.data and 
        a.hora == agendamento.hora for a in agendamentos):
        raise HTTPException(
            status_code=400,
            detail="Agendamento já cadastrado para este usuário, data e hora."
        )
    agendamentos.append(agendamento)
    return agendamento

@app.get("/agendamentos", response_model=List[Agendamento])
def listar_agendamentos():
    return agendamentos

@app.put("/agendamentos/{cpf}")
def alterar_agendamento(cpf: str, agendamento: Agendamento):
    for i, a in enumerate(agendamentos):
        if a.usuario_cpf == cpf and a.data == agendamento.data:
            agendamentos[i] = agendamento
            return agendamento
    raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

@app.delete("/agendamentos/{cpf}/{data}")
def excluir_agendamento(cpf: str, data: date):
    global agendamentos
    agendamentos = [
        a for a in agendamentos 
        if not (a.usuario_cpf == cpf and a.data == data)
    ]
    return {"message": f"Agendamento para CPF {cpf} na data {data} excluído com sucesso."}

# --- Rodar a aplicação ---
# Execute `uvicorn script_name:app --reload` para rodar a aplicação
