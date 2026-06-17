from sqlalchemy import Column, Integer, String, ForeignKey, Text
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    ci = Column(String, unique=True)
    codigo_paciente = Column(String)

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_p1"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    edad = Column(String); sexo = Column(String)
    fecha_nacimiento = Column(String); lugar_nacimiento = Column(String)
    domicilio = Column(String); n_casa = Column(String)
    zona_barrio = Column(String); ciudad = Column(String)
    pais = Column(String); telefono = Column(String)
    estado_civil = Column(String); profesion_oficio = Column(String)

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    vista = Column(String); auditivo = Column(String); respiratorio = Column(String)
    cardio = Column(String); digestivos = Column(String); sangre = Column(String)
    genitourinario = Column(String); sistema_nervioso = Column(String)
    psiquiatricos = Column(String); osteomusculares = Column(String)
    reumatologicos = Column(String); dermatologicas = Column(String)
    alergias = Column(String); cirugias = Column(String); infecciones = Column(String)
    acc_personales = Column(String); acc_trabajo = Column(String)
    medicamentos = Column(String); endocrino = Column(String)
    familiares = Column(String); otros_especificos = Column(String); generales = Column(String)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    fuma = Column(String); fuma_cantidad = Column(String)
    alcohol = Column(String); alcohol_frecuencia = Column(String)
    drogas = Column(String); drogas_tipo = Column(String)
    coca = Column(String); deporte = Column(String); deporte_detalle = Column(String)
    grupo_sanguineo = Column(String); historia_laboral = Column(Text)
    riesgos_expuestos = Column(Text); observaciones = Column(String)

class Enfermera(Base):
    __tablename__ = "enfermeras"
    id_enfe = Column(Integer, primary_key=True, index=True)
    ci_enfe = Column(String, unique=True)
    appaterno_enfe = Column(String); apmaterno_enfe = Column(String)
    nombre_enfe = Column(String); turno_enfe = Column(String)
    edu_enfe = Column(String); especialidad = Column(String)

class Doctor(Base):
    __tablename__ = "doctores"
    id_doc = Column(Integer, primary_key=True, index=True)
    ci_doc = Column(String, unique=True)
    appaterno_doc = Column(String); apmaterno_doc = Column(String)
    nombre_doc = Column(String); turno_doc = Column(String); especialidad = Column(String)

class FichaOftalmologica(Base):
    __tablename__ = "ficha_oftalmologica"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    lentes = Column(String); daltonismo = Column(String); diabetes = Column(String)
    estrabismo = Column(String); infecciones = Column(String); presion_alta = Column(String)
    obs_ant = Column(Text); anamnesis = Column(String); ana_obs = Column(Text)
    examen_externo = Column(String); exe_obs = Column(Text)
    od_l_sc = Column(String); od_l_cc = Column(String); od_l_dio = Column(String)
    oi_l_sc = Column(String); oi_l_cc = Column(String); oi_l_dio = Column(String)
    od_c_sc = Column(String); od_c_cc = Column(String); od_c_dio = Column(String)
    oi_c_sc = Column(String); oi_c_cc = Column(String); oi_c_dio = Column(String)
    cv_od = Column(String); cv_od_obs = Column(Text); cv_oi = Column(String); cv_oi_obs = Column(Text)
    fo = Column(String); fo_obs = Column(Text); ish = Column(String); ish_obs = Column(Text)
    est = Column(String); est_obs = Column(Text); pio_od = Column(String)
    pio_oi = Column(String); pio_obs = Column(String); diagnostico = Column(Text)

class FichaPsicologia(Base):
    __tablename__ = "fichas_psicologia"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer)
    historia_familiar = Column(String)
    personalidad = Column(String)
    conducta_sexual = Column(String)
    habitos_alcohol = Column(String)
    habitos_tabaco = Column(String)
    habitos_drogas = Column(String) # Cambiado de 'drogas'
    habitos_coquear = Column(String) # Cambiado de 'coquear'
    otras_observaciones = Column(String)
    presentacion = Column(String)
    postura = Column(String)
    discurso = Column(String)
    pensamiento = Column(String)
    percepcion = Column(String)
    resultado_psicologico = Column(String) # CAMBIADO: 'psicologicamente' por 'resultado_psicologico'

class FichaEspirometria(Base):
    __tablename__ = "ficha_espirometria"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    
    # Criterios de Exclusión (5 preguntas)
    criterios_exclusion_1 = Column(String); criterios_exclusion_2 = Column(String)
    criterios_exclusion_3 = Column(String); criterios_exclusion_4 = Column(String)
    criterios_exclusion_5 = Column(String)
    
    # Para el Profesional (6 campos)
    hemoptisis = Column(String); infarto_reciente = Column(String)
    neumotorax = Column(String); fiebre_nauseas = Column(String)
    traqueostomia = Column(String); embarazo_avanzado = Column(String)
        
    # Entrevistados sin criterios (8 preguntas + 3 detalles)
    infeccion_respiratoria = Column(String); infeccion_oido = Column(String)
    uso_aerosoles = Column(String); uso_aerosoles_detalle = Column(String) # Campo hrs
    fumo_ultimas_horas = Column(String); fumo_cantidad_detalle = Column(String)
    ejercicio_fisico = Column(String); comio_ultima_hora = Column(String)
    tos_flemas = Column(String); tos_flemas_detalle = Column(String) # Campo desde cuando
    equipo_proteccion = Column(String)

class FichaElectroencefalograma(Base):
    __tablename__ = "ficha_electroencefalograma"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    cefaleas = Column(String); epilepsia = Column(String); convulsiones = Column(String)
    accidente = Column(String); perdida_conocimiento = Column(String); paralisis = Column(String)
    otros_antecedentes = Column(Text); derrame_cerebral = Column(String); quirurgicos = Column(String)
    observaciones_antecedentes = Column(Text); marcha = Column(String); reflejos = Column(String)
    coordinacion_dedo_nariz = Column(String); coordinacion_talon_rodilla = Column(String)
    romberg = Column(String); vertigo_nistagmo = Column(String); vertigo_adaptacion = Column(String)
    observaciones_examen = Column(Text); descripcion_estudio = Column(String)
    resultado_estudio = Column(String); observaciones_estudio = Column(Text)

class FichaCardiologia(Base):
    __tablename__ = "ficha_cardiologia"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    
    ninez = Column(String)
    tabaquismo = Column(String)
    hta = Column(String)
    adolescente = Column(String)
    hiperlipidemias = Column(String)
    diabetes = Column(String)
    adultez = Column(String)
    asma_bronquial = Column(String)
    bronquitis = Column(String)
    obs_antecedentes = Column(Text)
    padre = Column(String)
    madre = Column(String)
    hermanos = Column(String)
    abuelos = Column(String)
    hijos = Column(String)
    obs_familiares = Column(Text)
    anamnesis = Column(Text)
    presion_arterial = Column(String)
    frecuencia_cardiaca = Column(String)
    pulso = Column(String)
    frecuencia_respiratoria = Column(String)
    talla = Column(String)
    peso = Column(String)
    imc = Column(String)
    sat_o2 = Column(String)
    examen_clinico = Column(Text)
    resultado_electro = Column(Text)
    diagnostico_recomendaciones = Column(Text)

