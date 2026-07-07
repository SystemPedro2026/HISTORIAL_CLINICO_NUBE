from sqlalchemy import Column, Integer, String, ForeignKey, Text
from .database import Base
from pydantic import BaseModel
from typing import Optional

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

class FichaAltura(Base):
    __tablename__ = "ficha_altura"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer)
    # Antecedentes
    agorafobia = Column(String)
    diabetes = Column(String)
    acrofobia = Column(String)
    insuficiencia_cardiaca = Column(String)
    arritmia = Column(String)
    hipertension = Column(String)
    consumo_drogas = Column(String)
    meniere = Column(String)
    enfermedad_psiquiatrica = Column(String)
    ametropia = Column(String)
    trauma_encefalo = Column(String)
    esteropsis = Column(String)
    convulsiones = Column(String)
    asma_bronquial = Column(String)
    vertigo = Column(String)
    hipoacusia = Column(String)
    sincope = Column(String)
    accidentes_fracturas = Column(String)
    mioclonias = Column(String)
    deformidades = Column(String)
    cefaleas = Column(String)
    obs_antecedentes = Column(Text)
    # Examen Dirigido
    soplo_cardiaco = Column(String)
    sustentacion_pie = Column(String)
    arritmias_cardiacas = Column(String)
    camina_libre = Column(String)
    nistagmus = Column(String)
    adiacocinesia = Column(String)
    test_romberg = Column(String)
    audicion = Column(String)
    test_barany = Column(String)
    marcha_ojos_cerrados = Column(String)
    test_babinsky = Column(String)
    extremidades = Column(String)
    obs_examen = Column(Text)

class FichaElectroencefalograma(Base):
    __tablename__ = "ficha_electroencefalograma"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    
    # Antecedentes
    cefaleas = Column(String); epilepsia = Column(String); convulsiones = Column(String)
    accidente = Column(String); perdida_conocimiento = Column(String); paralisis = Column(String)
    otros_antecedentes = Column(Text); derrame_cerebral = Column(String); quirurgicos = Column(String)
    observaciones_antecedentes = Column(Text)
    
    # Examen Clínico
    marcha = Column(String); reflejos = Column(String)
    coordinacion_dedo_nariz = Column(String); coordinacion_talon_rodilla = Column(String)
    romberg = Column(String); vertigo_nistagmo = Column(String); vertigo_adaptacion = Column(String)
    observaciones_examen = Column(Text)
    
    # Descripción y Activación
    descripcion_estudio = Column(String); resultado_estudio = Column(String); observaciones_estudio = Column(Text)
    diagnostico_recomendaciones = Column(Text)
    reposo = Column(String)
    fotoestimulacion = Column(String)
    hipernea = Column(String)


class FichaAptitud(Base):
    __tablename__ = "ficha_aptitud"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False)
    
    razon_social = Column(String) 
    actividad_economica = Column(String) 
 
    dia = Column(String)
    mes = Column(String)
    anio = Column(String)
    tipo_examen = Column(String)
    detalle_otros = Column(String)
    
    apellido_paterno = Column(String)
    apellido_materno = Column(String)
    nombres = Column(String)
    edad = Column(String)
    genero = Column(String)
    nro_doc_identidad = Column(String)
    puesto_trabajo = Column(String)
    
    resultado = Column(String)
    detalle_conclusion = Column(Text) 
    
    recomendacion_1 = Column(Text)
    recomendacion_2 = Column(Text)
    recomendacion_3 = Column(Text)
    recomendacion_4 = Column(Text)

class FichaAptitudFisica(Base):
    __tablename__ = "ficha_aptitud_fisica"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_paciente = Column(String, nullable=False) # ID clave para el mapeo
    razon_social = Column(String)
    actividad_economica = Column(String)
    dia = Column(String)
    mes = Column(String)
    anio = Column(String)
    tipo_examen = Column(String)
    otros_tipo = Column(String)
    ape_pat = Column(String)
    ape_mat = Column(String)
    nombres = Column(String)
    edad = Column(String)
    genero = Column(String)
    doc_id = Column(String)
    puesto_trabajo = Column(String)
    resultado_fisico = Column(String)
    resultado_psicologico = Column(String)
    conclusion_general = Column(Text)
    rec1 = Column(String)
    rec2 = Column(String)
    rec3 = Column(String)
    rec4 = Column(String)
    rec5 = Column(String)
    rec6 = Column(String)

class HistorialClinico(Base):
    __tablename__ = "historial_clinico"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    codigo_paciente = Column(String, index=True) # Clave para el mapeo y búsqueda (Punto 5)

    # SECCION I: DATOS GENERALES
    empresa = Column(String); nombre = Column(String); fecha = Column(String)
    ci = Column(String); sexo = Column(String); edad = Column(String)

    # SECCION II: OCUPACIÓN
    puesto = Column(String); area = Column(String); anos = Column(String); riesgos = Column(String)

    # SECCION III: RIESGOS
    ruido = Column(String); radiacion = Column(String); vibracion = Column(String); mecanicos = Column(String)
    temp_ext = Column(String); otros_fis = Column(String); polvo = Column(String); humos = Column(String)
    gases = Column(String); metales = Column(String); otros_quim = Column(String); mov_rep = Column(String)
    lev_carga = Column(String); otros_erg = Column(String); psico = Column(String); bio = Column(String)
    altura = Column(String); confinados = Column(String); tipo_control = Column(String)

    # SECCION IV: ANTECEDENTES
    antecedentes_det = Column(Text); enf1 = Column(String); si1 = Column(String); no1 = Column(String)
    fecha1 = Column(String); dias1 = Column(String); enf2 = Column(String); si2 = Column(String)
    no2 = Column(String); fecha2 = Column(String); dias2 = Column(String)

    # SECCION V: ANAMNESIS
    hab_anamnesis = Column(String); anamnesis_det = Column(String)

    # SECCION VI: EXAMEN FÍSICO
    ta_m = Column(String); ta_cm = Column(String); fc = Column(String); peso = Column(String)
    talla = Column(String); imc = Column(String); sat = Column(String); pam = Column(String)
    piel_n = Column(String); piel_a = Column(String); piel_d = Column(String)
    cabello_n = Column(String); cabello_a = Column(String); cabello_d = Column(String)
    ojos_n = Column(String); ojos_a = Column(String); ojos_d = Column(String)
    oidos_n = Column(String); oidos_a = Column(String); oidos_d = Column(String)
    nariz_n = Column(String); nariz_a = Column(String); nariz_d = Column(String)
    boca_n = Column(String); boca_a = Column(String); boca_d = Column(String)
    faringe_n = Column(String); faringe_a = Column(String); faringe_d = Column(String)
    cuello_n = Column(String); cuello_a = Column(String); cuello_d = Column(String)
    resp_n = Column(String); resp_a = Column(String); resp_d = Column(String)
    cardio_n = Column(String); cardio_a = Column(String); cardio_d = Column(String)
    dig_n = Column(String); dig_a = Column(String); dig_d = Column(String)
    gen_n = Column(String); gen_a = Column(String); gen_d = Column(String)
    loc_n = Column(String); loc_a = Column(String); loc_d = Column(String)
    col_n = Column(String); col_a = Column(String); col_d = Column(String)
    linf_n = Column(String); linf_a = Column(String); linf_d = Column(String)
    nerv_n = Column(String); nerv_a = Column(String); nerv_d = Column(String)

    # SECCION VII: EXÁMENES COMPLEMENTARIOS
    hem_na = Column(String); hem_n = Column(String); hem_a = Column(String); hem_d = Column(String)
    glu_na = Column(String); glu_n = Column(String); glu_a = Column(String); glu_d = Column(String)
    ure_na = Column(String); ure_n = Column(String); ure_a = Column(String); ure_d = Column(String)
    aur_na = Column(String); aur_n = Column(String); aur_a = Column(String); aur_d = Column(String)
    cre_na = Column(String); cre_n = Column(String); cre_a = Column(String); cre_d = Column(String)
    per_na = Column(String); per_n = Column(String); per_a = Column(String); per_d = Column(String)
    vdr_na = Column(String); vdr_n = Column(String); vdr_a = Column(String); vdr_d = Column(String)
    cha_na = Column(String); cha_n = Column(String); cha_a = Column(String); cha_d = Column(String)
    ego_na = Column(String); ego_n = Column(String); ego_a = Column(String); ego_d = Column(String)
    psa_na = Column(String); psa_n = Column(String); psa_a = Column(String); psa_d = Column(String)
    rxt_na = Column(String); rxt_n = Column(String); rxt_a = Column(String); rxt_d = Column(String)
    eca_na = Column(String); eca_n = Column(String); eca_a = Column(String); eca_d = Column(String)
    ecg_na = Column(String); ecg_n = Column(String); ecg_a = Column(String); ecg_d = Column(String)
    esp_na = Column(String); esp_n = Column(String); esp_a = Column(String); esp_d = Column(String)
    aud_na = Column(String); aud_n = Column(String); aud_a = Column(String); aud_d = Column(String)
    teq_na = Column(String); teq_n = Column(String); teq_a = Column(String); teq_d = Column(String)

    # SECCION VIII: DIAGNÓSTICOS
    diag1 = Column(String); diag2 = Column(String); diag3 = Column(String); diag4 = Column(String)
    diag5 = Column(String); diag6 = Column(String); diag7 = Column(String)

    # SECCION IX: CONCLUSIONES
    aptitud_apto = Column(String)
    aptitud_no_apto = Column(String)
    aptitud_restriccion = Column(String)
    observaciones = Column(Text)

    # SECCION X: RECOMENDACIONES
    rec_nutricion = Column(String)
    rec_especialidad = Column(String)
    rec_laboratorio = Column(String)
    rec_otras = Column(String)
    medidas_higiene = Column(Text)

class HistorialClinico(BaseModel):
    codigo_paciente: str
    nombre_completo: str
    edad: int
    sexo: str
    ci: str
    fecha: str
    
    # I. PUESTO
    carga_menor_25: bool
    carga_25_50: bool
    carga_mayor_50: bool
    postura_pie: bool
    postura_sentado: bool
    mov_cabeza: bool
    mov_tronco: bool
    mov_mms: bool
    mov_mmi: bool
    
    # II. ANTECEDENTES
    ant1_fecha: str
    ant1_diagnostico: str
    ant1_tratamiento: str
    ant1_comentario: str
    ant2_fecha: str
    ant2_diagnostico: str
    ant2_tratamiento: str
    ant2_comentario: str
    ant3_fecha: str
    ant3_diagnostico: str
    ant3_tratamiento: str
    ant3_comentario: str
    
    # III. HOMBRO
    hombro_dx_desde: str
    hombro_ix_desde: str
    dolor_ant_der: bool
    dolor_lat_der: bool
    dolor_pos_der: bool
    flexion_der: bool
    abduccion_der: bool
    rotacion_int_der: bool
    rotacion_ext_der: bool
    dolor_ant_izq: bool
    dolor_lat_izq: bool
    dolor_pos_izq: bool
    flexion_izq: bool
    abduccion_izq: bool
    rotacion_int_izq: bool
    rotacion_ext_izq: bool
    arco_der_presente: bool
    arco_der_ausente: bool
    arco_izq_presente: bool
    arco_izq_ausente: bool
    biceps_der_presente: bool
    biceps_der_ausente: bool
    biceps_izq_presente: bool
    biceps_izq_ausente: bool
    grave_hombro_der: str
    grave_hombro_izq: str
    observaciones_hombro: str
    
    # CODO
    codo_dx_desde: str
    codo_ix_desde: str
    edema_localizado_der: bool
    edema_nolocalizado_der: bool
    epicondilio_der: bool
    epitroclea_der: bool
    olecranon_der: bool
    musculo_epicondilio_der: bool
    musculo_epitroclea_der: bool
    edema_localizado_izq: bool
    edema_nolocalizado_izq: bool
    epicondilio_izq: bool
    epitroclea_izq: bool
    olecranon_izq: bool
    musculo_epicondilio_izq: bool
    musculo_epitroclea_izq: bool
    epicondilitis_der_presente: bool
    epicondilitis_der_ausente: bool
    parestesia_der: bool
    gravedad_codo_der: str
    epicondilitis_izq_presente: bool
    epicondilitis_izq_ausente: bool
    parestesia_izq: bool
    gravedad_codo_izq: str
    observaciones_codo: str
    
    # MUÑECA
    muneca_dx_desde: str
    muneca_ix_desde: str
    quiste_dorsal_der: bool
    quiste_ventral_der: bool
    edema_dorsal_der: bool
    edema_ventral_der: bool
    edema_estiloide_radial_der: bool
    edema_estiloide_ulnar_der: bool
    hipotrofia_der: bool
    deformidades_der: bool
    quiste_dorsal_izq: bool
    quiste_ventral_izq: bool
    edema_dorsal_izq: bool
    edema_ventral_izq: bool
    edema_estiloide_radial_izq: bool
    edema_estiloide_ulnar_izq: bool
    hipotrofia_izq: bool
    deformidades_izq: bool
    trapecio_dx: bool
    trapecio_ix: bool
    estiloide_radial_dx: bool
    estiloide_radial_ix: bool
    clic_dx: bool
    clic_ix: bool
    finkelsten_der: bool
    cr_der: bool
    mp_der: bool
    cr_resistencia_der: bool
    dolor_extension_der: bool
    finkelsten_izq: bool
    cr_izq: bool
    mp_izq: bool
    cr_resistencia_izq: bool
    dolor_extension_izq: bool
    sintomatologia_si: bool
    sintomatologia_no: bool
    apofisis_espinoza: str
    trapecio_sup: str
    paravertebral: str
    flexion_muneca: str
    extension_muneca: str
    fatiga1_derecha: str
    fatiga2_derecha: str
    fatiga1_izquierda: str
    fatiga2_izquierda: str
    phalen_mediano_der: bool
    phalen_cubital_der: bool
    phalen_noterr_der: bool
    presion_mediano_der: bool
    presion_cubital_der: bool
    presion_noterr_der: bool
    phalen_mediano_izq: bool
    phalen_cubital_izq: bool
    phalen_noterr_izq: bool
    presion_mediano_izq: bool
    presion_cubital_izq: bool
    presion_noterr_izq: bool
    grado_codo_der: str
    grado_codo_izq: str
    observaciones_muneca: str
    
    # COLUMNA Y FINAL
    cervical_desde: str
    dorsal_desde: str
    lumbar_desde: str
    conclusiones_diagnostica: str
    gravedad_cuadro: str
    concepto_aptitud: str
    observaciones_final: str
    restricciones: str
    fecha_firma: str
