"""
Tu Abogado de Bolsillo - Generador de Contratos para PyMEs en México
Aplicación Streamlit + OpenAI
"""

import os
import streamlit as st
from datetime import datetime
from contract_fields import SERVICIOS_FIELDS, ARRENDAMIENTO_FIELDS
from agent import generate_contract, review_contract
from export import contract_to_docx, contract_to_pdf

# --- Configuración de página ---
st.set_page_config(
    page_title="Tu Abogado de Bolsillo",
    page_icon="⚖️",
    layout="wide",
)

# --- CSS personalizado ---
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .contract-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        transition: border-color 0.3s;
    }
    .contract-card:hover {
        border-color: #1f77b4;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Inicializa el estado de la sesión."""
    defaults = {
        "step": "select",       # select -> fill -> review -> chat
        "contract_type": None,
        "form_data": {},
        "generated_contract": None,
        "chat_history": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def render_header():
    """Renderiza el header de la app."""
    st.markdown("<div class='main-header'>", unsafe_allow_html=True)
    st.title("⚖️ Tu Abogado de Bolsillo")
    st.caption("Generador inteligente de contratos para PyMEs en México")
    st.markdown("</div>", unsafe_allow_html=True)


def render_contract_selection():
    """Paso 1: Selección de tipo de contrato."""
    st.header("Paso 1: Selecciona el tipo de contrato")
    st.write("Elige el contrato que necesitas generar:")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Prestación de Servicios Independientes")
        st.write(
            "Para contratar freelancers, consultores o prestadores de servicios "
            "independientes. Incluye cláusulas de confidencialidad, no competencia, "
            "propiedad intelectual y cumplimiento legal."
        )
        if st.button("Seleccionar Servicios", key="btn_servicios", use_container_width=True):
            st.session_state.contract_type = "servicios"
            st.session_state.step = "fill"
            st.rerun()

    with col2:
        st.subheader("Contrato de Arrendamiento")
        st.write(
            "Para arrendar inmuebles, locales o terrenos. Incluye cláusulas de "
            "vigencia, uso permitido, obligaciones de las partes, depósito en "
            "garantía y condiciones de terminación."
        )
        if st.button("Seleccionar Arrendamiento", key="btn_arrendamiento", use_container_width=True):
            st.session_state.contract_type = "arrendamiento"
            st.session_state.step = "fill"
            st.rerun()


def render_form_field(field: dict) -> str | None:
    """Renderiza un campo del formulario y retorna el valor."""
    key = field["key"]
    label = field["label"]
    required = field.get("required", False)
    display_label = f"{label} *" if required else label
    placeholder = field.get("placeholder", "")

    # Recuperar valor previo si existe
    prev_value = st.session_state.form_data.get(key, "")

    field_type = field["type"]
    if field_type == "text":
        return st.text_input(display_label, value=prev_value, placeholder=placeholder, key=f"field_{key}")
    elif field_type == "textarea":
        return st.text_area(display_label, value=prev_value, placeholder=placeholder, key=f"field_{key}")
    elif field_type == "number":
        default = int(prev_value) if prev_value else 0
        return str(st.number_input(display_label, min_value=0, value=default, key=f"field_{key}"))
    elif field_type == "select":
        options = field.get("options", [])
        idx = 0
        if prev_value in options:
            idx = options.index(prev_value)
        return st.selectbox(display_label, options=options, index=idx, key=f"field_{key}")
    elif field_type == "date":
        return str(st.date_input(display_label, key=f"field_{key}"))
    return None


def render_form():
    """Paso 2: Formulario para llenar datos del contrato."""
    contract_type = st.session_state.contract_type
    type_names = {
        "servicios": "Prestación de Servicios Independientes",
        "arrendamiento": "Arrendamiento",
    }

    st.header(f"Paso 2: Datos del contrato de {type_names[contract_type]}")

    if st.button("← Cambiar tipo de contrato"):
        st.session_state.step = "select"
        st.session_state.contract_type = None
        st.session_state.form_data = {}
        st.rerun()

    fields = SERVICIOS_FIELDS if contract_type == "servicios" else ARRENDAMIENTO_FIELDS

    # Renderizar campos por sección
    form_data = {}
    current_section = None

    for field in fields:
        if "section" in field:
            current_section = field["section"]
            st.subheader(current_section)
            continue

        value = render_form_field(field)
        if value:
            form_data[field["key"]] = value

    st.divider()

    # Instrucciones especiales
    special = st.text_area(
        "Instrucciones especiales (opcional)",
        placeholder="Ejemplo: Agregar una cláusula de penalización por retraso en pagos...",
        key="special_instructions",
    )

    # Validación
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Generar Contrato", type="primary", use_container_width=True):
            # Verificar campos requeridos
            missing = []
            for field in fields:
                if "section" in field:
                    continue
                if field.get("required") and not form_data.get(field["key"]):
                    missing.append(field["label"])

            if missing:
                st.error(f"Faltan campos obligatorios: {', '.join(missing[:5])}")
            else:
                st.session_state.form_data = form_data
                st.session_state.special_instructions = special
                st.session_state.step = "review"
                st.rerun()


def render_review():
    """Paso 3: Generación y revisión del contrato."""
    st.header("Paso 3: Tu contrato generado")

    if st.button("← Volver al formulario"):
        st.session_state.step = "fill"
        st.session_state.generated_contract = None
        st.rerun()

    # Generar contrato si no existe
    if not st.session_state.generated_contract:
        api_key = st.session_state.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error(
                "Ingresa tu API key de OpenAI en la barra lateral para generar el contrato."
            )
            return

        with st.spinner("Generando tu contrato... Esto puede tomar un momento."):
            try:
                contract = generate_contract(
                    st.session_state.contract_type,
                    st.session_state.form_data,
                    st.session_state.get("special_instructions", ""),
                    api_key=api_key,
                )
                st.session_state.generated_contract = contract
            except Exception as e:
                st.error(f"Error al generar el contrato: {e}")
                return

    # Mostrar contrato
    contract_text = st.session_state.generated_contract
    st.text_area("Contrato generado", value=contract_text, height=600, key="contract_display")

    # Botones de descarga
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_name = f"contrato_{st.session_state.contract_type}_{timestamp}"

    st.subheader("Descargar contrato")
    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        docx_bytes = contract_to_docx(contract_text)
        st.download_button(
            "Descargar Word (.docx)",
            data=docx_bytes,
            file_name=f"{base_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

    with col_d2:
        pdf_bytes = contract_to_pdf(contract_text)
        st.download_button(
            "Descargar PDF",
            data=pdf_bytes,
            file_name=f"{base_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with col_d3:
        st.download_button(
            "Descargar texto (.txt)",
            data=contract_text,
            file_name=f"{base_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # Botones de acción
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Regenerar contrato", use_container_width=True):
            st.session_state.generated_contract = None
            st.rerun()

    with col2:
        if st.button("Modificar / Preguntar al agente", use_container_width=True):
            st.session_state.step = "chat"
            st.rerun()


def render_chat():
    """Paso 4: Chat con el agente para modificaciones."""
    st.header("Paso 4: Consulta con tu Abogado de Bolsillo")

    if st.button("← Volver al contrato"):
        st.session_state.step = "review"
        st.rerun()

    st.info(
        "Puedes hacer preguntas sobre el contrato o pedir modificaciones. "
        "Por ejemplo: 'Cambia la cláusula de vigencia a 2 años' o "
        "'¿Qué significa la cláusula de no competencia?'"
    )

    # Mostrar historial
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input del usuario
    user_input = st.chat_input("Escribe tu pregunta o solicitud de cambio...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                try:
                    api_key = st.session_state.get("api_key") or os.getenv("OPENAI_API_KEY")
                    response = review_contract(
                        st.session_state.generated_contract,
                        user_input,
                        api_key=api_key,
                    )
                    st.write(response)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response}
                    )

                    # Si la respuesta parece ser un contrato modificado, actualizarlo
                    if len(response) > 2000 and "CONTRATO" in response.upper():
                        st.session_state.generated_contract = response
                        st.success("El contrato ha sido actualizado con los cambios.")
                except Exception as e:
                    st.error(f"Error: {e}")


def render_sidebar():
    """Renderiza la barra lateral con información y progreso."""
    with st.sidebar:
        st.header("⚖️ Tu Abogado de Bolsillo")
        st.caption("v1.0 - Boceto inicial")

        st.divider()

        # API Key input
        api_key_input = st.text_input(
            "API Key de OpenAI",
            type="password",
            placeholder="sk-...",
            value=st.session_state.get("api_key", ""),
            help="Tu key no se almacena. Solo se usa durante esta sesión.",
        )
        if api_key_input:
            st.session_state.api_key = api_key_input

        st.divider()

        # Indicador de progreso
        steps = {
            "select": ("Seleccionar contrato", 1),
            "fill": ("Llenar datos", 2),
            "review": ("Revisar contrato", 3),
            "chat": ("Consultar agente", 4),
        }
        current_step = st.session_state.step
        current_num = steps[current_step][1]

        st.subheader("Progreso")
        for step_key, (step_name, step_num) in steps.items():
            if step_num < current_num:
                st.write(f"~~{step_num}. {step_name}~~")
            elif step_num == current_num:
                st.write(f"**→ {step_num}. {step_name}**")
            else:
                st.write(f"{step_num}. {step_name}")

        st.divider()

        if st.session_state.contract_type:
            tipo = "Servicios Independientes" if st.session_state.contract_type == "servicios" else "Arrendamiento"
            st.write(f"**Contrato:** {tipo}")

        st.divider()
        st.caption(
            "Este es un asistente para generar borradores de contratos. "
            "Siempre consulta con un abogado antes de firmar cualquier documento legal."
        )


# --- Main ---
def main():
    init_session_state()
    render_header()
    render_sidebar()

    if st.session_state.step == "select":
        render_contract_selection()
    elif st.session_state.step == "fill":
        render_form()
    elif st.session_state.step == "review":
        render_review()
    elif st.session_state.step == "chat":
        render_chat()


if __name__ == "__main__":
    main()
