from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .crud import create_doctor, create_enfermera
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# ----------- BLOQUE P1: FILIACION -----------
@app.post("/filiacion/")
def guardar_filiacion(data: dict, db: Session = Depends(get_db)):
    nueva = models.DeclaracionJurada(**data); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.get("/api/paciente-completo/{paciente_id}")
def obtener_paciente_completo(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente: raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {
        "paciente": paciente,
        "filiacion": db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first(),
        "antecedentes": db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente_id).first(),
        "habitos": db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente_id).first()
    }

# ----------- BLOQUE P2 y P3 -----------
@app.post("/p2/")
def guardar_p2(data: dict, db: Session = Depends(get_db)):
    nueva = models.AntecedentesP2(**data); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.post("/p3/")
def guardar_p3(data: dict, db: Session = Depends(get_db)):
    nueva = models.HabitosRiesgosP3(**data); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

# ----------- GESTION PACIENTES -----------
@app.get("/pacientes/")
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/pacientes/")
def registrar_paciente(data: dict, db: Session = Depends(get_db)):
    nuevo = models.Paciente(**data); db.add(nuevo); db.commit(); db.refresh(nuevo); return nuevo

@app.get("/buscar-id-por-codigo/{codigo}")
def buscar_id_por_codigo(codigo: str, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.codigo_paciente == codigo).first()
    if not p: raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"id": p.id}

# ----------- FICHA MÉDICA -----------
@app.post("/ficha-oftalmo/")
def guardar_ficha_oftalmo(data: dict, db: Session = Depends(get_db)):
    nueva = models.FichaOftalmologica(**data); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.get("/ficha-oftalmo/{paciente_id}")
def obtener_ficha_oftalmo(paciente_id: int, db: Session = Depends(get_db)):
    ficha = db.query(models.FichaOftalmologica).filter(models.FichaOftalmologica.paciente_id == paciente_id).first()
    if not ficha: raise HTTPException(status_code=404, detail="Ficha no encontrada")
    return ficha
# ----------- FICHA PSICOLOGICA -----------
@app.post("/guardar-psicologia/")
def guardar_psicologia(data: dict, db: Session = Depends(get_db)):
    codigo = data.get("codigo_paciente")
    paciente = db.query(models.Paciente).filter(models.Paciente.codigo_paciente == codigo).first()
    if not paciente: raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    datos = data.copy()
    datos["paciente_id"] = paciente.id
    nueva = models.FichaPsicologia(**datos); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.get("/ficha-psicologia/{paciente_id}")
def obtener_ficha_psicologia(paciente_id: int, db: Session = Depends(get_db)):
    ficha = db.query(models.FichaPsicologia).filter(models.FichaPsicologia.paciente_id == paciente_id).first()
    if not ficha: raise HTTPException(status_code=404, detail="Ficha psicológica no encontrada")
    return ficha



# ----------- PERSONAL: DOCTORES -----------
@app.get("/personal/")
def obtener_personal(db: Session = Depends(get_db)):
    return {"doctores": db.query(models.Doctor).all(), "enfermeras": db.query(models.Enfermera).all()}

@app.post("/doctores/")
def registrar_doctor(data: dict, db: Session = Depends(get_db)): return create_doctor(db, data)

@app.get("/doctores/{id_doc}")
def obtener_doctor(id_doc: int, db: Session = Depends(get_db)):
    d = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not d: raise HTTPException(status_code=404, detail="No encontrado")
    return d

@app.put("/doctores/{id_doc}")
def actualizar_doctor(id_doc: int, data: dict, db: Session = Depends(get_db)):
    d = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not d: raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in data.items(): setattr(d, k, v)
    db.commit(); db.refresh(d); return d

@app.delete("/doctores/{id_doc}")
def borrar_doctor(id_doc: int, db: Session = Depends(get_db)):
    d = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not d: raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(d); db.commit(); return {"message": "Eliminado"}

# ----------- PERSONAL: ENFERMERAS -----------
@app.post("/enfermeras/")
def registrar_enfermera(data: dict, db: Session = Depends(get_db)): return create_enfermera(db, data)

@app.get("/enfermeras/{id_enfe}")
def obtener_enfermera(id_enfe: int, db: Session = Depends(get_db)):
    e = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not e: raise HTTPException(status_code=404, detail="No encontrada")
    return e

@app.put("/enfermeras/{id_enfe}")
def actualizar_enfermera(id_enfe: int, data: dict, db: Session = Depends(get_db)):
    e = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not e: raise HTTPException(status_code=404, detail="No encontrada")
    for k, v in data.items(): setattr(e, k, v)
    db.commit(); db.refresh(e); return e

@app.delete("/enfermeras/{id_enfe}")
def borrar_enfermera(id_enfe: int, db: Session = Depends(get_db)):
    e = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not e: raise HTTPException(status_code=404, detail="No encontrada")
    db.delete(e); db.commit(); return {"message": "Eliminada"}
