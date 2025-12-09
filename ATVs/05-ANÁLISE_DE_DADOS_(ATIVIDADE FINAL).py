# ==================================================
#* Para rodar a aplicação
# ==================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path

# ==================================================
#* Configuração visual
# ==================================================
sns.set_theme(style="darkgrid")

# ==================================================
#* Caminho correto do arquivo Excel
#   Estrutura esperada:
#   DATA/
#     ├── 05 - ANÁLISE DE DADOS (ATIVIDADE FINAL).xlsx
#     └── ATVs/
#         └── 05-ANÁLISE_DE_DADOS_(ATIVIDADE FINAL).py
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent
arquivo_excel = BASE_DIR / "05 - ANÁLISE DE DADOS (ATIVIDADE FINAL).xlsx"

# ==================================================
#* Carregar base de dados (Excel)
# ==================================================
df = pd.read_excel(
    arquivo_excel,
    sheet_name="Planilha1"
)

# ==================================================
#* Mostrar as primeiras 5 linhas (compatível fora do Jupyter)
# ==================================================
print(df.head())

# ==================================================
#* Verificando tipos de dados e valores nulos
# ==================================================
df.info()

# ==================================================
#* TRATAMENTO DE DADOS
# ==================================================

#* Limpeza de e-mail
df["EmailLimpo"] = df["ClientesEmail"].astype(str).str.split("#").str[0]

#* Conversão de data de nascimento
df["ClientesNascimento"] = pd.to_datetime(
    df["ClientesNascimento"],
    errors="coerce"
)

#* Corrigir anos inválidos (ex.: 2054 → 1954)
ano_atual = datetime.now().year

def corrigir_ano(data):
    if pd.isna(data):
        return data
    if data.year > ano_atual:
        return data.replace(year=data.year - 100)
    return data

df["DataNascimento"] = df["ClientesNascimento"].apply(corrigir_ano)

#* Calcular idade
hoje = datetime.now()

def calcular_idade(data):
    if pd.isna(data):
        return None
    idade = hoje.year - data.year
    if (hoje.month, hoje.day) < (data.month, data.day):
        idade -= 1
    return idade

df["Idade"] = df["DataNascimento"].apply(calcular_idade)

#* Criar faixas etárias
bins = [0, 29, 39, 49, 59, 69, 120]
labels = ["<30", "30-39", "40-49", "50-59", "60-69", "70+"]

df["FaixaEtaria"] = pd.cut(
    df["Idade"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# ==================================================
#* ANÁLISES VISUAIS (DASHBOARD)
# ==================================================

#* Distribuição de Idade
plt.figure(figsize=(10, 6))
sns.histplot(
    data=df.dropna(subset=["Idade"]),
    x="Idade",
    bins=15,
    kde=True
)
plt.title("Distribuição de Idade dos Clientes")
plt.xlabel("Idade")
plt.ylabel("Quantidade")
plt.show()

#* Boxplot de Idade por Cidade
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="ClientesCidade",
    y="Idade"
)
plt.title("Distribuição de Idade por Cidade")
plt.xlabel("Cidade")
plt.ylabel("Idade")
plt.xticks(rotation=30)
plt.show()

#* KDE da Idade
plt.figure(figsize=(10, 6))
sns.kdeplot(
    data=df.dropna(subset=["Idade"]),
    x="Idade",
    fill=True
)
plt.title("Densidade de Idade dos Clientes")
plt.xlabel("Idade")
plt.show()

#* Distribuição de Clientes por Faixa Etária
plt.figure(figsize=(10, 6))
sns.countplot(
    data=df,
    x="FaixaEtaria"
)
plt.title("Distribuição de Clientes por Faixa Etária")
plt.xlabel("Faixa Etária")
plt.ylabel("Quantidade")
plt.show()

#* Boxplot de Idade por Faixa Etária
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="FaixaEtaria",
    y="Idade"
)
plt.title("Idade por Faixa Etária")
plt.xlabel("Faixa Etária")
plt.ylabel("Idade")
plt.show()

#* Quantidade de Clientes por Cidade
plt.figure(figsize=(10, 6))
sns.countplot(
    data=df,
    x="ClientesCidade"
)
plt.title("Quantidade de Clientes por Cidade")
plt.xlabel("Cidade")
plt.ylabel("Quantidade")
plt.xticks(rotation=30)
plt.show()

#* Quantidade de Clientes por Faixa Etária e Cidade
plt.figure(figsize=(10, 6))
sns.countplot(
    data=df,
    x="FaixaEtaria",
    hue="ClientesCidade"
)
plt.title("Faixa Etária por Cidade")
plt.xlabel("Faixa Etária")
plt.ylabel("Quantidade")
plt.show()

# ==================================================
#* INDICADORES (KPIs)
# ==================================================

print("\n===== INDICADORES GERAIS =====")
print(f"Total de clientes: {df.shape[0]}")
print(f"Idade média: {df['Idade'].mean():.1f} anos")
print(f"Idade mínima: {int(df['Idade'].min())} anos")
print(f"Idade máxima: {int(df['Idade'].max())} anos")
