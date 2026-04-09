
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Bem vindo! Vamos analisar dados com filtros de UF e notas")
st.write("Iremos analisar os dados de um arquivo CSV e mostrar resultados com filtro de Unidade Federativa e faixa de notas.")
st.markdown("---")
df = pd.read_csv("TABELA.csv")
df["nome_uf_prova"] = df["nome_uf_prova"].astype(str).str.strip()

st.sidebar.header("Filtros")
uf_options = sorted(df["nome_uf_prova"].dropna().unique())
selected_ufs = st.sidebar.multiselect("Selecione as UFs", options=uf_options, default=uf_options)

min_nota = float(df["nota_ch_ciencias_humanas"].min())
max_nota = float(df["nota_ch_ciencias_humanas"].max())
selected_nota = st.sidebar.slider(
    "Faixa de notas de Ciências Humanas",
    min_value=min_nota,
    max_value=max_nota,
    value=(min_nota, max_nota),
    step=0.1,
)

filtered_df = df[
    df["nome_uf_prova"].isin(selected_ufs)
    & df["nota_ch_ciencias_humanas"].between(selected_nota[0], selected_nota[1])
]

st.subheader("Dados filtrados")
st.write(f"Registros mostrados: {len(filtered_df)}")
st.dataframe(filtered_df[["nome_uf_prova", "nota_ch_ciencias_humanas", "nota_cn_ciencias_da_natureza", "nota_lc_linguagens_e_codigos", "nota_mt_matematica", "nota_redacao"]])

st.subheader("Estatísticas dos tópicos selecionados")
topic_options = [
    "nota_ch_ciencias_humanas",
    "nota_cn_ciencias_da_natureza",
    "nota_lc_linguagens_e_codigos",
    "nota_mt_matematica",
    "nota_redacao",
    "nota_media_5_notas",
]
selected_topics = st.multiselect(
    "Selecione os tópicos para calcular média, moda e mediana:",
    options=topic_options,
    default=topic_options[:3],
)

if selected_topics:
    stats = []
    for col in selected_topics:
        values = filtered_df[col].dropna()
        if values.empty:
            stats.append({"Tópico": col, "Média": None, "Moda": None, "Mediana": None})
            continue
        mode_values = values.mode()
        mode_text = ", ".join(str(v) for v in mode_values.tolist())
        stats.append({
            "Tópico": col,
            "Média": round(values.mean(), 2),
            "Moda": mode_text,
            "Mediana": round(values.median(), 2),
        })
    st.dataframe(pd.DataFrame(stats))
else:
    st.info("Selecione ao menos um tópico para calcular as estatísticas.")

st.subheader("Gráfico Plotly: distribuição de notas de Ciências Humanas")
fig = px.histogram(
    filtered_df,
    x="nota_ch_ciencias_humanas",
    color="nome_uf_prova",
    nbins=30,
    opacity=0.8,
    title="Distribuição de notas de Ciências Humanas por UF",
    labels={"nota_ch_ciencias_humanas": "Nota CH", "nome_uf_prova": "UF"},
)
fig.update_layout(barmode="overlay", legend_title_text="UF")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Resumo por UF")
summary = filtered_df.groupby("nome_uf_prova")["nota_ch_ciencias_humanas"].agg(["count", "mean", "min", "max"]).reset_index()
summary.columns = ["UF", "Contagem", "Média CH", "Mínimo CH", "Máximo CH"]
st.dataframe(summary)


st.write("Obrigado pela atenção!")



