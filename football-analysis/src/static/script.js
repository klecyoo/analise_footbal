// Configuração da API
const API_BASE_URL = '/api';

// Estado global da aplicação
let appState = {
    teams: [],
    matches: [],
    currentSection: 'dashboard',
    loading: false
};

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadDashboardData();
});

function initializeApp() {
    // Configurar navegação
    setupNavigation();
    
    // Carregar dados iniciais
    loadTeams();
    loadMatches();
    
    // Configurar gráficos
    setupCharts();
}

function setupEventListeners() {
    // Pesquisa de equipas
    const teamSearch = document.getElementById('team-search');
    if (teamSearch) {
        teamSearch.addEventListener('input', filterTeams);
    }
    
    // Filtros de partidas
    const championshipFilter = document.getElementById('championship-filter');
    const statusFilter = document.getElementById('status-filter');
    
    if (championshipFilter) {
        championshipFilter.addEventListener('change', filterMatches);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterMatches);
    }
    
    // Seletores de equipas para análise
    loadTeamSelectors();
}

function setupNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const section = this.dataset.section;
            switchSection(section);
            
            // Atualizar menu ativo
            menuItems.forEach(mi => mi.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function switchSection(section) {
    // Esconder todas as seções
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(s => s.classList.remove('active'));
    
    // Mostrar seção ativa
    const activeSection = document.getElementById(`${section}-section`);
    if (activeSection) {
        activeSection.classList.add('active');
    }
    
    // Atualizar título
    updatePageTitle(section);
    
    // Carregar dados específicos da seção
    loadSectionData(section);
    
    appState.currentSection = section;
}

function updatePageTitle(section) {
    const titles = {
        dashboard: { title: 'Dashboard', subtitle: 'Visão geral do sistema de análise' },
        teams: { title: 'Equipas', subtitle: 'Gestão e análise de equipas' },
        matches: { title: 'Partidas', subtitle: 'Histórico e próximas partidas' },
        odds125: { title: 'Odds 1.25', subtitle: 'Oportunidades de apostas confiáveis' },
        analysis: { title: 'Análise Avançada', subtitle: 'Análise detalhada de confrontos' },
        performance: { title: 'Performance', subtitle: 'Métricas e tendências' }
    };
    
    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');
    
    if (pageTitle && titles[section]) {
        pageTitle.textContent = titles[section].title;
        pageSubtitle.textContent = titles[section].subtitle;
    }
}

function loadSectionData(section) {
    switch (section) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'teams':
            displayTeams();
            break;
        case 'matches':
            displayMatches();
            break;
        case 'odds125':
            loadMarketAnalysis();
            break;
        case 'performance':
            loadPerformanceData();
            break;
    }
}

// Funções de carregamento de dados
async function loadDashboardData() {
    try {
        showLoading();
        
        // Carregar estatísticas gerais
        const [teamsResponse, matchesResponse, performanceResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/football/teams`),
            fetch(`${API_BASE_URL}/football/matches`),
            fetch(`${API_BASE_URL}/odds/performance-tracking`)
        ]);
        
        const teams = await teamsResponse.json();
        const matches = await matchesResponse.json();
        const performance = await performanceResponse.json();
        
        // Atualizar estatísticas
        updateDashboardStats(teams, matches, performance);
        
        // Carregar oportunidades de hoje
        loadTodayOpportunities();
        
        hideLoading();
    } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        showToast('Erro ao carregar dados do dashboard', 'error');
        hideLoading();
    }
}

function updateDashboardStats(teams, matches, performance) {
    document.getElementById('total-teams').textContent = teams.length || 0;
    document.getElementById('total-matches').textContent = matches.length || 0;
    
    if (performance.overall_metrics) {
        document.getElementById('success-rate').textContent = `${performance.overall_metrics.win_rate || 0}%`;
        document.getElementById('roi').textContent = `${performance.overall_metrics.roi || 0}%`;
    }
}

async function loadTodayOpportunities() {
    try {
        const response = await fetch(`${API_BASE_URL}/odds/daily-recommendations`);
        const data = await response.json();
        
        const container = document.getElementById('today-opportunities');
        
        if (data.recommendations && data.recommendations.length > 0) {
            container.innerHTML = data.recommendations.map(rec => `
                <div class="recommendation-item">
                    <div class="recommendation-header">
                        <span class="recommendation-match">${rec.match}</span>
                        <span class="confidence-badge confidence-${rec.confidence >= 85 ? 'high' : rec.confidence >= 80 ? 'medium' : 'low'}">
                            ${rec.confidence}%
                        </span>
                    </div>
                    <div class="recommendation-details">
                        <span>Tipo: ${rec.bet_type}</span>
                        <span>Stake: €${rec.stake}</span>
                        <span>Lucro: €${rec.potential_profit}</span>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-search"></i>
                    <p>Nenhuma oportunidade encontrada para hoje</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Erro ao carregar oportunidades:', error);
        document.getElementById('today-opportunities').innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Erro ao carregar oportunidades</p>
            </div>
        `;
    }
}

async function loadTeams() {
    try {
        const response = await fetch(`${API_BASE_URL}/football/teams`);
        const teams = await response.json();
        appState.teams = teams;
        
        if (appState.currentSection === 'teams') {
            displayTeams();
        }
    } catch (error) {
        console.error('Erro ao carregar equipas:', error);
        showToast('Erro ao carregar equipas', 'error');
    }
}

function displayTeams() {
    const container = document.getElementById('teams-grid');
    
    if (appState.teams.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-users"></i>
                <p>Nenhuma equipa encontrada. Sincronize os dados primeiro.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = appState.teams.map(team => `
        <div class="team-card">
            <div class="team-header">
                <div class="team-logo">
                    ${team.logo_url ? `<img src="${team.logo_url}" alt="${team.name}" style="width: 100%; height: 100%; object-fit: contain;">` : '<i class="fas fa-shield-alt"></i>'}
                </div>
                <div class="team-info">
                    <h3>${team.popular_name}</h3>
                    <p>${team.abbreviation}</p>
                </div>
            </div>
            <div class="team-stats">
                <div class="team-stat">
                    <div class="value">${team.stats ? team.stats.matches_played : 0}</div>
                    <div class="label">Jogos</div>
                </div>
                <div class="team-stat">
                    <div class="value">${team.stats ? team.stats.win_percentage : 0}%</div>
                    <div class="label">Vitórias</div>
                </div>
                <div class="team-stat">
                    <div class="value">${team.stats ? team.stats.goals_per_match : 0}</div>
                    <div class="label">Golos/Jogo</div>
                </div>
                <div class="team-stat">
                    <div class="value">${team.stats ? team.stats.goals_conceded_per_match : 0}</div>
                    <div class="label">Sofridos/Jogo</div>
                </div>
            </div>
        </div>
    `).join('');
}

function filterTeams() {
    const search = document.getElementById('team-search').value.toLowerCase();
    const filteredTeams = appState.teams.filter(team => 
        team.popular_name.toLowerCase().includes(search) ||
        team.name.toLowerCase().includes(search) ||
        team.abbreviation.toLowerCase().includes(search)
    );
    
    const container = document.getElementById('teams-grid');
    container.innerHTML = filteredTeams.map(team => `
        <div class="team-card">
            <div class="team-header">
                <div class="team-logo">
                    ${team.logo_url ? `<img src="${team.logo_url}" alt="${team.name}" style="width: 100%; height: 100%; object-fit: contain;">` : '<i class="fas fa-shield-alt"></i>'}
                </div>
                <div class="team-info">
                    <h3>${team.popular_name}</h3>
                    <p>${team.abbreviation}</p>
                </div>
            </div>
            <div class="team-stats">
                <div class="team-stat">
                    <div class="value">${team.stats ? team.stats.matches_played : 0}</div>
                    <div class="label">Jogos</div>
                </div>
                <div class="team-stat">
                    <div class="value">${team.stats ? team.stats.win_percentage : 0}%</div>
                    <div class="label">Vitórias</div>
                </div>
                <div class="team-stat">
                    <div class="value">${team.stats ? team.stats.goals_per_match : 0}</div>
                    <div class="label">Golos/Jogo</div>
                </div>
                <div class="team-stat">
                    <div class="value">${team.stats ? team.stats.goals_conceded_per_match : 0}</div>
                    <div class="label">Sofridos/Jogo</div>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadMatches() {
    try {
        const response = await fetch(`${API_BASE_URL}/football/matches`);
        const matches = await response.json();
        appState.matches = matches;
        
        if (appState.currentSection === 'matches') {
            displayMatches();
        }
    } catch (error) {
        console.error('Erro ao carregar partidas:', error);
        showToast('Erro ao carregar partidas', 'error');
    }
}

function displayMatches() {
    const tbody = document.getElementById('matches-tbody');
    
    if (appState.matches.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="empty-state">
                    <i class="fas fa-calendar-alt"></i>
                    <p>Nenhuma partida encontrada. Sincronize os dados primeiro.</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = appState.matches.map(match => `
        <tr>
            <td>${match.match_date ? new Date(match.match_date).toLocaleDateString('pt-PT') : 'N/A'}</td>
            <td>${match.home_team}</td>
            <td class="text-center">
                ${match.status === 'finalizado' ? `${match.home_score} - ${match.away_score}` : '-'}
            </td>
            <td>${match.away_team}</td>
            <td>${match.championship_name}</td>
            <td>
                <span class="badge ${getStatusClass(match.status)}">${match.status}</span>
            </td>
            <td>
                <button class="btn btn-sm btn-secondary" onclick="analyzeSpecificMatch(${match.api_id})">
                    <i class="fas fa-analytics"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function getStatusClass(status) {
    switch (status) {
        case 'finalizado': return 'badge-success';
        case 'ao-vivo': return 'badge-warning';
        case 'agendado': return 'badge-info';
        default: return 'badge-secondary';
    }
}

function filterMatches() {
    // Implementar filtros de partidas
    const championship = document.getElementById('championship-filter').value;
    const status = document.getElementById('status-filter').value;
    
    let filteredMatches = appState.matches;
    
    if (championship) {
        filteredMatches = filteredMatches.filter(match => 
            match.championship_name.includes(championship)
        );
    }
    
    if (status) {
        filteredMatches = filteredMatches.filter(match => match.status === status);
    }
    
    // Atualizar tabela com partidas filtradas
    const tbody = document.getElementById('matches-tbody');
    tbody.innerHTML = filteredMatches.map(match => `
        <tr>
            <td>${match.match_date ? new Date(match.match_date).toLocaleDateString('pt-PT') : 'N/A'}</td>
            <td>${match.home_team}</td>
            <td class="text-center">
                ${match.status === 'finalizado' ? `${match.home_score} - ${match.away_score}` : '-'}
            </td>
            <td>${match.away_team}</td>
            <td>${match.championship_name}</td>
            <td>
                <span class="badge ${getStatusClass(match.status)}">${match.status}</span>
            </td>
            <td>
                <button class="btn btn-sm btn-secondary" onclick="analyzeSpecificMatch(${match.api_id})">
                    <i class="fas fa-analytics"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Funções de Odds 1.25
async function findOdds125Opportunities() {
    try {
        showLoading();
        
        const championshipId = document.getElementById('odds-championship').value;
        const payload = {};
        
        if (championshipId) {
            payload.championship_id = parseInt(championshipId);
        }
        
        const response = await fetch(`${API_BASE_URL}/odds/find-125-opportunities`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (data.high_confidence_bets) {
            displayOddsOpportunities(data.high_confidence_bets);
            document.getElementById('recommendations-count').textContent = data.high_confidence_bets.length;
        }
        
        hideLoading();
        showToast('Oportunidades atualizadas com sucesso', 'success');
    } catch (error) {
        console.error('Erro ao buscar oportunidades:', error);
        showToast('Erro ao buscar oportunidades', 'error');
        hideLoading();
    }
}

function displayOddsOpportunities(opportunities) {
    const container = document.getElementById('daily-recommendations');
    
    if (opportunities.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <p>Nenhuma oportunidade encontrada com alta confiança</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = opportunities.map(opp => `
        <div class="recommendation-item">
            <div class="recommendation-header">
                <span class="recommendation-match">${opp.match}</span>
                <span class="confidence-badge confidence-${opp.confidence >= 85 ? 'high' : opp.confidence >= 80 ? 'medium' : 'low'}">
                    ${opp.confidence}%
                </span>
            </div>
            <div class="recommendation-details">
                <span>Tipo: ${opp.recommended_bet}</span>
                <span>Valor Esperado: ${opp.expected_value}%</span>
                <span>Risco: ${opp.risk_level}</span>
            </div>
            <div class="recommendation-factors">
                <small>${opp.supporting_factors.join(', ')}</small>
            </div>
        </div>
    `).join('');
}

function calculateBet() {
    const stake = parseFloat(document.getElementById('calc-stake').value) || 0;
    const confidence = parseFloat(document.getElementById('calc-confidence').value) || 0;
    
    if (stake <= 0 || confidence <= 0) {
        showToast('Por favor, insira valores válidos', 'warning');
        return;
    }
    
    const odds = 1.25;
    const potentialProfit = stake * (odds - 1);
    const confidenceDecimal = confidence / 100;
    const expectedValue = (confidenceDecimal * potentialProfit) - ((1 - confidenceDecimal) * stake);
    const roi = (expectedValue / stake) * 100;
    
    // Mostrar resultados
    document.getElementById('calc-profit').textContent = `€${potentialProfit.toFixed(2)}`;
    document.getElementById('calc-ev').textContent = `€${expectedValue.toFixed(2)}`;
    document.getElementById('calc-roi').textContent = `${roi.toFixed(2)}%`;
    
    document.getElementById('calc-results').style.display = 'block';
}

async function loadMarketAnalysis() {
    try {
        const response = await fetch(`${API_BASE_URL}/odds/market-analysis`);
        const data = await response.json();
        
        const container = document.getElementById('market-analysis');
        
        if (data.identified_patterns) {
            container.innerHTML = `
                <div class="market-stats">
                    <h4>Estatísticas do Mercado (${data.analysis_period})</h4>
                    <div class="stats-row">
                        <div class="stat">
                            <span class="label">Vitórias Casa:</span>
                            <span class="value">${data.market_statistics.home_win_percentage}%</span>
                        </div>
                        <div class="stat">
                            <span class="label">Empates:</span>
                            <span class="value">${data.market_statistics.draw_percentage}%</span>
                        </div>
                        <div class="stat">
                            <span class="label">Vitórias Fora:</span>
                            <span class="value">${data.market_statistics.away_win_percentage}%</span>
                        </div>
                        <div class="stat">
                            <span class="label">Golos/Jogo:</span>
                            <span class="value">${data.market_statistics.average_goals_per_match}</span>
                        </div>
                    </div>
                </div>
                
                <div class="market-patterns">
                    <h4>Padrões Identificados</h4>
                    ${data.identified_patterns.map(pattern => `
                        <div class="pattern-item">
                            <div class="pattern-header">
                                <span class="pattern-name">${pattern.pattern}</span>
                                <span class="pattern-confidence confidence-${pattern.confidence.toLowerCase()}">${pattern.confidence}</span>
                            </div>
                            <div class="pattern-details">
                                <p><strong>Percentagem:</strong> ${pattern.percentage}%</p>
                                <p><strong>Oportunidade:</strong> ${pattern.opportunity}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <div class="market-recommendation">
                    <h4>Recomendação Geral</h4>
                    <p>${data.market_opportunities.recommendation}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Erro ao carregar análise de mercado:', error);
        document.getElementById('market-analysis').innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Erro ao carregar análise de mercado</p>
            </div>
        `;
    }
}

// Funções de Análise Avançada
async function loadTeamSelectors() {
    try {
        const response = await fetch(`${API_BASE_URL}/football/teams`);
        const teams = await response.json();
        
        const homeSelect = document.getElementById('home-team-select');
        const awaySelect = document.getElementById('away-team-select');
        
        if (homeSelect && awaySelect) {
            const options = teams.map(team => 
                `<option value="${team.api_id}">${team.popular_name}</option>`
            ).join('');
            
            homeSelect.innerHTML = '<option value="">Selecionar equipa...</option>' + options;
            awaySelect.innerHTML = '<option value="">Selecionar equipa...</option>' + options;
        }
    } catch (error) {
        console.error('Erro ao carregar seletores de equipas:', error);
    }
}

async function analyzeMatch() {
    const homeTeamId = document.getElementById('home-team-select').value;
    const awayTeamId = document.getElementById('away-team-select').value;
    
    if (!homeTeamId || !awayTeamId) {
        showToast('Por favor, selecione ambas as equipas', 'warning');
        return;
    }
    
    if (homeTeamId === awayTeamId) {
        showToast('Por favor, selecione equipas diferentes', 'warning');
        return;
    }
    
    try {
        showLoading();
        
        const response = await fetch(`${API_BASE_URL}/advanced/analyze-match`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                home_team_id: parseInt(homeTeamId),
                away_team_id: parseInt(awayTeamId)
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showToast(data.error, 'error');
            hideLoading();
            return;
        }
        
        displayMatchAnalysis(data);
        document.getElementById('match-analysis-results').style.display = 'block';
        
        hideLoading();
        showToast('Análise concluída com sucesso', 'success');
    } catch (error) {
        console.error('Erro ao analisar partida:', error);
        showToast('Erro ao analisar partida', 'error');
        hideLoading();
    }
}

function displayMatchAnalysis(data) {
    // Probabilidades
    const probabilityBars = document.getElementById('probability-bars');
    probabilityBars.innerHTML = `
        <div class="probability-bar">
            <div class="probability-label">
                <span>Vitória ${data.match_info.home_team}</span>
                <span>${data.match_probabilities.home_win}%</span>
            </div>
            <div class="probability-track">
                <div class="probability-fill" style="width: ${data.match_probabilities.home_win}%"></div>
            </div>
        </div>
        <div class="probability-bar">
            <div class="probability-label">
                <span>Empate</span>
                <span>${data.match_probabilities.draw}%</span>
            </div>
            <div class="probability-track">
                <div class="probability-fill" style="width: ${data.match_probabilities.draw}%"></div>
            </div>
        </div>
        <div class="probability-bar">
            <div class="probability-label">
                <span>Vitória ${data.match_info.away_team}</span>
                <span>${data.match_probabilities.away_win}%</span>
            </div>
            <div class="probability-track">
                <div class="probability-fill" style="width: ${data.match_probabilities.away_win}%"></div>
            </div>
        </div>
    `;
    
    // Métricas das equipas
    const teamMetrics = document.getElementById('team-metrics');
    teamMetrics.innerHTML = `
        <div class="team-comparison-grid">
            <div class="team-column">
                <h4>${data.match_info.home_team}</h4>
                <div class="metric-item">
                    <span>Rating ELO:</span>
                    <span>${data.home_team_metrics.elo_rating}</span>
                </div>
                <div class="metric-item">
                    <span>Forma:</span>
                    <span>${(data.home_team_metrics.form_index * 100).toFixed(1)}%</span>
                </div>
                <div class="metric-item">
                    <span>Golos/Jogo:</span>
                    <span>${data.home_team_metrics.goals_per_match}</span>
                </div>
                <div class="metric-item">
                    <span>Sofridos/Jogo:</span>
                    <span>${data.home_team_metrics.goals_conceded_per_match}</span>
                </div>
            </div>
            <div class="team-column">
                <h4>${data.match_info.away_team}</h4>
                <div class="metric-item">
                    <span>Rating ELO:</span>
                    <span>${data.away_team_metrics.elo_rating}</span>
                </div>
                <div class="metric-item">
                    <span>Forma:</span>
                    <span>${(data.away_team_metrics.form_index * 100).toFixed(1)}%</span>
                </div>
                <div class="metric-item">
                    <span>Golos/Jogo:</span>
                    <span>${data.away_team_metrics.goals_per_match}</span>
                </div>
                <div class="metric-item">
                    <span>Sofridos/Jogo:</span>
                    <span>${data.away_team_metrics.goals_conceded_per_match}</span>
                </div>
            </div>
        </div>
    `;
    
    // Recomendação
    const recommendation = document.getElementById('match-recommendation');
    if (data.recommendation) {
        recommendation.innerHTML = `
            <div class="recommendation-card">
                <h4>Aposta Recomendada</h4>
                <div class="rec-details">
                    <p><strong>Tipo:</strong> ${data.recommendation.outcome}</p>
                    <p><strong>Confiança:</strong> ${(data.recommendation.confidence * 100).toFixed(1)}%</p>
                    <p><strong>Odds:</strong> ${data.recommendation.odds}</p>
                    <p><strong>Valor Esperado:</strong> ${(data.recommendation.expected_value * 100).toFixed(2)}%</p>
                </div>
            </div>
        `;
    } else {
        recommendation.innerHTML = `
            <div class="no-recommendation">
                <p>Nenhuma aposta recomendada com confiança suficiente para odds 1.25</p>
            </div>
        `;
    }
}

// Funções de Performance
async function loadPerformanceData() {
    try {
        const response = await fetch(`${API_BASE_URL}/odds/performance-tracking`);
        const data = await response.json();
        
        if (data.overall_metrics) {
            displayPerformanceMetrics(data.overall_metrics);
        }
    } catch (error) {
        console.error('Erro ao carregar dados de performance:', error);
        showToast('Erro ao carregar dados de performance', 'error');
    }
}

function displayPerformanceMetrics(metrics) {
    const container = document.getElementById('performance-metrics');
    
    container.innerHTML = `
        <div class="metric-item">
            <div class="metric-value">${metrics.total_predictions}</div>
            <div class="metric-label">Previsões</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">${metrics.win_rate}%</div>
            <div class="metric-label">Taxa de Acerto</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">${metrics.roi}%</div>
            <div class="metric-label">ROI</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">€${metrics.profit_loss}</div>
            <div class="metric-label">Lucro/Prejuízo</div>
        </div>
    `;
}

// Funções de sincronização
async function syncData() {
    try {
        showLoading();
        showToast('Iniciando sincronização de dados...', 'info');
        
        // Sincronizar campeonatos principais (IDs de exemplo)
        const championshipIds = [2, 6, 10]; // Copa do Brasil, Carioca, etc.
        
        for (const id of championshipIds) {
            try {
                const response = await fetch(`${API_BASE_URL}/football/sync-championship/${id}`, {
                    method: 'POST'
                });
                
                if (response.ok) {
                    const result = await response.json();
                    showToast(`Campeonato ${id}: ${result.teams_synced} equipas, ${result.matches_synced} partidas`, 'success');
                }
            } catch (error) {
                console.error(`Erro ao sincronizar campeonato ${id}:`, error);
            }
        }
        
        // Calcular estatísticas
        await calculateAllStats();
        
        // Recarregar dados
        await loadTeams();
        await loadMatches();
        await loadDashboardData();
        
        hideLoading();
        showToast('Sincronização concluída com sucesso!', 'success');
    } catch (error) {
        console.error('Erro na sincronização:', error);
        showToast('Erro durante a sincronização', 'error');
        hideLoading();
    }
}

async function calculateAllStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/football/calculate-stats`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const result = await response.json();
            showToast(`Estatísticas calculadas para ${result.teams_updated} equipas`, 'success');
        }
    } catch (error) {
        console.error('Erro ao calcular estatísticas:', error);
        showToast('Erro ao calcular estatísticas', 'error');
    }
}

// Funções de UI
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
    appState.loading = true;
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
    appState.loading = false;
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    container.appendChild(toast);
    
    // Remover após 5 segundos
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function getToastIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        default: return 'info-circle';
    }
}

function refreshOpportunities() {
    loadTodayOpportunities();
}

function analyzeSpecificMatch(matchId) {
    // Implementar análise de partida específica
    showToast('Funcionalidade em desenvolvimento', 'info');
}

// Configuração de gráficos
function setupCharts() {
    // Gráfico de performance no dashboard
    const performanceCtx = document.getElementById('performance-chart');
    if (performanceCtx) {
        new Chart(performanceCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                datasets: [{
                    label: 'Taxa de Acerto (%)',
                    data: [75, 78, 82, 79, 85, 83],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Gráfico de tendências na seção de performance
    const trendsCtx = document.getElementById('trends-chart');
    if (trendsCtx) {
        new Chart(trendsCtx, {
            type: 'bar',
            data: {
                labels: ['Vitória Casa', 'Empate', 'Vitória Fora', 'Over 2.5', 'BTTS'],
                datasets: [{
                    label: 'Taxa de Sucesso (%)',
                    data: [82, 65, 71, 78, 85],
                    backgroundColor: [
                        '#10b981',
                        '#f59e0b',
                        '#ef4444',
                        '#3b82f6',
                        '#8b5cf6'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

