from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import SessionLocal, engine, Base
from .crud import create_doctor, create_enfermera
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
    # Usamos func.upper para normalizar la búsqueda contra el modelo
    p = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo.upper().strip()).first()
    
    if not p: 
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
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
@app.post("/guardar-psicologia")
async def guardar_psicologia(data: dict, db: Session = Depends(get_db)):
    codigo_input = str(data.get("codigo_paciente", "")).strip().upper()
    if not codigo_input:
        raise HTTPException(status_code=400, detail="El código del paciente es obligatorio")

    # Búsqueda normalizada
    paciente = db.query(models.Paciente).filter(
        func.upper(models.Paciente.codigo_paciente) == codigo_input
    ).first()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado en el sistema")

    try:
        nueva_ficha = models.FichaPsicologia(
            paciente_id=paciente.id,
            historia_familiar=data.get("historia_familiar"),
            personalidad=data.get("personalidad"),
            conducta_sexual=data.get("conducta_sexual"),
            habitos_alcohol=data.get("habitos_alcohol"),
            habitos_tabaco=data.get("habitos_tabaco"),
            habitos_drogas=data.get("habitos_drogas"),
            habitos_coquear=data.get("habitos_coquear"),
            otras_observaciones=data.get("otras_observaciones"),
            presentacion=data.get("presentacion"),
            postura=data.get("postura"),
            discurso=data.get("discurso"),
            pensamiento=data.get("pensamiento"),
            percepcion=data.get("percepcion"),
            resultado_psicologico=data.get("resultado_psicologico")
        )
        db.add(nueva_ficha)
        db.commit()
        db.refresh(nueva_ficha)
        return {"message": "GUARDADO EXITOSAMENTE"}
    except Exception as e:
        print(f"Error al guardar: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ficha-psicologia/{paciente_id}")
def obtener_ficha_psicologia(paciente_id: int, db: Session = Depends(get_db)):
    ficha = db.query(models.FichaPsicologia).filter(models.FichaPsicologia.paciente_id == paciente_id).first()
    if not ficha: raise HTTPException(status_code=404, detail="Ficha no encontrada")
    return ficha

# NUEVO ENDPOINT PARA CONSULTAS (El que faltaba)
@app.get("/ficha-psicologia-filtrada/{estado}")
def obtener_fichas_por_estado(estado: str, db: Session = Depends(get_db)):
    fichas = db.query(models.FichaPsicologia).filter(models.FichaPsicologia.resultado_psicologico == estado).all()
    resultados = []
    for f in fichas:
        paciente = db.query(models.Paciente).filter(models.Paciente.id == f.paciente_id).first()
        if paciente:
            resultados.append({
                "codigo": paciente.codigo_paciente,
                "nombre": f"{paciente.apellido} {paciente.nombre}",
                "estado": f.resultado_psicologico
            })
    return resultados


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


# ----------- FICHA CARDIOLOGIA -----------
@app.post("/guardar-cardiologia")
async def guardar_cardiologia(data: dict, db: Session = Depends(get_db)):
    codigo_input = str(data.get("codigo_paciente", "")).strip().upper()
    paciente = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo_input).first()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    nueva_ficha = models.FichaCardiologia(
        paciente_id=paciente.id,
        ninez=data.get("ninez"),
        tabaquismo=data.get("tabaquismo"),
        hta=data.get("hta"),
        adolescente=data.get("adolescente"),
        hiperlipidemias=data.get("hiperlipidemias"),
        diabetes=data.get("diabetes"),
        adultez=data.get("adultez"),
        asma_bronquial=data.get("asma_bronquial"),
        bronquitis=data.get("bronquitis"),
        obs_antecedentes=data.get("obs_antecedentes"),
        padre=data.get("padre"),
        madre=data.get("madre"),
        hermanos=data.get("hermanos"),
        abuelos=data.get("abuelos"),
        hijos=data.get("hijos"),
        obs_familiares=data.get("obs_familiares"),
        anamnesis=data.get("anamnesis"),
        presion_arterial=data.get("presion_arterial"),
        frecuencia_cardiaca=data.get("frecuencia_cardiaca"),
        pulso=data.get("pulso"),
        frecuencia_respiratoria=data.get("frecuencia_respiratoria"),
        talla=data.get("talla"),
        peso=data.get("peso"),
        imc=data.get("imc"),
        sat_o2=data.get("sat_o2"),
        examen_clinico=data.get("examen_clinico"),
        resultado_electro=data.get("resultado_electro"),
        diagnostico_recomendaciones=data.get("diagnostico_recomendaciones")
    )
    db.add(nueva_ficha)
    db.commit()
    return {"status": "success"}



@app.get("/ficha-cardiologia/{paciente_id}")
def obtener_ficha_cardiologia(paciente_id: int, db: Session = Depends(get_db)):
    ficha = db.query(models.FichaCardiologia).filter(models.FichaCardiologia.paciente_id == paciente_id).first()
    if not ficha: raise HTTPException(status_code=404, detail="Ficha no encontrada")
    return ficha

@app.get("/consulta-cardiologia/{diagnostico}")
def consultar_cardiologia(diagnostico: str, db: Session = Depends(get_db)):
    # Buscamos fichas que contengan el texto en el diagnóstico
    fichas = db.query(models.FichaCardiologia).filter(
        models.FichaCardiologia.diagnostico_recomendaciones.contains(diagnostico)
    ).all()
    
    resultados = []
    for f in fichas:
        p = db.query(models.Paciente).filter(models.Paciente.id == f.paciente_id).first()
        if p:
            resultados.append({
                "codigo": p.codigo_paciente,
                "nombre": f"{p.apellido} {p.nombre}",
                "diagnostico": f.diagnostico_recomendaciones
            })
    return resultados

@app.get("/filtrar-cardiologia")
async def filtrar_cardiologia(query: str, db: Session = Depends(get_db)):
    # Buscamos en la tabla ficha_cardiologia filtrando por diagnostico_recomendaciones
    resultados = db.query(models.FichaCardiologia, models.Paciente).join(
        models.Paciente
    ).filter(
        models.FichaCardiologia.diagnostico_recomendaciones.ilike(f"%{query}%")
    ).all()
    
    return [
        {
            "codigo_paciente": p.codigo_paciente,
            "nombre_paciente": p.nombre_completo,
            "diagnostico": f.diagnostico_recomendaciones
        } for f, p in resultados
    ]


@app.get("/buscar-cardiologia")
async def buscar_cardiologia(antecedente: str, db: Session = Depends(get_db)):
    # Mapeo directo a los atributos del modelo
    columnas = {
        "NINEZ": models.FichaCardiologia.ninez,
        "ADOLESCENTE": models.FichaCardiologia.adolescente,
        "ADULTEZ": models.FichaCardiologia.adultez,
        "TABAQUISMO": models.FichaCardiologia.tabaquismo,
        "HIPERLIPIDEMIAS": models.FichaCardiologia.hiperlipidemias,
        "ASMA_BRONQUIAL": models.FichaCardiologia.asma_bronquial,
        "HTA": models.FichaCardiologia.hta,
        "DIABETES": models.FichaCardiologia.diabetes,
        "BRONQUITIS": models.FichaCardiologia.bronquitis
    }
    
    columna_modelo = columnas.get(antecedente.upper().strip())
    if not columna_modelo:
        return []

    # EJECUCIÓN: Query sin el alias de modelo confuso, referenciando las tablas desde la sesión
    query = db.query(models.Paciente.codigo_paciente, models.Paciente.nombre, models.Paciente.apellido).\
               join(models.FichaCardiologia, models.FichaCardiologia.paciente_id == models.Paciente.id).\
               filter(columna_modelo == "SI").all()

    # Formateo de salida para que el frontend reciba algo que entienda
    return [{"codigo": r[0], "nombre": f"{r[1]} {r[2]}", "detalle": "CONFIRMADO"} for r in query]


# -----------------FICHA ESPIROMETRÍA -----------------
@app.post("/guardar-espirometria")
async def guardar_espirometria(data: dict):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Mapeo completo sincronizado con la estructura de tu modelo y base de datos
        query = """
            INSERT INTO ficha_espirometria (
                paciente_id, criterios_exclusion_1, criterios_exclusion_2, criterios_exclusion_3, 
                criterios_exclusion_4, criterios_exclusion_5, hemoptisis, infarto_reciente, 
                neumotorax, fiebre_nauseas, traqueostomia, embarazo_avanzado, sonda_pleural, 
                embarazo_complicado, aneurisma_cerebral, inestabilidad_cv, embolia_pulmonar, 
                infeccion_respiratoria, infeccion_oido, uso_aerosoles, uso_aerosoles_detalle, 
                fumo_ultimas_horas, fumo_cantidad_detalle, ejercicio_fisico, comio_ultima_hora, 
                tos_flemas, tos_flemas_detalle, equipo_proteccion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        valores = (
            None, # paciente_id
            data.get("criterios_exclusion_1", ""), data.get("criterios_exclusion_2", ""),
            data.get("criterios_exclusion_3", ""), data.get("criterios_exclusion_4", ""),
            data.get("criterios_exclusion_5", ""), data.get("hemoptisis", ""),
            data.get("infarto_reciente", ""), data.get("neumotorax", ""),
            data.get("fiebre_nauseas", ""), data.get("traqueostomia", ""),
            data.get("embarazo_avanzado", ""), data.get("sonda_pleural", ""),
            data.get("embarazo_complicado", ""), data.get("aneurisma_cerebral", ""),
            data.get("inestabilidad_cv", ""), data.get("embolia_pulmonar", ""),
            data.get("infeccion_respiratoria", ""), data.get("infeccion_oido", ""),
            data.get("uso_aerosoles", ""), data.get("uso_aerosoles_detalle", ""),
            data.get("fumo_ultimas_horas", ""), data.get("fumo_cantidad_detalle", ""),
            data.get("ejercicio_fisico", ""), data.get("comio_ultima_hora", ""),
            data.get("tos_flemas", ""), data.get("tos_flemas_detalle", ""),
            data.get("equipo_proteccion", "")
        )
        
        cursor.execute(query, valores)
        db.commit()
        return {"status": "success", "message": "Guardado exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------
@app.get("/consultar-espirometria/{codigo_paciente}")
async def consultar_espirometria(codigo_paciente: str):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM espirometria WHERE codigo_paciente = ?", (codigo_paciente.strip().upper(),))
        row = cursor.fetchone()
        return dict(row) if row else {"status": "error", "message": "Paciente no encontrado"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
# -------
@app.get("/listar-espirometria")
async def listar_espirometria(filtro: str = ""):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM espirometria WHERE codigo_paciente LIKE ?", (f"%{filtro.strip().upper()}%",))
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- FIN DE LÓGICA COMPLETA Y DEFINITIVA PARA ESPIROMETRÍA ---

