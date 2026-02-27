"""
Agente OpenAI para generación de contratos legales mexicanos.
Toma la plantilla base + datos del usuario y genera el contrato personalizado.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def _get_client(api_key: str | None = None) -> OpenAI:
    """Crea un cliente OpenAI con la key proporcionada o la del entorno."""
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("No se proporcionó una API key de OpenAI.")
    return OpenAI(api_key=key)

SYSTEM_PROMPT = """Eres un asistente legal especializado en derecho mexicano para PyMEs.
Tu trabajo es tomar una PLANTILLA BASE de contrato y los datos proporcionados por el usuario
para generar un contrato ADAPTADO a su situación específica, profesional y listo para firma.

IMPORTANTE: La plantilla base fue redactada para un negocio específico (ej. empresa de bienestar,
proyecto de energía solar). Tu trabajo NO es solo rellenar huecos, sino ADAPTAR el contenido
al giro y contexto real del usuario.

REGLAS DE ADAPTACIÓN:
1. Reemplaza TODOS los placeholders [*], [_], ___ con los datos proporcionados.
2. Si un dato no fue proporcionado, déjalo como "[POR DEFINIR]".
3. ADAPTA las cláusulas sustantivas al giro del negocio del usuario:
   - Cláusula de NO COMPETENCIA: reescríbela describiendo las actividades REALES del cliente
     (no las del machote original). Usa el objeto social y giro proporcionados.
   - Cláusula de OBJETO: adáptala a los servicios o uso reales que el usuario necesita.
   - Cláusula de CONTRAPRESTACIÓN: usa la moneda correcta (MXN o USD según indique el usuario).
   - Para arrendamiento: adapta el uso del inmueble al proyecto real del usuario
     (no asumas que es energía solar/eólica a menos que el usuario lo indique).
   - Infraestructura y equipamiento: describe lo que aplique al giro real, no lo del machote.
4. MANTÉN intactas las cláusulas de forma/procedimiento que son genéricas:
   - Confidencialidad (estructura general)
   - Notificaciones
   - Legislación y jurisdicción
   - Datos personales (LFPDPPP)
   - Cumplimiento legal / anti-corrupción / anti-lavado
   - Propiedad intelectual (estructura general)
   - Indemnización (estructura general)
5. NO inventes datos fácticos (nombres, fechas, montos, RFC, escrituras, etc.).
6. Adapta género gramatical cuando sea necesario.
7. Fechas y montos deben aparecer en número y letra cuando el contrato lo requiera.
8. Si el usuario pide cláusulas nuevas o eliminar alguna, hazlo.

FORMATO DE SALIDA:
- Contrato completo en texto plano con formato limpio.
- Saltos de línea entre cláusulas.
- Numeración y formato consistente con el estilo del original.
"""


def load_template(contract_type: str) -> str:
    """Carga la plantilla de contrato desde archivo."""
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    if contract_type == "servicios":
        path = os.path.join(templates_dir, "servicios_raw.txt")
    elif contract_type == "arrendamiento":
        path = os.path.join(templates_dir, "arrendamiento_raw.txt")
    else:
        raise ValueError(f"Tipo de contrato no soportado: {contract_type}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def format_user_data(data: dict) -> str:
    """Formatea los datos del usuario para el prompt."""
    lines = []
    for key, value in data.items():
        if value:
            label = key.replace("_", " ").title()
            lines.append(f"- {label}: {value}")
    return "\n".join(lines)


def generate_contract(contract_type: str, user_data: dict, special_instructions: str = "", api_key: str | None = None) -> str:
    """
    Genera un contrato personalizado usando OpenAI.

    Args:
        contract_type: "servicios" o "arrendamiento"
        user_data: Diccionario con los datos del formulario
        special_instructions: Instrucciones adicionales del usuario
        api_key: API key de OpenAI (si no se pasa, usa la del entorno)

    Returns:
        Texto del contrato generado
    """
    client = _get_client(api_key)
    template = load_template(contract_type)
    formatted_data = format_user_data(user_data)

    tipo_nombre = {
        "servicios": "Prestación de Servicios Independientes",
        "arrendamiento": "Arrendamiento",
    }

    user_message = f"""Genera el contrato de {tipo_nombre[contract_type]} usando la siguiente información:

DATOS DEL USUARIO:
{formatted_data}

PLANTILLA BASE DEL CONTRATO:
{template}

{f"INSTRUCCIONES ADICIONALES: {special_instructions}" if special_instructions else ""}

Por favor genera el contrato completo con todos los datos reemplazados correctamente."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,
        max_tokens=16000,
    )

    return response.choices[0].message.content


def review_contract(contract_text: str, question: str, api_key: str | None = None) -> str:
    """
    Permite al usuario hacer preguntas o pedir modificaciones sobre el contrato generado.

    Args:
        contract_text: El contrato generado
        question: Pregunta o instrucción del usuario
        api_key: API key de OpenAI (si no se pasa, usa la del entorno)

    Returns:
        Respuesta del agente o contrato modificado
    """
    client = _get_client(api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""Aquí está el contrato generado:

{contract_text}

El usuario tiene la siguiente pregunta o solicitud de modificación:
{question}

Si es una pregunta, responde de forma clara y concisa.
Si es una solicitud de modificación, devuelve el contrato completo con los cambios aplicados.
Indica claramente qué cambios realizaste.""",
            },
        ],
        temperature=0.1,
        max_tokens=16000,
    )

    return response.choices[0].message.content
