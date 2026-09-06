import streamlit as st
import database

# Configuração da página inicial do Streamlit
st.set_page_config(page_title="SaaS Marketing - Multicliente", page_icon="🚀", layout="wide")

# Inicializa o banco de dados
supabase = database.iniciar_conexao()

# SIMULAÇÃO DE LOGIN: Como ainda não temos tela de login, vamos fixar um ID 
# para representar a Drogfar como o "Cliente Zero" operando o sistema.
TENANT_ID_TESTE = "123e4567-e89b-12d3-a456-426614174000" # UUID de exemplo

# --- MENU LATERAL ---
st.sidebar.title("🚀 Menu de Navegação")
pagina_selecionada = st.sidebar.radio(
    "Ir para:",
    ["Configurações de API", "Upload de Contatos (Em breve)", "Disparos (Em breve)"]
)

# --- TELA: CONFIGURAÇÕES DE API ---
if pagina_selecionada == "Configurações de API":
    st.title("⚙️ Configuração de Credenciais")
    st.markdown("Insira aqui os tokens da Meta e de E-mail exclusivos da sua operação.")

    # Busca no banco para ver se o cliente já tem algo salvo
    dados_atuais = database.buscar_credenciais(supabase, TENANT_ID_TESTE)
    
    # Se não tiver dados, inicia vazio
    if not dados_atuais:
        dados_atuais = {
            "nome_empresa": "Minha Farmácia", "whatsapp_token": "", 
            "phone_number_id": "", "waba_id": "", "email_api_key": ""
        }

    # Formulário de entrada de dados
    with st.form("form_credenciais"):
        st.subheader("🤖 WhatsApp Business Cloud API")
        nome_empresa = st.text_input("Nome do Estabelecimento", value=dados_atuais.get("nome_empresa", ""))
        wp_token = st.text_input("Permanent System User Token (Meta)", type="password", value=dados_atuais.get("whatsapp_token", ""))
        phone_id = st.text_input("Phone Number ID", value=dados_atuais.get("phone_number_id", ""))
        waba_id = st.text_input("WABA ID (WhatsApp Business Account)", value=dados_atuais.get("waba_id", ""))
        
        st.subheader("📧 E-mail Marketing")
        email_key = st.text_input("Chave da API (SendGrid/Resend)", type="password", value=dados_atuais.get("email_api_key", ""))

        submit_btn = st.form_submit_button("Salvar Credenciais")

        if submit_btn:
            if wp_token and phone_id and waba_id:
                try:
                    # Envia os dados para o Supabase
                    database.salvar_credenciais(
                        supabase, TENANT_ID_TESTE, nome_empresa, wp_token, phone_id, waba_id, email_key
                    )
                    st.success("✅ Credenciais salvas com sucesso no seu cofre blindado!")
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
            else:
                st.warning("⚠️ Preencha pelo menos os 3 campos obrigatórios do WhatsApp.")
