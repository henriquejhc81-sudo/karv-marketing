import streamlit as st
from supabase import create_client, Client

# Função para conectar ao Supabase (O cache evita que reconecte a toda hora)
@st.cache_resource
def iniciar_conexao() -> Client:
    # As chaves virão de um arquivo oculto de segurança (secrets)
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# Função para salvar ou atualizar as credenciais do cliente (Farmácia/SaaS)
def salvar_credenciais(supabase: Client, tenant_id: str, nome_empresa: str, 
                       wp_token: str, phone_id: str, waba_id: str, email_key: str):
    
    dados = {
        "id": tenant_id, # Usando o ID fixo, ele atualiza (upsert) se já existir
        "nome_empresa": nome_empresa,
        "whatsapp_token": wp_token,
        "phone_number_id": phone_id,
        "waba_id": waba_id,
        "email_api_key": email_key
    }
    
    # Envia para a tabela 'clientes_saas'
    resposta = supabase.table("clientes_saas").upsert(dados).execute()
    return resposta

# Função para buscar as credenciais atuais para preencher a tela
def buscar_credenciais(supabase: Client, tenant_id: str):
    resposta = supabase.table("clientes_saas").select("*").eq("id", tenant_id).execute()
    if resposta.data:
        return resposta.data[0] # Retorna os dados do primeiro cliente encontrado
    return None
