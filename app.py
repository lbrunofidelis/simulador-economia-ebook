import streamlit as st

st.set_page_config(
    page_title="Simulador de economia financeira com E-book",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="💵"
)

st.title("Simulador de economia financeira com E-book")

st.markdown("""
<style>
    footer {
        visibility: hidden;
    }
    .custom-footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background-color: #f0f2f6;
        font-size: 0.8rem;
        color: #555;
        border-top: 1px solid #ddd;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #FFF;
        color: black;
        font-weight: bold;
        width: 200px;
        font-size: 160%;
    }
    .botao {
        display: flex;
        justify-content: center;
        flex-direction: row;
    }
    div.row-widget.stButton {
        text-align: center;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #000;
        color: white;
        border-color: #000;
    }
    .economia-title {
        font-size: 150%;
        font-weight: bold;
    }
    .economia {
        color: #30FF90;
        font-size: 130%;
        font-weight: bold;
    }
    .perda {
        color: #FF6060;
        font-size: 130%;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def formata_input_dinheiro(input_value):
    limpo = ''.join(c for c in input_value if c.isdigit() or c in [',', '.'])
    
    try:
        if ',' in limpo:
            limpo = limpo.replace('.', '').replace(',', '.')
        
        valor = float(limpo)
        
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ "

def formata_input_numerico(input_value):
    limpo = ''.join(c for c in input_value if c.isdigit())
    
    try:
        value = int(limpo)
        return f"{value:,}".replace(',', '.')
    except (ValueError, TypeError):
        return ""

def formata_dinheiro(value):
    if value is None:
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mensalidade_key = "mensalidade"
        
        valor_atual = st.session_state.get(mensalidade_key, "")
        
        if valor_atual and isinstance(valor_atual, str) and valor_atual.strip() != "":
            valor_atual = formata_input_dinheiro(valor_atual)
        
        mensalidade_dinheiro = st.text_input(
            "Mensalidade (R$)",
            value=valor_atual,
            key=mensalidade_key,
            placeholder="R$"
        )
        
        try:
            clean_value = mensalidade_dinheiro.replace("R$", "").replace(".", "").replace(",", ".").strip()
            if clean_value:
                mensalidade = float(clean_value)
            else:
                mensalidade = None
        except ValueError:
            mensalidade = None
    
    with col2:
        contratos_key = "qtd_contratos"
        
        valor_atual = st.session_state.get(contratos_key, "")
        
        if valor_atual and isinstance(valor_atual, str) and valor_atual.strip() != "":
            valor_atual = formata_input_numerico(valor_atual)
        
        qtd_contratos_formatado = st.text_input(
            "Quantidade de contratos",
            value=valor_atual,
            key=contratos_key,
            placeholder="Quantidade"
        )
        
        try:
            clean_value = qtd_contratos_formatado.replace(".", "").strip()
            if clean_value:
                qtd_contratos = int(clean_value)
            else:
                qtd_contratos = None
        except ValueError:
            qtd_contratos = None
    
    with col3:
        percentual_ebook = st.number_input(
            "Valor E-book (%)",
            min_value=0.0,
            max_value=100.0,
            value=None,
            step=0.1,
            format="%.1f",
            placeholder="%",
            help="Percentual da mensalidade referente ao E-book"
        )

# col1, col2, col3 = st.columns([1, 1, 1])
# with col2:
#     st.markdown('<div class="botao">', unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)
 
st.markdown("""
<style>
    div.stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    .stButton>button {
        background-color: #FFF;
        color: black;
        font-weight: bold;
        width: 300px;
        font-size: 200%; 
        padding: 10px 0; 
        margin: 20px 0;
        transition: all 0.5s;
    }
</style>
""", unsafe_allow_html=True)    
simulate_button = st.button("SIMULAR")

st.divider()

st.header("Resultados da simulação")

if simulate_button:
    if mensalidade is None or qtd_contratos is None or percentual_ebook is None:
        st.error("Preencha os campos acima corretamente para visualizar os dados da simulação!")
    else:
        receita_bruta = mensalidade * qtd_contratos
        base_calculo_sem_ebook = receita_bruta
        pis = receita_bruta * 0.0065
        cofins = receita_bruta * 0.03
        iss = receita_bruta * 0.05
        irpj = 0.15 * (receita_bruta * 0.32)
        csll = 0.09 * (receita_bruta * 0.32)
        carga_total = pis + cofins + iss + irpj + csll
        
        valor_ebook = receita_bruta * (percentual_ebook / 100)
        base_calculo_com_ebook = receita_bruta - valor_ebook
        pis_ebook = base_calculo_com_ebook * 0.0065
        cofins_ebook = base_calculo_com_ebook * 0.03
        iss_ebook = base_calculo_com_ebook * 0.05
        irpj_ebook = 0.15 * (base_calculo_com_ebook * 0.32)
        irpj8_ebook =  0.15 * (base_calculo_com_ebook * 0.08)
        csll_ebook = 0.09 * (base_calculo_com_ebook * 0.32)
        csll12_ebook = 0.09 * (base_calculo_com_ebook * 0.12)
        carga_total_ebook = pis_ebook + cofins_ebook + iss_ebook + irpj_ebook + irpj8_ebook + csll_ebook + csll12_ebook

        economia = carga_total - carga_total_ebook
        if economia >= 0:
            classe = 'economia'
        else:
            classe = 'perda'

        # Tabelinha:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("")
            st.markdown("**Receita Bruta**")
            st.markdown("**E-book**")
            st.markdown("**Base de Cálculo Imposto**")
            st.markdown("**PIS (0,65%)**")
            st.markdown("**COFINS (3%)**")
            st.markdown("**ISS (5%)**")
            st.markdown("**IRPJ (15% de 32%)**")
            st.markdown("**IRPJ (15% de 8%**")
            st.markdown("**CSLL (9% de 32%)**")
            st.markdown("**CSLL (9% de 12%**")
            st.markdown("**Carga Total**")
            st.markdown('<div class="economia-title">ECONOMIA MENSAL</div>', unsafe_allow_html=True)
            
        with col2:
            st.subheader("Sem e-book")
            st.markdown(f"**{formata_dinheiro(receita_bruta)}**")
            st.markdown("**-**")
            st.markdown(f"**{formata_dinheiro(base_calculo_sem_ebook)}**")
            st.markdown(f"**{formata_dinheiro(pis)}**")
            st.markdown(f"**{formata_dinheiro(cofins)}**")
            st.markdown(f"**{formata_dinheiro(iss)}**")
            st.markdown(f"**{formata_dinheiro(irpj)}**")
            st.markdown(f"**-**")
            st.markdown(f"**{formata_dinheiro(csll)}**")
            st.markdown(f"**-**")
            st.markdown(f"**{formata_dinheiro(carga_total)}**")
            
        with col3:
            st.subheader("Com e-book")
            st.markdown(f"**{formata_dinheiro(receita_bruta)}**")
            st.markdown(f"**{formata_dinheiro(valor_ebook)}**")
            st.markdown(f"**{formata_dinheiro(base_calculo_com_ebook)}**")
            st.markdown(f"**{formata_dinheiro(pis_ebook)}**")
            st.markdown(f"**{formata_dinheiro(cofins_ebook)}**")
            st.markdown(f"**{formata_dinheiro(iss_ebook)}**")
            st.markdown(f"**{formata_dinheiro(irpj_ebook)}**")
            st.markdown(f"**{formata_dinheiro(irpj8_ebook)}**")
            st.markdown(f"**{formata_dinheiro(csll_ebook)}**")
            st.markdown(f"**{formata_dinheiro(csll12_ebook)}**")
            st.markdown(f"**{formata_dinheiro(carga_total_ebook)}**")
            st.markdown(f'<div class="{classe}">{formata_dinheiro(economia)}</div>', unsafe_allow_html=True)
else:
    st.info("Preencha todos os campos acima e clique em SIMULAR para visualizar os resultados da simulação.")