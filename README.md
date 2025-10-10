# CARTEIRA DIVERSIFICADA  
### *Framework Quantitativo de Alocação de Ativos*

---
## Descrição Geral do Projeto
O projeto **Carteira Diversificada** é um framework quantitativo desenvolvido para automatizar a construção de portfólios de investimento personalizados com base no perfil, idade e objetivos do investidor.  
O objetivo central é transformar o processo de alocação de ativos em uma **estrutura sistemática, objetiva e replicável**, substituindo decisões intuitivas por métricas verificáveis e métodos quantitativos sólidos.

Para especializações técnicas e aprofundamento teórico da solução computacional aprimorada, acesse as documentações abaixo!
Definição teórica : https://docs.google.com/document/d/1CgBhhni9QJSXMyYvoJFjYaWu1Rm_UzxiCMTPq6gGuuE/edit?usp=sharing
Detalhes técnicos e objetivos: 
---

## Contexto e Motivação

No ambiente atual, o investidor enfrenta um desafio crescente: a **complexidade dos mercados financeiros**.  
As oportunidades de investimento se multiplicaram, mas também os riscos — resultantes de ciclos macroeconômicos, volatilidade global e choques externos.  

Tradicionalmente, muitos investidores recorrem a recomendações genéricas, desconsiderando o **perfil individual de risco** e o **horizonte de investimento**.  
A *Carteira Diversificada* surge para resolver esse problema, oferecendo uma **plataforma quantitativa e dinâmica** capaz de:

- Traduzir o perfil e o horizonte do investidor ;  
- Analisar o comportamento conjunto dos ativos via ;  
- Gerar **carteiras ótimas** conforme o perfil de risco;  
- Executar **monitoramento e rebalanceamento contínuos**, mantendo o alinhamento estratégico ao longo do tempo.

---

## Objetivos do Projeto

### Objetivo Geral
Desenvolver um **framework quantitativo modular** capaz de:
- Estimar retornos e riscos esperados;
- Calcular correlações e volatilidades históricas;
- Aplicar algoritmos de otimização para construção da **carteira eficiente**;
- Ajustar automaticamente as alocações conforme **perfil e idade do investidor**.

### Objetivos Específicos
1. **Construir um pipeline de dados financeiros** robusto e automatizado (coleta, limpeza e processamento);  
2. **Gerar carteiras de referência** (Conservadora, Moderada e Arrojada) para diferentes idades;  
3. **Simular cenários históricos e stress tests**, avaliando robustez e estabilidade;  
4. **Integrar futuramente modelos de IA** para previsão de retornos e rebalanceamento dinâmico;  
5. **Gerar relatórios e visualizações automatizadas** (fronteira eficiente, correlação, métricas de risco).  

---

## Visão Geral do Projeto

O projeto é estruturado em **duas camadas principais**:

- **Camada Conceitual e Financeira:**  
  Define fundamentos teóricos como perfil de risco, diversificação, correlação e fronteira eficiente.  

- **Camada Técnica e Computacional:**  
  Implementa na prática os cálculos, a estrutura de dados e os algoritmos de otimização.  

A integração entre essas camadas é o diferencial do framework:  
o sistema não apenas replica o modelo de Markowitz, mas também o **expande com princípios de engenharia de software, ciência de dados e automação**, garantindo:

- Escalabilidade  
- Reprodutibilidade  
- Modularidade  
- Aderência a perfis reais de investimento

As quatro etapas formam o ciclo completo do sistema Carteira Diversificada:
definir dados → otimizar → aplicar → monitorar.


# Arquitetura Técnica do Sistema
## Contexto e Motivação
O sistema Carteira Diversificada foi projetado com base em uma arquitetura modular e escalável, separando as responsabilidades em camadas distintas: coleta, pré-processamento, otimização e relatórios

A estrutura de diretórios do projeto segue o padrão de sistemas de pesquisa quantitativa e análise de portfólio, garantindo clareza e modularidade
Essa arquitetura modular permite:
 - Facilidade na substituição de componentes (por exemplo, trocar a fonte de dados sem alterar o otimizador);
 - Rastreamento claro do fluxo de informação;
 - Organização compatível com pipelines de machine learning e backtesting financeiro.

## Descrição dos Módulos Principais

### a) Data Collection (Coleta de Dados)
Responsável pela **obtenção de preços e séries históricas** de ativos financeiros.  
Utiliza APIs como **Yahoo Finance** e **Banco Central (BCB)**.  
O resultado é armazenado em `data/raw/prices_raw.csv`.

**Funções principais:**
- `fetch_yahoo.py`: coleta e ajusta preços (dividendos e splits);  
- `fetch_bcb.py`: coleta dados macroeconômicos (CDI, IPCA, SELIC).  

---

###  b) Preprocessing (Pré-processamento)
Converte preços brutos em **retornos percentuais**, remove dados inconsistentes e calcula **matrizes de correlação e covariância**.  
Essa etapa prepara os dados para a otimização.

**Funções principais:**
- `clean_data.py`: tratamento de valores nulos e alinhamento temporal;  
- `returns_calculator.py`: cálculo de retornos diários, mensais e anuais;  
- `correlation_matrix.py`: geração das matrizes de correlação e covariância.  

**Saídas:**  
`returns.csv`, `correlation.csv`, `covariance.csv`

---

### c) Optimization (Otimização e Modelagem)
Núcleo quantitativo do sistema.  
Implementa o **modelo de Markowitz** e resolve o problema de **programação quadrática** para determinar a alocação ótima.

**Componentes:**
- `markowitz_model.py`: cálculo da carteira eficiente;  
- `constraints.py`: definição de limites e perfis de risco;  
- `efficient_frontier.py`: geração dos pontos de risco-retorno da fronteira eficiente.  

**Saídas:**  
`allocations.csv`, `efficient_frontier.png`

---

### 📊 d) Reporting (Relatórios e Visualização)
Responsável pela geração de relatórios e gráficos para interpretação dos resultados.  
Consolida métricas de risco-retorno, fronteira eficiente e alocações finais.

**Funções principais:**
- `visualization.py`: gráficos de correlação, dispersão e fronteira eficiente;  
- `generate_report.py`: criação de relatórios automáticos (PDF, HTML ou CSV);  
- `export_results.py`: exportação de resultados padronizados para reutilização.  

**Saídas:**  
`report.pdf`, `allocations.csv`, `efficient_frontier.png`

---

### e) Utils (Funções Auxiliares)
Reúne ferramentas de suporte que garantem modularidade e manutenção simplificada.

**Funções principais:**
- `config_loader.py`: leitura de arquivos de configuração;  
- `logger.py`: logging estruturado para depuração e auditoria;  
- `performance_metrics.py`: cálculo de métricas como *Sharpe Ratio* e *Drawdown*.

---

## Fluxo de Dados (Pipeline Quantitativo)

O sistema segue um **pipeline linear e reproduzível**, composto por quatro estágios:

1. **Coleta de Dados:**  
   Importação de séries históricas e dados macroeconômicos.

2. **Pré-Processamento:**  
   Limpeza, normalização e cálculo de retornos e matrizes estatísticas.

3. **Otimização:**  
   Aplicação do modelo de Markowitz e determinação dos pesos ideais.

4. **Geração de Saída:**  
   Produção de relatórios e visualizações (carteira ótima e fronteira eficiente).

Cada etapa escreve seus resultados em diretórios específicos dentro de `/data/`, garantindo **rastreabilidade total** e **reprodutibilidade completa** do processo.
