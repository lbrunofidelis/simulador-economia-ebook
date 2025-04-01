import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simulador de economia financeira com E-book",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="💵"
)

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Simulador de economia financeira com E-book")

st.text("Este simulador é uma ferramenta que permite calcular potenciais economias tributárias ao incluir e-books em seu modelo de negócio.")

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
 
isenta_pis_cofins = st.toggle("Isenta PIS/COFINS")
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
        if isenta_pis_cofins:
            pis_ebook = base_calculo_com_ebook * 0.0065
            cofins_ebook = base_calculo_com_ebook * 0.03
        else:
            pis_ebook = pis
            cofins_ebook = cofins
            
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
        
        data = {
            "Item": [
                "Receita Bruta",
                "Valor do E-book (R$)",
                "Base de Cálculo Imposto",
                "PIS (0,65%)",
                "COFINS (3%)",
                "ISS (5%)",
                "IRPJ (15% de 32%)",
                "IRPJ (15% de 8%)",
                "CSLL (9% de 32%)",
                "CSLL (9% de 12%)",
                "Carga Total",
                "Economia por mensalidade",
                "Economia mensal",
                "Economia anual"
            ],
            "Sem e-book": [
                formata_dinheiro(receita_bruta),
                "-",
                formata_dinheiro(base_calculo_sem_ebook),
                formata_dinheiro(pis),
                formata_dinheiro(cofins),
                formata_dinheiro(iss),
                formata_dinheiro(irpj),
                "-",
                formata_dinheiro(csll),
                "-",
                formata_dinheiro(carga_total),
                "-",
                "-",
                "-"
            ],
            "Com e-book": [
                formata_dinheiro(receita_bruta),
                formata_dinheiro(valor_ebook),
                formata_dinheiro(base_calculo_com_ebook),
                formata_dinheiro(pis_ebook),
                formata_dinheiro(cofins_ebook),
                formata_dinheiro(iss_ebook),
                formata_dinheiro(irpj_ebook),
                formata_dinheiro(irpj8_ebook),
                formata_dinheiro(csll_ebook),
                formata_dinheiro(csll12_ebook),
                formata_dinheiro(carga_total_ebook),
                formata_dinheiro(economia/qtd_contratos),
                formata_dinheiro(economia),
                formata_dinheiro(economia*12)
            ]
        }
        
        df = pd.DataFrame(data)
        
        def highlight_row(row):
            styles = [''] * len(row)
            if row.name >= 12:
                styles[2] = f'color: {"#11b35c" if economia >= 0 else "#ee3838"}; font-weight: bold; font-size: 125%'
            if row.name == 0 or row.name == 2 or row.name == 10:
                styles = ['font-weight: bold'] * len(row)
            return styles
        
        styled_df = df.style.apply(highlight_row, axis=1)
        
        st.dataframe(styled_df, use_container_width=True, height=530)
        
        st.markdown("### Resumo da Economia 💵")
        col1, col2 = st.columns(2)
        if economia >= 0:
            with col1:
                st.markdown(f"""
                <div style='font-size: 20px; font-weight: bold; margin: 15px 0; padding: 10px; background-color: {"#e6f7ef" if economia >= 0 else "#fce8e6"}; border-radius: 5px;'>
                    <span>Você economiza por mês: <span style='color: {"#11b35c" if economia >= 0 else "#ee3838"};'>{formata_dinheiro(economia)}</span></span><br>
                    <span>Você economiza por ano: <span style='color: {"#11b35c" if economia >= 0 else "#ee3838"};'>{formata_dinheiro(economia*12)}</span></span>
                </div>
                """, unsafe_allow_html=True)
        else:
            with col1:
                st.error(f"Com essa configuração, você teria um aumento de {formata_dinheiro(abs(economia))} por mês em impostos.")
            
        # if economia >= 0:
            # st.success(f"Com a estratégia do e-book, você economiza {formata_dinheiro(economia)} por mês em impostos!")
        
        with col2:     
            with st.expander("LEGENDA", expanded=False):
                st.markdown("""
                - **Receita Bruta**: Valor total recebido de todos os contratos
                - **E-book**: Valor atribuído ao e-book conforme o percentual escolhido
                - **Base de Cálculo Imposto**: Valor sobre o qual os impostos serão calculados
                - **PIS/COFINS/ISS**: Impostos calculados sobre a base de cálculo
                - **IRPJ/CSLL**: Impostos sobre o lucro presumido
                """)
else:
    st.info("Preencha todos os campos acima e clique em SIMULAR para visualizar os resultados da simulação.")
