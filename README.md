# NogTech ETL Pipeline — Apache Airflow

Pipeline de ETL para consolidar o relatório diário de vendas da NogTech, cruzando transações financeiras com engajamento de alunos e enriquecendo os dados com informações geográficas e de calendário via BrasilAPI.

---

## Tecnologias utilizadas

- **Apache Airflow 2.9.1** — orquestração do pipeline
- **PostgreSQL 15** — destino final dos dados
- **Docker + Docker Compose** — containerização do ambiente
- **Python** (pandas, SQLAlchemy, requests) — lógica de ETL
- **BrasilAPI** — enriquecimento de CEP e feriados nacionais

---

## Estrutura do projeto


```
nogtech-etl-airflow/
├── airflow/
│   ├── dags/
│   │   ├── nogtech_etl.py
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   ├── scripts/
│   └── requirements.txt
├── data/
│   ├── transacoes_nogtech.csv
│   └── engajamento_alunos.json
└── docker-compose.yml
```


## Como rodar

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Subindo o ambiente

```bash
git clone https://github.com/Marquin25/nogtech-etl-airflow.git
cd nogtech-etl-airflow
docker-compose up -d
```

Aguarda uns 60 segundos pro Airflow inicializar.

### Acessos

| Serviço    | URL                   | Usuário | Senha  |
|------------|-----------------------|---------|--------|
| Airflow UI | http://localhost:8080 | admin   | admin  |
| PostgreSQL | localhost:5432        | airflow | airflow|

---

## Como executar o pipeline

1. Acessa o Airflow em http://localhost:8080
2. Localiza a DAG **nogtech_etl**
3. Clica em **Trigger DAG** para disparar
4. Acompanha as 3 etapas ficando verdes: Extract → Transform → Load

O resultado vai para a tabela **fato_vendas** no banco nogtech.

---

## O que o pipeline faz

### Extract
- Lê `transacoes_nogtech.csv` (encoding utf-8-sig, separador `;`)
- Lê `engajamento_alunos.json`
- Cruza os dois pelo `cpf_aluno` e `mes_referencia` (LEFT JOIN)

### Transform
- Padroniza o formato do CPF
- Consulta a BrasilAPI pra pegar cidade, UF e bairro pelo CEP
- Verifica se a data da transação cai em feriado nacional
- Anonimiza o CPF seguindo a LGPD: `***.XXX.XXX-**`
- Remove o campo `nome_aluno` do dataset final

### Load
- Apaga os registros das mesmas datas antes de inserir
- Grava na tabela `fato_vendas` do PostgreSQL

---

## Idempotência

A cada execução, o pipeline apaga os registros com as mesmas datas do lote atual antes de inserir os novos. Assim pode rodar várias vezes sem duplicar dados.

---

## Tratamento de falhas

Todas as chamadas pra BrasilAPI têm 3 tentativas com timeout de 5 segundos. Se a API não responder, os campos ficam nulos mas o pipeline continua normalmente.
