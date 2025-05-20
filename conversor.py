import pandas as pd
import os

# === 1. Carrega os arquivos .xls com os nomes reais ===
df_programa = pd.read_excel("tabelas/Programa.xls")
df_objetivo_geral = pd.read_excel("tabelas/ObjetivoGeral.xls")
df_objetivo = pd.read_excel("tabelas/Objetivo.xls")
df_objetivo_especifico = pd.read_excel("tabelas/ObjetivoEspecifico.xls")
df_indicador_entrega = pd.read_excel("tabelas/Indicador Entrega.xls")
df_indicador_obj_espec = pd.read_excel("tabelas/Indicador Objetivo Especifico.xls")

# Normaliza nomes das colunas (padroniza todos para UPPER)
for df in [df_programa, df_objetivo_geral, df_objetivo, df_objetivo_especifico, df_indicador_entrega, df_indicador_obj_espec]:
    df.columns = df.columns.str.strip().str.upper()

# === 2. Cria diretório de saída ===
output_dir = "docs"
os.makedirs(output_dir, exist_ok=True)

# === 3. Função principal ===
def gerar_passages(df_programa, df_objetivo_geral, df_objetivo, df_objetivo_especifico, df_ind_entrega, df_ind_obj_esp):
    passages = []
    print("Colunas do df_programa:", df_programa.columns.tolist())

    for _, prog in df_programa.iterrows():
        prog_id = prog["PROGRAMA"]
        prog_nome = prog["TÍTULO"]

        texto = f"Programa: {prog_nome.strip()}\n\n"

        # Objetivos Gerais
        objetivos_gerais = df_objetivo_geral[df_objetivo_geral["PROGRAMA"] == prog_id]
        if not objetivos_gerais.empty:
            texto += "Objetivo Geral:\n"
            for _, row in objetivos_gerais.iterrows():
                texto += f"- {row['ENUNCIADO']}\n"
        else:
            texto += "Objetivo Geral: não definido\n"

        # Objetivos
        objetivos = df_objetivo[df_objetivo["PROGRAMA"] == prog_id]
        if not objetivos.empty:
            texto += "\nObjetivos:\n"
            for _, row in objetivos.iterrows():
                texto += f"- {row['ENUNCIADO']}\n"

        # Objetivos Específicos
        objetivos_esp = df_objetivo_especifico[df_objetivo_especifico["PROGRAMA"] == prog_id]
        if not objetivos_esp.empty:
            texto += "\nObjetivos Específicos:\n"
            for _, row in objetivos_esp.iterrows():
                texto += f"- {row['ENUNCIADO']}\n"

        # Indicadores (Entrega)
        ind_entrega = df_ind_entrega[df_ind_entrega["PROGRAMA"] == prog_id]
        if not ind_entrega.empty:
            texto += "\nIndicadores de Entrega:\n"
            for _, ind in ind_entrega.iterrows():
                nome = ind.get("DENOMINAÇÃO", "Indicador sem nome")
                #meta = ind.get("VALOR_META", "meta não informada")
                #ano = ind.get("ANO_FINAL", "")
                texto += f"- {nome} \n" # #: {meta} ({ano})
 
        # Indicadores (Objetivo Específico)
        ind_obj = df_ind_obj_esp[df_ind_obj_esp["PROGRAMA"] == prog_id]
        if not ind_obj.empty:
            texto += "\nIndicadores de Objetivos Específicos:\n"
            for _, ind in ind_obj.iterrows():
                nome = ind.get("DENOMINAÇÃO", "Indicador sem nome")
                #meta = ind.get("VALOR_META", "meta não informada")
                #ano = ind.get("ANO_FINAL", "")
                texto += f"- {nome}: \n" #{meta} ({ano})

        passage = f"passage: {texto.strip()}"
        passages.append((prog_nome.strip(), passage))

    return passages

# === 4. Executa a geração e salva os arquivos ===
passagens = gerar_passages(
    df_programa,
    df_objetivo_geral,
    df_objetivo,
    df_objetivo_especifico,
    df_indicador_entrega,
    df_indicador_obj_espec
)

for nome_prog, passage in passagens:
    nome_arquivo = f"{nome_prog.replace(' ', '_').replace('/', '-')}.txt"
    with open(os.path.join(output_dir, nome_arquivo), "w", encoding="utf-8") as f:
        f.write(passage)

print(f"✅ {len(passagens)} arquivos salvos em '{output_dir}'")
