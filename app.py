import streamlit as st
import pandas as pd
import database

# Configuração da página inicial do Streamlit
st.set_page_config(page_title="SaaS Marketing - Multicliente", page_icon="🚀", layout="wide")

# Inicializa o banco de dados
supabase = database.iniciar_conexao()

# SIMULAÇÃO DE LOGIN: Tenant fixo para a operação piloto da sua drogaria
TENANT_ID_TESTE = "123e4567-e89b-12d3-a456-426614174000" 

# --- MENU LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/5332/5332219.png", width=100) # Ícone genérico
st.sidebar.title("🚀 Painel de Automação")
st.sidebar.markdown("---")

pagina_selecionada = st.sidebar.radio(
    "Navegação:",
    ["⚙️ Configurações de API", "📁 Upload de Contatos", "⚡ Central de Disparos"]
)

# ==========================================
# TELA 1: CONFIGURAÇÕES DE API
# ==========================================
if pagina_selecionada == "⚙️ Configurações de API":
    st.title("⚙️ Configuração de Credenciais")
    st.markdown("Insira aqui os tokens da Meta e de E-mail exclusivos da sua operação. Esses dados ficam isolados no seu Tenant.")

    # Busca no banco para ver se o cliente já tem algo salvo
    dados_atuais = database.buscar_credenciais(supabase, TENANT_ID_TESTE)
    
    if not dados_atuais:
        dados_atuais = {
            "nome_empresa": "Drogfar (Piloto)", "whatsapp_token": "", 
            "phone_number_id": "", "waba_id": "", "email_api_key": ""
        }

    with st.form("form_credenciais"):
        st.subheader("🤖 WhatsApp Business Cloud API")
        nome_empresa = st.text_input("Nome do Estabelecimento", value=dados_atuais.get("nome_empresa", ""))
        wp_token = st.text_input("Permanent System User Token (Meta)", type="password", value=dados_atuais.get("whatsapp_token", ""))
        phone_id = st.text_input("Phone Number ID", value=dados_atuais.get("phone_number_id", ""))
        waba_id = st.text_input("WABA ID (WhatsApp Business Account)", value=dados_atuais.get("waba_id", ""))
        
        st.subheader("📧 E-mail Marketing")
        email_key = st.text_input("Chave da API (SendGrid/Resend)", type="password", value=dados_atuais.get("email_api_key", ""))

        submit_btn = st.form_submit_button("Salvar Cofre de Credenciais")

        if submit_btn:
            if wp_token and phone_id and waba_id:
                try:
                    database.salvar_credenciais(
                        supabase, TENANT_ID_TESTE, nome_empresa, wp_token, phone_id, waba_id, email_key
                    )
                    st.success("✅ Credenciais salvas com sucesso no banco de dados isolado!")
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
            else:
                st.warning("⚠️ Preencha pelo menos os 3 campos obrigatórios da Meta (WhatsApp).")

# ==========================================
# TELA 2: UPLOAD E BASE DE CONTATOS
# ==========================================
elif pagina_selecionada == "📁 Upload de Contatos":
    st.title("📁 Gestão de Leads e Contatos")
    st.markdown("Faça o upload da sua lista de clientes para alimentar a régua de relacionamento.")

    arquivo_csv = st.file_uploader("Arraste seu arquivo CSV aqui", type=["csv"])
    
    if arquivo_csv is not None:
        try:
            # Lê o CSV usando a biblioteca Pandas
            df = pd.read_csv(arquivo_csv)
            
            st.success(f"Arquivo carregado! Foram encontrados {len(df)} contatos.")
            st.write("Pré-visualização dos dados:")
            st.dataframe(df.head(10), use_container_width=True) # Mostra as 10 primeiras linhas
            
            # Validação simples de colunas
            colunas_esperadas = ['nome', 'telefone', 'email']
            if all(col in df.columns for col in colunas_esperadas):
                if st.button("Gravar contatos no Banco de Dados"):
                    st.info("Aqui entrará a função do database.py para salvar os leads no Supabase vinculados ao seu Tenant.")
            else:
                st.error(f"O CSV precisa ter as colunas básicas: {', '.join(colunas_esperadas)}")
                
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

# ==========================================
# TELA 3: CENTRAL DE DISPAROS
# ==========================================
elif pagina_selecionada == "⚡ Central de Disparos":
    st.title("⚡ Automação e Disparos")
    st.markdown("Agende ou dispare mensagens em massa usando templates pré-aprovados da Meta.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Configurar Campanha")
        tipo_disparo = st.selectbox("Canal de Disparo", ["WhatsApp", "E-mail", "Ambos (Régua)"])
        
        template_selecionado = st.selectbox(
            "Selecione o Template (Aprovado na Meta)", 
            ["lembrete_recompra_vitaminas", "oferta_fim_de_semana", "carrinho_abandonado", "boas_vindas"]
        )
        
        # Simulação de variáveis dependendo do template
        if template_selecionado == "lembrete_recompra_vitaminas":
            st.info("Variáveis deste template: {{1}} Nome, {{2}} Produto")
            
    with col2:
        st.subheader("Pré-visualização")
        st.markdown(f"""
        <div style="padding: 15px; border-radius: 10px; background-color: #e5ddd5; color: #000; font-family: sans-serif; max-width: 300px;">
            Olá <b>[Nome do Cliente]</b>! Vimos que seu <b>[Produto]</b> deve estar acabando. Quer aproveitar nosso cupom de 10% para renovar o estoque de saúde na farmácia hoje?
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    if st.button("🚀 Iniciar Disparo em Massa", type="primary"):
        st.warning("O motor de disparo `whatsapp_api.py` será conectado aqui em breve para processar a fila!")
