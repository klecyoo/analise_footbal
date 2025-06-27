# Sistema de Análise de Futebol - Odds 1.25

## Resumo Executivo

O Sistema de Análise de Futebol com foco em Odds 1.25 é uma solução completa e avançada para análise estatística de futebol, desenvolvida especificamente para identificar oportunidades de apostas com odds 1.25 confiáveis. O sistema combina recolha automatizada de dados, algoritmos de análise avançada, e uma interface web moderna para fornecer previsões precisas e recomendações fundamentadas.

### Características Principais

- **Recolha Automatizada de Dados**: Integração com APIs de futebol para obter dados atualizados de equipas, jogadores e partidas
- **Análise Estatística Avançada**: Algoritmos sofisticados para calcular médias, tendências e probabilidades
- **Sistema Especializado em Odds 1.25**: Foco específico em identificar apostas com 80%+ de probabilidade de sucesso
- **Interface Web Moderna**: Dashboard interativo com visualizações em tempo real
- **Calculadora de Apostas**: Ferramentas para calcular valor esperado, ROI e gestão de risco
- **Análise de Mercado**: Identificação de padrões e tendências do mercado de apostas
- **Rastreamento de Performance**: Monitorização contínua da precisão das previsões

## Arquitetura do Sistema

### Backend (Flask)
- **Framework**: Flask com Python 3.11
- **Base de Dados**: SQLite com SQLAlchemy ORM
- **APIs**: Integração com API-Futebol.com.br
- **Estrutura Modular**: Separação clara entre modelos, serviços e rotas

### Frontend (Web)
- **Tecnologias**: HTML5, CSS3, JavaScript ES6+
- **Design**: Interface responsiva com design moderno
- **Gráficos**: Chart.js para visualizações interativas
- **UX/UI**: Dashboard intuitivo com navegação fluida

### Componentes Principais

1. **Módulo de Recolha de Dados** (`football_api.py`)
2. **Motor de Análise Avançada** (`advanced_analytics.py`)
3. **Sistema de Odds 1.25** (`odds_125_system.py`)
4. **Interface Web** (HTML/CSS/JS)
5. **Modelos de Dados** (`football.py`)

## Funcionalidades Detalhadas

### 1. Recolha e Processamento de Dados

O sistema recolhe automaticamente dados de:
- **Equipas**: Informações básicas, estatísticas, histórico
- **Jogadores**: Dados individuais, performance, estatísticas
- **Partidas**: Resultados, estatísticas detalhadas, contexto
- **Campeonatos**: Estrutura, calendário, classificações

**Endpoints Principais:**
- `/api/football/sync-championship/{id}` - Sincronizar dados de campeonato
- `/api/football/teams` - Listar equipas
- `/api/football/matches` - Listar partidas
- `/api/football/calculate-stats` - Calcular estatísticas

### 2. Análise Estatística Avançada

**Métricas Calculadas:**
- Rating ELO das equipas
- Índice de forma recente
- Médias de golos por partida
- Percentagem de vitórias
- Análise de confrontos diretos
- Tendências de casa vs fora

**Algoritmos Implementados:**
- Regressão logística para probabilidades
- Análise de séries temporais
- Modelos preditivos baseados em histórico
- Cálculo de valor esperado

### 3. Sistema Especializado em Odds 1.25

**Cenários Identificados:**
- Equipa muito superior em casa
- Over/Under baseado em histórico de golos
- Ambas equipas marcam/não marcam
- Dupla hipótese (casa ou empate)
- Forma recente extrema

**Critérios de Confiança:**
- Mínimo 82% de confiança para recomendação
- Análise de valor esperado positivo
- Gestão de risco integrada
- Critério de Kelly para dimensionamento

**Endpoints Específicos:**
- `/api/odds/find-125-opportunities` - Encontrar oportunidades
- `/api/odds/daily-recommendations` - Recomendações diárias
- `/api/odds/bet-calculator` - Calculadora de apostas
- `/api/odds/performance-tracking` - Rastreamento de performance
- `/api/odds/market-analysis` - Análise de mercado

### 4. Interface Web Interativa

**Seções do Dashboard:**
- **Dashboard Principal**: Visão geral e estatísticas
- **Equipas**: Gestão e análise de equipas
- **Partidas**: Histórico e próximas partidas
- **Odds 1.25**: Oportunidades e recomendações
- **Análise Avançada**: Comparação detalhada de equipas
- **Performance**: Métricas e tendências

**Funcionalidades da Interface:**
- Navegação fluida entre seções
- Gráficos interativos em tempo real
- Calculadora de apostas integrada
- Filtros e pesquisa avançada
- Notificações toast para feedback
- Design responsivo para mobile

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip (gestor de pacotes Python)
- Navegador web moderno

### Passos de Instalação

1. **Clonar/Descarregar o Sistema**
```bash
# O sistema está localizado em /home/ubuntu/football-analysis
cd /home/ubuntu/football-analysis
```

2. **Configurar Ambiente Virtual**
```bash
# Ativar ambiente virtual (já criado)
source venv/bin/activate
```

3. **Instalar Dependências**
```bash
# As dependências já estão instaladas
pip install -r requirements.txt
```

4. **Configurar Base de Dados**
```bash
# A base de dados SQLite será criada automaticamente
python -c "from src.models.user import db; db.create_all()"
```

5. **Iniciar o Sistema**
```bash
python src/main.py
```

6. **Aceder à Interface**
- Abrir navegador em `http://localhost:5000`
- O sistema estará disponível imediatamente

### Configuração da API

Para utilizar dados reais, configure a chave da API no ficheiro `src/services/football_api.py`:

```python
API_KEY = "sua_chave_api_aqui"
```

## Guia de Utilização

### 1. Primeiro Acesso

1. **Sincronizar Dados**: Clicar em "Sincronizar Dados" no dashboard
2. **Aguardar Processamento**: O sistema irá recolher dados dos campeonatos
3. **Verificar Estatísticas**: Confirmar que as métricas foram calculadas

### 2. Encontrar Oportunidades de Odds 1.25

1. **Navegar para "Odds 1.25"**
2. **Configurar Parâmetros**:
   - Definir bankroll disponível
   - Selecionar campeonato (opcional)
3. **Clicar "Encontrar Oportunidades"**
4. **Analisar Recomendações**:
   - Verificar nível de confiança
   - Avaliar fatores de suporte
   - Considerar nível de risco

### 3. Utilizar a Calculadora de Apostas

1. **Inserir Valor da Aposta**
2. **Definir Nível de Confiança**
3. **Clicar "Calcular"**
4. **Analisar Resultados**:
   - Lucro potencial
   - Valor esperado
   - ROI estimado

### 4. Análise Avançada de Confrontos

1. **Navegar para "Análise Avançada"**
2. **Selecionar Equipas**:
   - Equipa da casa
   - Equipa visitante
3. **Clicar "Analisar"**
4. **Interpretar Resultados**:
   - Probabilidades de cada resultado
   - Métricas comparativas
   - Recomendação final

### 5. Monitorizar Performance

1. **Navegar para "Performance"**
2. **Selecionar Período de Análise**
3. **Analisar Métricas**:
   - Taxa de acerto
   - ROI médio
   - Tendências

## Algoritmos e Metodologia

### Cálculo de Probabilidades

O sistema utiliza múltiplos modelos para calcular probabilidades:

1. **Modelo ELO**: Rating baseado em resultados históricos
2. **Análise de Forma**: Ponderação de resultados recentes
3. **Vantagem de Casa**: Ajuste estatístico para jogos em casa
4. **Confrontos Diretos**: Histórico específico entre equipas

### Sistema de Confiança

A confiança é calculada através de:
- Consistência histórica dos padrões
- Margem de superioridade estatística
- Volatilidade dos resultados
- Tamanho da amostra de dados

### Gestão de Risco

Implementação do Critério de Kelly para:
- Dimensionamento ótimo de apostas
- Proteção contra ruína
- Maximização do crescimento a longo prazo

## API Reference

### Endpoints de Futebol

#### GET /api/football/teams
Retorna lista de todas as equipas com estatísticas.

**Resposta:**
```json
[
  {
    "id": 1,
    "name": "Nome da Equipa",
    "popular_name": "Nome Popular",
    "abbreviation": "ABC",
    "stats": {
      "matches_played": 20,
      "win_percentage": 65.0,
      "goals_per_match": 1.8,
      "goals_conceded_per_match": 1.2
    }
  }
]
```

#### GET /api/football/matches
Retorna lista de partidas com filtros opcionais.

**Parâmetros:**
- `championship_id` (opcional): ID do campeonato
- `status` (opcional): Status da partida

#### POST /api/football/sync-championship/{id}
Sincroniza dados de um campeonato específico.

### Endpoints de Odds 1.25

#### POST /api/odds/find-125-opportunities
Encontra oportunidades de apostas com odds 1.25.

**Body:**
```json
{
  "championship_id": 2,
  "days_ahead": 7
}
```

#### GET /api/odds/daily-recommendations
Gera recomendações diárias baseadas no bankroll.

**Parâmetros:**
- `bankroll`: Valor disponível para apostas

#### POST /api/odds/bet-calculator
Calcula métricas para uma aposta específica.

**Body:**
```json
{
  "stake": 100,
  "confidence": 80,
  "bet_type": "single"
}
```

## Manutenção e Suporte

### Logs do Sistema
Os logs são armazenados automaticamente e incluem:
- Erros de API
- Cálculos de estatísticas
- Ações do utilizador
- Performance do sistema

### Backup de Dados
A base de dados SQLite deve ser copiada regularmente:
```bash
cp src/database/app.db backup/app_$(date +%Y%m%d).db
```

### Atualizações
Para atualizar o sistema:
1. Fazer backup da base de dados
2. Atualizar código fonte
3. Reinstalar dependências se necessário
4. Reiniciar o serviço

### Resolução de Problemas Comuns

**Erro de Conexão com API:**
- Verificar chave de API
- Confirmar conectividade à internet
- Verificar limites de rate da API

**Performance Lenta:**
- Limpar dados antigos da base de dados
- Otimizar consultas SQL
- Aumentar recursos do servidor

**Interface Não Carrega:**
- Verificar se o Flask está em execução
- Confirmar porta 5000 disponível
- Verificar logs de erro no browser

## Considerações de Segurança

### Proteção de Dados
- Chaves de API armazenadas de forma segura
- Validação de entrada em todos os endpoints
- Sanitização de dados do utilizador

### Acesso ao Sistema
- Sistema projetado para uso local
- Para produção, implementar autenticação
- Considerar HTTPS para dados sensíveis

## Limitações e Disclaimers

### Limitações Técnicas
- Dependente da qualidade dos dados da API
- Requer conectividade constante à internet
- Performance limitada pelo hardware local

### Disclaimer de Apostas
**IMPORTANTE**: Este sistema é uma ferramenta de análise estatística. As apostas envolvem risco financeiro e não há garantia de lucro. O utilizador é responsável por:
- Verificar a legalidade das apostas na sua jurisdição
- Apostar apenas o que pode permitir-se perder
- Considerar as previsões como orientação, não garantias
- Manter sempre controlo sobre as suas finanças

### Responsabilidade
Os desenvolvedores não se responsabilizam por:
- Perdas financeiras resultantes do uso do sistema
- Imprecisões nos dados ou cálculos
- Problemas técnicos ou indisponibilidade
- Decisões de apostas tomadas pelo utilizador

## Roadmap Futuro

### Melhorias Planeadas
- Integração com mais fontes de dados
- Algoritmos de machine learning avançados
- App mobile nativa
- Sistema de alertas em tempo real
- Análise de vídeo automatizada
- Integração com casas de apostas

### Funcionalidades Avançadas
- Previsões para outros tipos de odds
- Análise de mercados de apostas ao vivo
- Sistema de portfolio de apostas
- Backtesting histórico automatizado
- API pública para terceiros

---

**Versão do Sistema**: 1.0  
**Data de Criação**: Junho 2025  
**Última Atualização**: Junho 2025  

Para suporte técnico ou questões sobre o sistema, consulte a documentação técnica ou contacte a equipa de desenvolvimento.

