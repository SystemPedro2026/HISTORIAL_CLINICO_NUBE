from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from api.models import FichaElectroencefalograma, Paciente 
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import SessionLocal, engine, Base
from .crud import create_doctor, create_enfermera
from . import models
from .models import FichaAptitudFisica 
from .database import get_db

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

# ----------- FICHA ESPIROMETRÍA (SOLUCIÓN DEFINITIVA) -----------
@app.post("/guardar-espirometria")
async def guardar_espirometria(data: dict, db: Session = Depends(get_db)):
    try:
        codigo = str(data.get("codigo_paciente", "")).strip().upper()
        paciente = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo).first()
        
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        # Mapeo exacto basado en tu models.py
        nueva_ficha = models.FichaEspirometria(
            paciente_id=paciente.id,
            criterios_exclusion_1=data.get("criterios_exclusion_1"),
            criterios_exclusion_2=data.get("criterios_exclusion_2"),
            criterios_exclusion_3=data.get("criterios_exclusion_3"),
            criterios_exclusion_4=data.get("criterios_exclusion_4"),
            criterios_exclusion_5=data.get("criterios_exclusion_5"),
            
            hemoptisis=data.get("hemoptisis"),
            infarto_reciente=data.get("infarto_reciente"),
            neumotorax=data.get("neumotorax"),
            fiebre_nauseas=data.get("fiebre_nauseas"),
            traqueostomia=data.get("traqueostomia"),
            embarazo_avanzado=data.get("embarazo_avanzado"),
                  
            infeccion_respiratoria=data.get("infeccion_respiratoria"),
            infeccion_oido=data.get("infeccion_oido"),
            uso_aerosoles=data.get("uso_aerosoles"),
            uso_aerosoles_detalle=data.get("uso_aerosoles_detalle"),
            fumo_ultimas_horas=data.get("fumo_ultimas_horas"),
            fumo_cantidad_detalle=data.get("fumo_cantidad_detalle"),
            ejercicio_fisico=data.get("ejercicio_fisico"),
            comio_ultima_hora=data.get("comio_ultima_hora"),
            tos_flemas=data.get("tos_flemas"),
            tos_flemas_detalle=data.get("tos_flemas_detalle"),
            equipo_proteccion=data.get("equipo_proteccion")
        )
        db.add(nueva_ficha)
        db.commit()
        db.refresh(nueva_ficha)
        return {"status": "success", "message": "GUARDADO EXITOSAMENTE"}
    except Exception as e:
        # Esto imprimirá el error real en los logs de Render
        print(f"ERROR DETALLADO: {str(e)}") 
        raise HTTPException(status_code=500, detail=str(e))
# ----------------------------
@app.get("/consultar-espirometria/{codigo_paciente}")
async def consultar_espirometria(codigo_paciente: str, db: Session = Depends(get_db)):
    # Buscamos al paciente
    paciente = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo_paciente.upper().strip()).first()
    if not paciente:
        return {"status": "error", "message": "Paciente no encontrado"}
    
    # Buscamos la ficha en la tabla correcta
    ficha = db.query(models.FichaEspirometria).filter(models.FichaEspirometria.paciente_id == paciente.id).first()
    if not ficha:
        return {"status": "error", "message": "Ficha no encontrada"}
        
    return ficha

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

# ----------- ENDPOINT PARA CONSULTA FILTRADA ESPIROMETRÍA -----------
@app.get("/espirometria-filtrada/{sintoma}")
def obtener_espirometria_por_sintoma(sintoma: str, db: Session = Depends(get_db)):
    # Filtramos la tabla FichaEspirometria donde el síntoma sea "SI"
    # Mapeamos los valores del frontend a los campos del modelo
    mapeo = {
        "hemoptisis": models.FichaEspirometria.hemoptisis,
        "infarto_reciente": models.FichaEspirometria.infarto_reciente,
        "neumotorax": models.FichaEspirometria.neumotorax,
        "fiebre_nauseas": models.FichaEspirometria.fiebre_nauseas,
        "traqueostomia": models.FichaEspirometria.traqueostomia,
        "embarazo_avanzado": models.FichaEspirometria.embarazo_avanzado
    }
    
    campo = mapeo.get(sintoma.lower())
    if not campo:
        return []

    fichas = db.query(models.FichaEspirometria).filter(campo == "SI").all()
    
    resultados = []
    for f in fichas:
        paciente = db.query(models.Paciente).filter(models.Paciente.id == f.paciente_id).first()
        if paciente:
            resultados.append({
                "codigo": paciente.codigo_paciente,
                "nombre": f"{paciente.apellido} {paciente.nombre}",
                "estado": sintoma.upper()
            })
    return resultados

# ------------------- FICHA ALTURA --------------------------
@app.post("/guardar-altura")
async def guardar_altura(data: dict, db: Session = Depends(get_db)):
    try:
        codigo = str(data.get("codigo_paciente", "")).strip().upper()
        paciente = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo).first()
        
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        nueva_ficha = models.FichaAltura(
            paciente_id=paciente.id,
            agorafobia=data.get("agorafobia"),
            diabetes=data.get("diabetes"),
            acrofobia=data.get("acrofobia"),
            insuficiencia_cardiaca=data.get("insuficiencia_cardiaca"),
            arritmia=data.get("arritmia"),
            hipertension=data.get("hipertension"),
            consumo_drogas=data.get("consumo_drogas"),
            meniere=data.get("meniere"),
            enfermedad_psiquiatrica=data.get("enfermedad_psiquiatrica"),
            ametropia=data.get("ametropia"),
            trauma_encefalo=data.get("trauma_encefalo"),
            esteropsis=data.get("esteropsis"),
            convulsiones=data.get("convulsiones"),
            asma_bronquial=data.get("asma_bronquial"),
            vertigo=data.get("vertigo"),
            hipoacusia=data.get("hipoacusia"),
            sincope=data.get("sincope"),
            accidentes_fracturas=data.get("accidentes_fracturas"),
            mioclonias=data.get("mioclonias"),
            deformidades=data.get("deformidades"),
            cefaleas=data.get("cefaleas"),
            obs_antecedentes=data.get("obs_antecedentes"),
            soplo_cardiaco=data.get("soplo_cardiaco"),
            sustentacion_pie=data.get("sustentacion_pie"),
            arritmias_cardiacas=data.get("arritmias_cardiacas"),
            camina_libre=data.get("camina_libre"),
            nistagmus=data.get("nistagmus"),
            adiacocinesia=data.get("adiacocinesia"),
            test_romberg=data.get("test_romberg"),
            audicion=data.get("audicion"),
            test_barany=data.get("test_barany"),
            marcha_ojos_cerrados=data.get("marcha_ojos_cerrados"),
            test_babinsky=data.get("test_babinsky"),
            extremidades=data.get("extremidades"),
            obs_examen=data.get("obs_examen")
        )
        db.add(nueva_ficha)
        db.commit()
        db.refresh(nueva_ficha)
        return {"status": "success", "message": "GUARDADO EXITOSAMENTE"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/consultar-altura/{codigo_paciente}")
async def consultar_altura(codigo_paciente: str, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo_paciente.upper().strip()).first()
    if not paciente:
        return {"status": "error", "message": "Paciente no encontrado"}
    
    ficha = db.query(models.FichaAltura).filter(models.FichaAltura.paciente_id == paciente.id).first()
    if not ficha:
        return {"status": "error", "message": "Ficha no encontrada"}
        
    return ficha

@app.get("/filtrar-altura/{campo}")
def filtrar_altura(campo: str, db: Session = Depends(get_db)):
    # Mapeo exacto a las columnas de la tabla FichaAltura
    mapeo = {
        "soplo_cardiaco": models.FichaAltura.soplo_cardiaco,
        "arritmias_cardiacas": models.FichaAltura.arritmias_cardiacas,
        "nistagmus": models.FichaAltura.nistagmus,
        "test_romberg": models.FichaAltura.test_romberg,
        "test_barany": models.FichaAltura.test_barany,
        "test_babinsky": models.FichaAltura.test_babinsky
    }
    columna = mapeo.get(campo)
    if not columna: return []

    # Consulta corregida con join explícito
    fichas = db.query(models.FichaAltura, models.Paciente).join(
        models.Paciente, models.FichaAltura.paciente_id == models.Paciente.id
    ).filter(columna == "SI").all()
    
    return [{"codigo": f.Paciente.codigo_paciente, "nombre": f"{f.Paciente.apellido} {f.Paciente.nombre}", "estado": "ANORMAL"} for f in fichas]

# ----------- FICHA ELECTROENCEFALOGRAMA -----------

@app.post("/guardar-electro")
async def guardar_electro(data: dict, db: Session = Depends(get_db)):
    # 1. Buscar paciente primero
    codigo = str(data.get("codigo_paciente", "")).strip().upper()
    paciente = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo).first()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # 2. Crear instancia con nombres exactos de columnas (ajustados a tu BD)
    try:
        nueva_ficha = models.FichaElectroencefalograma(
            paciente_id=paciente.id,
            cefaleas=data.get("cefaleas"),
            epilepsia=data.get("epilepsia"),
            convulsiones=data.get("convulsiones"),
            accidente=data.get("accidente"),
            perdida_conocimiento=data.get("perdida_conocimiento"),
            paralisis=data.get("paralisis"),
            otros_antecedentes=data.get("otros_antecedentes"),
            derrame_cerebral=data.get("derrame_cerebral"),
            quirurgicos=data.get("quirurgicos"),
            observaciones_antecedentes=data.get("observaciones_antecedentes"),
            marcha=data.get("marcha"),
            reflejos=data.get("reflejos"),
            coordinacion_dedo_nariz=data.get("coordinacion_dedo_nariz"),
            coordinacion_talon_rodilla=data.get("coordinacion_talon_rodilla"),
            romberg=data.get("romberg"),
            vertigo_nistagmo=data.get("vertigo_nistagmo"),
            vertigo_adaptacion=data.get("vertigo_adaptacion"),
            observaciones_examen=data.get("observaciones_examen"),
            descripcion_estudio=data.get("descripcion_estudio"),
            resultado_estudio=data.get("resultado_estudio"),
            observaciones_estudio=data.get("observaciones_estudio"),
            reposo=data.get("reposo"),
            fotoestimulacion=data.get("fotoestimulacion"),
            hipernea=data.get("hipernea"),
            diagnostico_recomendaciones=data.get("diagnostico_recomendaciones")
        )
        
        # 3. Guardar
        db.add(nueva_ficha)
        db.commit()
        db.refresh(nueva_ficha)
        return {"status": "success"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/consultar-electro-por-campo/{campo}")
async def consultar_electro_por_campo(campo: str, db: Session = Depends(get_db)):
    # Traemos todos los registros sin filtros complejos para evitar errores
    registros = db.query(models.FichaElectroencefalograma).all()
    lista = []
    
    for r in registros:
        # Obtenemos el valor de forma segura
        valor = getattr(r, campo, None)
        # Si el valor existe y no es "NO", lo agregamos
        if valor and str(valor).strip().upper() != 'NO':
            paciente = db.query(models.Paciente).filter(models.Paciente.id == r.paciente_id).first()
            lista.append({
                "codigo_paciente": paciente.codigo_paciente if paciente else "N/A",
                "nombre_paciente": f"{paciente.nombre} {paciente.apellido}" if paciente else "Desconocido",
                "valor": valor
            })
    return lista # Esto siempre será una lista, nunca dará error al iterar

# ----------- FICHA APTITUD MÉDICO OCUPACIONAL -----------
@app.post("/guardar-aptitud")
async def guardar_aptitud(data: dict, db: Session = Depends(get_db)):
    try:
        # Validación: buscar paciente
        codigo = str(data.get("codigo_paciente", "")).strip().upper()
        paciente = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo).first()
        if not paciente:
            return {"status": "error", "message": "Paciente no encontrado"}

        # Crear objeto con mapeo estricto
        nueva_ficha = models.FichaAptitud(
            paciente_id=paciente.id,
            razon_social=data.get("razon_social"),
            actividad_economica=data.get("actividad_economica"),
            dia=data.get("dia"),
            mes=data.get("mes"),
            anio=data.get("anio"),
            tipo_examen=data.get("tipo_examen"),
            detalle_otros=data.get("detalle_otros"),
            apellido_paterno=data.get("apellido_paterno"),
            apellido_materno=data.get("apellido_materno"),
            nombres=data.get("nombres"),
            edad=data.get("edad"),
            genero=data.get("genero"),
            nro_doc_identidad=data.get("nro_doc_identidad"),
            puesto_trabajo=data.get("puesto_trabajo"),
            resultado=str(data.get("resultado", "")).upper(),
            detalle_conclusion=data.get("detalle_conclusion"),
            recomendacion_1=data.get("recomendacion_1"),
            recomendacion_2=data.get("recomendacion_2"),
            recomendacion_3=data.get("recomendacion_3"),
            recomendacion_4=data.get("recomendacion_4")
        )
        db.add(nueva_ficha)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/consultar-aptitud/{codigo_paciente}")
async def consultar_aptitud(codigo_paciente: str, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(func.upper(models.Paciente.codigo_paciente) == codigo_paciente.upper().strip()).first()
    if not paciente:
        return {"status": "error", "message": "Paciente no encontrado"}
    
    ficha = db.query(models.FichaAptitud).filter(models.FichaAptitud.paciente_id == paciente.id).first()
    if not ficha:
        return {"status": "error", "message": "Ficha no encontrada"}
        
    return ficha

@app.get("/filtrar-aptitud/{resultado}")
def filtrar_aptitud_por_resultado(resultado: str, db: Session = Depends(get_db)):
    # Consulta optimizada para el listado de pacientes según su resultado
    fichas = db.query(models.FichaAptitud).filter(models.FichaAptitud.resultado == resultado.upper()).all()
    resultados = []
    for f in fichas:
        paciente = db.query(models.Paciente).filter(models.Paciente.id == f.paciente_id).first()
        if paciente:
            resultados.append({
                "codigo": paciente.codigo_paciente,
                "nombre": f"{paciente.apellido} {paciente.nombre}",
                "resultado": f.resultado
            })
    return resultados


# ----------- FICHA APTITUD FISICA Y PSICOLOGICA -----------
@app.post("/guardar-aptitud-fisica")
def guardar_aptitud_fisica(data: dict, db: Session = Depends(get_db)):
    # Verificación de existencia del paciente para evitar registros huérfanos
    paciente_existente = db.query(Paciente).filter(Paciente.codigo_paciente == data.get("codigo_paciente")).first()
    
    if not paciente_existente:
        raise HTTPException(status_code=404, detail="El Código del Paciente no existe en la base de datos.")
    
    try:
        nueva_ficha = FichaAptitudFisica(
            codigo_paciente=data.get("codigo_paciente"),
            razon_social=data.get("razon_social"),
            actividad_economica=data.get("actividad_economica"),
            dia=data.get("dia"),
            mes=data.get("mes"),
            anio=data.get("anio"),
            tipo_examen=data.get("tipo_examen"),
            otros_tipo=data.get("otros_tipo"),
            ape_pat=data.get("ape_pat"),
            ape_mat=data.get("ape_mat"),
            nombres=data.get("nombres"),
            edad=data.get("edad"),
            genero=data.get("genero"),
            doc_id=data.get("doc_id"),
            puesto_trabajo=data.get("puesto_trabajo"),
            resultado_fisico=data.get("resultado_fisico"),
            resultado_psicologico=data.get("resultado_psicologico"),
            conclusion_general=data.get("conclusion_general"),
            rec1=data.get("rec1"),
            rec2=data.get("rec2"),
            rec3=data.get("rec3"),
            rec4=data.get("rec4"),
            rec5=data.get("rec5"),
            rec6=data.get("rec6")
        )
        db.add(nueva_ficha)
        db.commit()
        db.refresh(nueva_ficha)
        return {"status": "success", "id": nueva_ficha.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/buscar-aptitud-fisica/{codigo_paciente}")
def buscar_aptitud_fisica(codigo_paciente: str, db: Session = Depends(get_db)):
    ficha = db.query(FichaAptitudFisica).filter(FichaAptitudFisica.codigo_paciente == codigo_paciente).order_by(FichaAptitudFisica.id.desc()).first()
    if not ficha:
        raise HTTPException(status_code=404, detail="No se encontró registro para este código.")
    return ficha

@app.get("/filtrar-aptitud/{fisico}/{psico}")
def filtrar_aptitud(fisico: str, psico: str, db: Session = Depends(get_db)):
    resultados = db.query(FichaAptitudFisica).filter(
        FichaAptitudFisica.resultado_fisico == fisico,
        FichaAptitudFisica.resultado_psicologico == psico
    ).all()
    
    return [
        {
            "codigo": f.codigo_paciente,
            "nombre": f"{f.nombres} {f.ape_pat} {f.ape_mat}",
            "resultado": f"Físico: {f.resultado_fisico} / Psico: {f.resultado_psicologico}"
        } for f in resultados
    ]

