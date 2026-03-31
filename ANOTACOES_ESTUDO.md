# Anotações de Estudos

Este arquivo contém minhas anotações de estudo durante o desenvolvimento do projeto.

O objetivo é registrar aprendizados sobre:
- dbt
- modelagem analítica
- data quality
- arquitetura de projetos de dados
- integração com APIs

## Arquitetura do projeto

Camadas do dbt utilizadas:

- sources → definição das tabelas brutas
- staging → limpeza e padronização inicial
- intermediate → regras de negócio intermediárias
- marts → tabelas analíticas finais

## Conceitos importantes do dbt

source()
Define tabelas externas utilizadas pelo dbt.

ref()
Permite referenciar outros modelos do dbt criando dependências no DAG.

tests
Validações automáticas de qualidade de dados.

snapshots
Captura histórico de mudanças em registros.

materialization
Define como um modelo será criado no banco (view, table, incremental).