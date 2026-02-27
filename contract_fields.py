"""
Definición de campos para cada tipo de contrato.
Cada campo tiene: key, label, tipo (text/date/number/select/textarea), placeholder, y si es requerido.
"""

SERVICIOS_FIELDS = [
    # --- Datos del Prestador ---
    {"section": "Datos del Prestador de Servicios"},
    {"key": "prestador_nombre", "label": "Nombre completo del prestador", "type": "text", "placeholder": "Juan Pérez López", "required": True},
    {"key": "prestador_nacionalidad", "label": "Nacionalidad", "type": "text", "placeholder": "Mexicana", "required": True},
    {"key": "prestador_edad", "label": "Edad", "type": "number", "placeholder": "35", "required": True},
    {"key": "prestador_estado_civil", "label": "Estado civil", "type": "select", "options": ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Unión libre"], "required": True},
    {"key": "prestador_sexo", "label": "Sexo", "type": "select", "options": ["Masculino", "Femenino"], "required": True},
    {"key": "prestador_domicilio", "label": "Domicilio del prestador", "type": "text", "placeholder": "Calle, número, colonia, ciudad, estado, C.P.", "required": True},

    # --- Datos del Cliente ---
    {"section": "Datos del Cliente (Empresa)"},
    {"key": "cliente_tipo_sociedad", "label": "Tipo de sociedad", "type": "text", "placeholder": "Sociedad Anónima de Capital Variable", "required": True},
    {"key": "cliente_escritura_numero", "label": "Número de escritura pública", "type": "text", "placeholder": "12345", "required": True},
    {"key": "cliente_escritura_fecha", "label": "Fecha de escritura (día/mes/año)", "type": "text", "placeholder": "15 de marzo de 2020", "required": True},
    {"key": "cliente_notario_nombre", "label": "Nombre del notario", "type": "text", "placeholder": "Lic. Roberto García", "required": True},
    {"key": "cliente_notario_numero", "label": "Número de notaría", "type": "text", "placeholder": "55", "required": True},
    {"key": "cliente_folio_mercantil", "label": "Folio mercantil", "type": "text", "placeholder": "2023010001", "required": False},
    {"key": "cliente_folio_fecha", "label": "Fecha de inscripción del folio", "type": "text", "placeholder": "20 de abril de 2020", "required": False},
    {"key": "cliente_representante", "label": "Nombre del representante legal", "type": "text", "placeholder": "María González Ruiz", "required": True},
    {"key": "cliente_objeto_social", "label": "Objeto social de la empresa", "type": "textarea", "placeholder": "Desarrollo de software y consultoría tecnológica", "required": True},
    {"key": "cliente_rfc", "label": "RFC de la empresa", "type": "text", "placeholder": "ABC123456XY0", "required": True},
    {"key": "cliente_domicilio", "label": "Domicilio fiscal del cliente", "type": "text", "placeholder": "Av. Reforma 100, Col. Centro, CDMX, C.P. 06000", "required": True},

    # --- Giro y actividades del cliente (para adaptar cláusulas) ---
    {"section": "Giro y Actividades del Cliente"},
    {"key": "cliente_giro", "label": "Giro o industria del cliente", "type": "text", "placeholder": "Ej: Tecnología, Restaurantes, Consultoría, Comercio electrónico...", "required": True},
    {"key": "cliente_actividades", "label": "Actividades principales del cliente (para cláusula de no competencia)", "type": "textarea", "placeholder": "Ej:\n- Desarrollo y venta de software de contabilidad\n- Consultoría fiscal para PyMEs\n- Operación de plataforma digital de facturación", "required": True},

    # --- Datos del Contrato ---
    {"section": "Términos del Contrato"},
    {"key": "servicios_descripcion", "label": "Descripción de los servicios a prestar", "type": "textarea", "placeholder": "Desarrollo de aplicaciones web, consultoría en arquitectura de software...", "required": True},
    {"key": "honorarios_moneda", "label": "Moneda de pago", "type": "select", "options": ["MXN (Pesos mexicanos)", "USD (Dólares americanos)"], "required": True},
    {"key": "honorarios_monto", "label": "Monto mensual de honorarios", "type": "text", "placeholder": "25,000.00", "required": True},
    {"key": "honorarios_monto_letra", "label": "Monto en letra", "type": "text", "placeholder": "Veinticinco mil pesos", "required": True},
    {"key": "cuenta_bancaria", "label": "Datos de cuenta bancaria para pago", "type": "textarea", "placeholder": "Banco: BBVA\nCLABE: 012345678901234567\nCuenta: 1234567890", "required": True},
    {"key": "fecha_inicio", "label": "Fecha de inicio del contrato", "type": "text", "placeholder": "1 de marzo de 2026", "required": True},
    {"key": "fecha_firma", "label": "Fecha de firma del contrato", "type": "text", "placeholder": "26 de febrero de 2026", "required": True},
]

ARRENDAMIENTO_FIELDS = [
    # --- Datos del Arrendador ---
    {"section": "Datos del Arrendador"},
    {"key": "arrendador_nombre", "label": "Nombre completo del arrendador", "type": "text", "placeholder": "José Martínez Hernández", "required": True},
    {"key": "arrendador_nacionalidad", "label": "Nacionalidad", "type": "text", "placeholder": "Mexicano", "required": True},
    {"key": "arrendador_estado_civil", "label": "Estado civil", "type": "select", "options": ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Unión libre"], "required": True},
    {"key": "arrendador_identificacion", "label": "Número de folio INE", "type": "text", "placeholder": "1234567890123", "required": True},
    {"key": "arrendador_rfc", "label": "RFC del arrendador", "type": "text", "placeholder": "MAHJ800101AB1", "required": True},
    {"key": "arrendador_representante", "label": "Representante legal (si aplica)", "type": "text", "placeholder": "Dejar vacío si firma directamente", "required": False},

    # --- Datos del Inmueble ---
    {"section": "Datos del Inmueble"},
    {"key": "inmueble_descripcion", "label": "Descripción del inmueble/tierras", "type": "textarea", "placeholder": "Tierras denominadas 'El Rancho', ubicadas en...", "required": True},
    {"key": "inmueble_ubicacion", "label": "Ubicación (municipio, estado)", "type": "text", "placeholder": "Municipio de Juchitán, Oaxaca", "required": True},
    {"key": "inmueble_superficie", "label": "Superficie total (hectáreas)", "type": "text", "placeholder": "150", "required": True},
    {"key": "inmueble_escritura", "label": "Número de escritura pública del inmueble", "type": "text", "placeholder": "56789", "required": True},
    {"key": "inmueble_notario", "label": "Notario y número de notaría", "type": "text", "placeholder": "Lic. Carlos López, Notaría 12, Ciudad de Oaxaca", "required": True},
    {"key": "inmueble_folio", "label": "Folio mercantil/registral", "type": "text", "placeholder": "2020030045", "required": False},
    {"key": "inmueble_linderos", "label": "Linderos y colindancias", "type": "textarea", "placeholder": "Norte: 200m, colinda con...\nSur: 180m, colinda con...", "required": True},

    # --- Datos de la Empresa (Arrendataria) ---
    {"section": "Datos de la Empresa Arrendataria"},
    {"key": "empresa_nombre", "label": "Razón social de la empresa", "type": "text", "placeholder": "Ej: Distribuidora del Norte S.A. de C.V.", "required": True},
    {"key": "empresa_escritura", "label": "Número de escritura constitutiva", "type": "text", "placeholder": "98765", "required": True},
    {"key": "empresa_notario", "label": "Notario y número de notaría", "type": "text", "placeholder": "Lic. Ana Ruiz, Notaría 8, CDMX", "required": True},
    {"key": "empresa_folio", "label": "Folio mercantil", "type": "text", "placeholder": "2021050078", "required": False},
    {"key": "empresa_rfc", "label": "RFC de la empresa", "type": "text", "placeholder": "DNO210501XY3", "required": True},
    {"key": "empresa_representante", "label": "Representante legal", "type": "text", "placeholder": "Lic. Laura Méndez", "required": True},
    {"key": "empresa_objeto", "label": "Objeto social / giro de la empresa", "type": "textarea", "placeholder": "Ej: Almacenamiento y distribución de productos agrícolas, operación de bodega comercial, restaurante, taller mecánico...", "required": True},

    # --- Uso y proyecto ---
    {"section": "Uso del Inmueble y Proyecto"},
    {"key": "uso_inmueble", "label": "Uso que se le dará al inmueble", "type": "textarea", "placeholder": "Ej: Instalación de bodega para almacenamiento de mercancía, oficinas administrativas, local comercial, taller de producción...", "required": True},
    {"key": "infraestructura", "label": "Infraestructura o instalaciones que se construirán/instalarán (si aplica)", "type": "textarea", "placeholder": "Ej: Bodega de 500m², estacionamiento, oficina administrativa. Dejar vacío si se usará tal cual.", "required": False},
    {"key": "superficie_estimada", "label": "Superficie a ocupar", "type": "text", "placeholder": "Ej: 500 m², 2 hectáreas, todo el inmueble", "required": True},

    # --- Términos del Contrato ---
    {"section": "Términos del Arrendamiento"},
    {"key": "vigencia_anos", "label": "Vigencia inicial (años)", "type": "number", "placeholder": "5", "required": True},
    {"key": "vigencia_adicional", "label": "Periodos de renovación (si aplica)", "type": "text", "placeholder": "Ej: 2 periodos adicionales de 3 años cada uno", "required": False},
    {"key": "renta_monto", "label": "Monto de renta mensual", "type": "text", "placeholder": "$15,000.00 MXN mensuales", "required": True},
    {"key": "renta_moneda", "label": "Moneda", "type": "select", "options": ["MXN (Pesos mexicanos)", "USD (Dólares americanos)"], "required": True},
    {"key": "deposito_garantia", "label": "Depósito en garantía (si aplica)", "type": "text", "placeholder": "Ej: Equivalente a 2 meses de renta", "required": False},
    {"key": "fecha_firma", "label": "Fecha de firma", "type": "text", "placeholder": "26 de febrero de 2026", "required": True},
]
