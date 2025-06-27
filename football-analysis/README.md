# 🏈 Sistema de Análise de Futebol - Odds 1.25

> Sistema completo de análise estatística de futebol com foco em identificar oportunidades de apostas com odds 1.25 confiáveis.

## 🚀 Características Principais

- **📊 Análise Estatística Avançada**: Algoritmos sofisticados para calcular probabilidades e tendências
- **🎯 Especialização em Odds 1.25**: Sistema otimizado para identificar apostas com 80%+ de confiança
- **🔄 Dados em Tempo Real**: Integração com APIs de futebol para informações atualizadas
- **💻 Interface Web Moderna**: Dashboard interativo e responsivo
- **🧮 Calculadora de Apostas**: Ferramentas para gestão de risco e cálculo de valor esperado
- **📈 Rastreamento de Performance**: Monitorização contínua da precisão das previsões

## 🏗️ Arquitetura

### Backend
- **Flask** (Python 3.11) - Servidor web e API REST
- **SQLite** - Base de dados com SQLAlchemy ORM
- **NumPy** - Cálculos estatísticos avançados

### Frontend
- **HTML5/CSS3/JavaScript** - Interface web moderna
- **Chart.js** - Gráficos interativos
- **Design Responsivo** - Compatível com desktop e mobile

## 📦 Instalação Rápida

```bash
# 1. Navegar para o diretório
cd /home/ubuntu/football-analysis

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Iniciar o sistema
python src/main.py

# 4. Abrir no navegador
# http://localhost:5000
```

## 🎮 Como Usar

### 1. Primeira Configuração
1. Aceder a `http://localhost:5000`
2. Clicar em "Sincronizar Dados"
3. Aguardar processamento dos dados

### 2. Encontrar Oportunidades
1. Navegar para "Odds 1.25"
2. Definir bankroll disponível
3. Clicar "Encontrar Oportunidades"
4. Analisar recomendações

### 3. Análise Avançada
1. Ir para "Análise Avançada"
2. Selecionar equipas para comparar
3. Obter análise detalhada do confronto

## 📊 Funcionalidades

### Dashboard Principal
- Visão geral das estatísticas
- Oportunidades do dia
- Gráficos de performance

### Sistema de Odds 1.25
- Identificação automática de oportunidades
- Análise de confiança e risco
- Recomendações personalizadas
- Calculadora de apostas integrada

### Análise de Equipas
- Estatísticas detalhadas
- Comparação entre equipas
- Histórico de confrontos
- Índices de forma

### Gestão de Performance
- Taxa de acerto das previsões
- ROI médio
- Análise de tendências
- Métricas de risco

## 🔧 Estrutura do Projeto

```
football-analysis/
├── src/
│   ├── main.py                 # Servidor Flask principal
│   ├── models/
│   │   ├── football.py         # Modelos de dados
│   │   └── user.py            # Gestão de utilizadores
│   ├── routes/
│   │   ├── football.py        # Endpoints de futebol
│   │   ├── odds_125.py        # Endpoints de odds 1.25
│   │   └── advanced.py        # Análise avançada
│   ├── services/
│   │   ├── football_api.py    # Integração com APIs
│   │   ├── advanced_analytics.py  # Algoritmos de análise
│   │   └── odds_125_system.py # Sistema especializado
│   └── static/
│       ├── index.html         # Interface principal
│       ├── styles.css         # Estilos
│       └── script.js          # Lógica frontend
├── venv/                      # Ambiente virtual Python
├── requirements.txt           # Dependências
├── DOCUMENTACAO_COMPLETA.md   # Documentação detalhada
└── INSTALACAO_RAPIDA.md       # Guia de instalação
```

## 🎯 Algoritmos Implementados

### Cálculo de Probabilidades
- **Rating ELO**: Sistema de classificação baseado em resultados
- **Análise de Forma**: Ponderação de resultados recentes
- **Vantagem de Casa**: Ajuste estatístico para jogos em casa
- **Confrontos Diretos**: Histórico específico entre equipas

### Sistema de Confiança
- Consistência histórica dos padrões
- Margem de superioridade estatística
- Análise de volatilidade
- Validação cruzada de dados

### Gestão de Risco
- **Critério de Kelly**: Dimensionamento ótimo de apostas
- **Valor Esperado**: Cálculo matemático de rentabilidade
- **Análise de Cenários**: Simulação de diferentes outcomes

## 📈 Cenários de Odds 1.25

O sistema identifica automaticamente:

1. **Equipa Superior em Casa**: Diferença significativa de qualidade
2. **Over/Under Golos**: Baseado em médias históricas
3. **Ambas Marcam**: Análise de capacidade ofensiva/defensiva
4. **Dupla Hipótese**: Casa ou empate com alta probabilidade
5. **Forma Extrema**: Equipas em excelente vs má forma

## 🔒 Disclaimer Importante

⚠️ **AVISO**: Este sistema é uma ferramenta de análise estatística. As apostas envolvem risco financeiro e não há garantia de lucro. Use com responsabilidade:

- Aposte apenas o que pode permitir-se perder
- Verifique a legalidade das apostas na sua jurisdição
- As previsões são orientações, não garantias
- Mantenha sempre controlo sobre as suas finanças

## 📚 Documentação

- **[Documentação Completa](DOCUMENTACAO_COMPLETA.md)** - Manual detalhado do sistema
- **[Guia de Instalação](INSTALACAO_RAPIDA.md)** - Instalação em 5 minutos
- **[Documentação PDF](DOCUMENTACAO_COMPLETA.pdf)** - Versão para impressão

## 🛠️ Requisitos Técnicos

- **Python**: 3.11 ou superior
- **Navegador**: Chrome, Firefox, Safari, Edge (versões recentes)
- **Memória**: Mínimo 2GB RAM
- **Armazenamento**: 500MB espaço livre
- **Internet**: Conexão estável para sincronização de dados

## 🚀 Funcionalidades Futuras

- [ ] App mobile nativa
- [ ] Integração com mais APIs de dados
- [ ] Algoritmos de machine learning
- [ ] Sistema de alertas em tempo real
- [ ] Análise de vídeo automatizada
- [ ] Backtesting histórico avançado

## 📞 Suporte

Para questões técnicas ou suporte:
1. Consultar a documentação completa
2. Verificar logs do sistema no terminal
3. Confirmar configuração da API
4. Validar conectividade à internet

---

**Desenvolvido com ❤️ para análise estatística de futebol**

*Versão 1.0 - Junho 2025*

