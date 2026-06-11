# NogTech ETL Pipeline — Apache Airflow

Pipeline de ETL desenvolvido para consolidar dados acadêmicos da NogTech, realizando extração, transformação e carga automatizada através do Apache Airflow. Os dados processados são armazenados em PostgreSQL e disponibilizados para análise através do Apache Superset.

---

## Tecnologias utilizadas

- **Apache Airflow 2.9.1** — Orquestração do pipeline
- **PostgreSQL 15** — Armazenamento dos dados processados
- **Apache Superset** — Visualização e análise dos dados
- **Docker + Docker Compose** — Containerização do ambiente
- **Python** — Desenvolvimento do ETL
- **Pandas** — Manipulação e tratamento dos dados
- **SQLAlchemy** — Integração com PostgreSQL
- **psycopg2** — Driver PostgreSQL para Python

---

## Arquitetura da Solução

```text
CSV
 │
 ▼
Extract
 │
 ▼
Transform
 │
 ▼
resultado.csv
 │
 ▼
PostgreSQL
 │
 ▼
Apache Superset
 │
 ▼
Dashboard Analítico
```

---

## Estrutura do Projeto

```text
nogtech-etl-airflow/
│
├── airflow/
│   ├── dags/
│   │   ├── nogtech_etl.py
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   │
│   └── requirements.txt
│
├── data/
│   ├── alunos.csv
│   └── resultado.csv
│
├── cache/
│
├── superset/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── exports/
│       └── dashboard_export_*.zip
│
├── docker-compose.yml
│
└── README.md
```

---

## Como Rodar o Projeto

### Pré-requisitos

- Docker
- Docker Compose
- Git

### Clonar o Repositório

```bash
git clone https://github.com/Marquin25/nogtech-etl-airflow.git

cd nogtech-etl-airflow
```

### Subir os Containers

```bash
docker compose up -d
```

Verificar se todos os containers estão executando:

```bash
docker ps
```

Containers esperados:

```text
airflow_nogtech
postgres_nogtech
superset_nogtech
```

Aguarde aproximadamente 60 segundos para que todos os serviços inicializem corretamente.

---

## Acessos

| Serviço | URL | Usuário | Senha |
|----------|----------|----------|----------|
| Airflow | http://localhost:8080 | admin | admin |
| Superset | http://localhost:8088 | admin | admin |
| PostgreSQL | localhost:5432 | airflow | airflow |

---

## Como Executar o Pipeline

1. Acesse o Airflow em `http://localhost:8080`
2. Localize a DAG **nogtech_etl**
3. Clique em **Trigger DAG**
4. Aguarde a execução das etapas:
   - Extract
   - Transform
   - Load
5. Verifique se todas as tarefas ficaram verdes

Após a conclusão, os dados serão carregados no PostgreSQL.

---

## O que o Pipeline Faz

### Extract

- Lê os dados de entrada (`alunos.csv`)
- Valida a estrutura dos dados
- Prepara os dados para transformação

### Transform

- Limpa e padroniza os dados
- Corrige tipos de dados
- Remove inconsistências
- Gera o arquivo consolidado `resultado.csv`

### Load

- Conecta ao PostgreSQL
- Cria ou substitui a tabela analítica
- Carrega os dados transformados

Tabela gerada:

```sql
alunos_tratados
```

---

## Banco de Dados

Acessando o PostgreSQL:

```bash
docker exec -it postgres_nogtech psql -U airflow -d nogtech
```

Consultar registros:

```sql
SELECT * FROM alunos_tratados LIMIT 10;
```

Contar registros:

```sql
SELECT COUNT(*) FROM alunos_tratados;
```

---

## Dashboard no Apache Superset

Após a execução do pipeline, os dados podem ser visualizados através do Apache Superset.

Acesse:

```text
http://localhost:8088
```

O projeto já possui um dashboard exportado disponível na pasta:

```text
superset/exports/
```

---

## Importando o Dashboard

O dashboard não é carregado automaticamente pelo Superset.

1. Acesse o Superset.
2. Vá em **Settings → Import Dashboards**.
3. Selecione o arquivo localizado em:

```text
superset/exports/dashboard_export_*.zip
```

4. Clique em **Import**.

---

## Configurando a Conexão com o PostgreSQL

Após importar o dashboard:

1. Vá em **Settings → Database Connections**.
2. Crie ou edite a conexão PostgreSQL.

### Dentro do Docker

```text
Host: postgres
Port: 5432
Database: nogtech
Username: airflow
Password: airflow
```

### Fora do Docker

```text
Host: localhost
Port: 5432
Database: nogtech
Username: airflow
Password: airflow
```

3. Clique em **Test Connection**.
4. Salve a conexão.

---

## Ajustando o Dataset após a Importação

Dependendo da instalação do Superset, o dashboard pode ser importado sem a conexão correta.

1. Acesse **Data → Datasets**
2. Localize o dataset utilizado pelo dashboard
3. Clique em **Edit**
4. Selecione a conexão PostgreSQL configurada anteriormente
5. Salve as alterações

Após esse procedimento, todos os gráficos e indicadores funcionarão normalmente.

---

## Monitoramento

O Apache Airflow permite:

- Visualizar logs das tarefas
- Monitorar execuções
- Identificar falhas
- Reexecutar tarefas individualmente
- Visualizar o DAG Graph

---

## Idempotência

O pipeline foi desenvolvido para permitir múltiplas execuções sem comprometer a consistência dos dados.

A cada execução:

- Os dados são reprocessados
- A tabela analítica é atualizada
- Não há duplicação de registros

---

## Testando Manualmente uma Tarefa

Executar a etapa de extração:

```bash
docker exec -it airflow_nogtech airflow tasks test nogtech_etl extract
```

Executar a etapa de transformação:

```bash
docker exec -it airflow_nogtech airflow tasks test nogtech_etl transform
```

Executar a etapa de carga:

```bash
docker exec -it airflow_nogtech airflow tasks test nogtech_etl load
```

---

## Objetivo Acadêmico

Projeto desenvolvido para a disciplina de **Big Data**, demonstrando a utilização de ferramentas Open Source para:

- Orquestração de pipelines de dados
- Processos ETL
- Containerização
- Armazenamento em banco relacional
- Construção de dashboards analíticos

---

## Autor

**Marcus Antônio Rodrigues Monteiro Rios de Pina**
**Theo Jose Luna Leal**
**João Victor Marinho**

GitHub: https://github.com/Marquin25

Disciplina: Big Data
