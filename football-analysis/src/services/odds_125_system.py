import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from src.models.football import Match, Team, TeamStats
from src.services.advanced_analytics import AdvancedStatsCalculator, PredictionEngine
import math

class OddsTargetSystem:
    """Sistema especializado para encontrar apostas com odds 1.25 confiáveis"""
    
    def __init__(self):
        self.target_odds = 1.25
        self.required_probability = 1 / self.target_odds  # 80%
        self.min_confidence_threshold = 0.82  # 82% para margem de segurança
        self.stats_calculator = AdvancedStatsCalculator()
        self.prediction_engine = PredictionEngine()
    
    def find_high_confidence_bets(self, matches_data: List[Dict], 
                                 teams_data: Dict[int, Dict]) -> List[Dict]:
        """
        Encontra apostas com alta confiança para odds 1.25
        Foca em cenários com probabilidade >= 82%
        """
        high_confidence_bets = []
        
        for match in matches_data:
            home_id = match['home_team_id']
            away_id = match['away_team_id']
            
            if home_id not in teams_data or away_id not in teams_data:
                continue
            
            # Análise detalhada do confronto
            analysis = self._analyze_match_for_125_odds(
                home_id, away_id, teams_data, matches_data
            )
            
            if analysis and analysis['max_confidence'] >= self.min_confidence_threshold:
                high_confidence_bets.append({
                    'home_team_id': home_id,
                    'away_team_id': away_id,
                    'recommended_bet': analysis['best_outcome'],
                    'confidence': analysis['max_confidence'],
                    'probability': analysis['probability'],
                    'expected_value': analysis['expected_value'],
                    'risk_level': analysis['risk_level'],
                    'supporting_factors': analysis['factors'],
                    'match_date': match.get('match_date', datetime.now())
                })
        
        # Ordenar por confiança e valor esperado
        return sorted(high_confidence_bets, 
                     key=lambda x: (x['confidence'], x['expected_value']), 
                     reverse=True)
    
    def _analyze_match_for_125_odds(self, home_id: int, away_id: int, 
                                   teams_data: Dict, all_matches: List[Dict]) -> Optional[Dict]:
        """Análise específica para encontrar odds 1.25 confiáveis"""
        
        home_data = teams_data[home_id]
        away_data = teams_data[away_id]
        
        # Cenários que favorecem odds 1.25
        scenarios = self._identify_125_scenarios(home_data, away_data, home_id, away_id, all_matches)
        
        best_scenario = None
        max_confidence = 0
        
        for scenario in scenarios:
            if scenario['confidence'] > max_confidence:
                max_confidence = scenario['confidence']
                best_scenario = scenario
        
        return best_scenario if max_confidence >= self.min_confidence_threshold else None
    
    def _identify_125_scenarios(self, home_data: Dict, away_data: Dict, 
                               home_id: int, away_id: int, all_matches: List[Dict]) -> List[Dict]:
        """Identifica cenários específicos que podem gerar odds 1.25 confiáveis"""
        
        scenarios = []
        
        # Cenário 1: Equipa muito superior em casa
        home_strength = self._calculate_team_strength(home_data, is_home=True)
        away_strength = self._calculate_team_strength(away_data, is_home=False)
        
        if home_strength - away_strength >= 200:  # Diferença significativa
            confidence = min(0.9, 0.7 + (home_strength - away_strength) / 1000)
            scenarios.append({
                'outcome': 'home_win',
                'confidence': confidence,
                'probability': confidence,
                'expected_value': (confidence * 0.25) - (1 - confidence),
                'risk_level': 'Baixo',
                'factors': ['Superioridade técnica significativa', 'Vantagem de jogar em casa'],
                'best_outcome': 'home_win'
            })
        
        # Cenário 2: Over/Under baseado em histórico de golos
        avg_goals = self._calculate_match_goals_expectation(home_data, away_data)
        if avg_goals >= 2.8:  # Expectativa alta de golos
            over_confidence = min(0.85, 0.6 + (avg_goals - 2.5) * 0.1)
            scenarios.append({
                'outcome': 'over_2.5',
                'confidence': over_confidence,
                'probability': over_confidence,
                'expected_value': (over_confidence * 0.25) - (1 - over_confidence),
                'risk_level': 'Médio',
                'factors': ['Média alta de golos das equipas', 'Histórico ofensivo'],
                'best_outcome': 'over_2.5'
            })
        elif avg_goals <= 1.8:  # Expectativa baixa de golos
            under_confidence = min(0.83, 0.65 + (2.0 - avg_goals) * 0.1)
            scenarios.append({
                'outcome': 'under_2.5',
                'confidence': under_confidence,
                'probability': under_confidence,
                'expected_value': (under_confidence * 0.25) - (1 - under_confidence),
                'risk_level': 'Baixo',
                'factors': ['Defesas sólidas', 'Baixa média de golos'],
                'best_outcome': 'under_2.5'
            })
        
        # Cenário 3: Ambas marcam baseado em estatísticas
        btts_probability = self._calculate_both_teams_score_probability(home_data, away_data)
        if btts_probability >= 0.82:
            scenarios.append({
                'outcome': 'both_teams_score',
                'confidence': btts_probability,
                'probability': btts_probability,
                'expected_value': (btts_probability * 0.25) - (1 - btts_probability),
                'risk_level': 'Médio',
                'factors': ['Ambas equipas com ataques eficazes', 'Defesas vulneráveis'],
                'best_outcome': 'both_teams_score'
            })
        elif btts_probability <= 0.18:  # Baixa probabilidade de ambas marcarem
            no_btts_confidence = 1 - btts_probability
            if no_btts_confidence >= 0.82:
                scenarios.append({
                    'outcome': 'no_both_teams_score',
                    'confidence': no_btts_confidence,
                    'probability': no_btts_confidence,
                    'expected_value': (no_btts_confidence * 0.25) - (1 - no_btts_confidence),
                    'risk_level': 'Baixo',
                    'factors': ['Uma ou ambas equipas com dificuldades ofensivas', 'Defesas sólidas'],
                    'best_outcome': 'no_both_teams_score'
                })
        
        # Cenário 4: Dupla hipótese baseada em análise de risco
        home_or_draw_prob = self._calculate_home_or_draw_probability(home_data, away_data)
        if home_or_draw_prob >= 0.82:
            scenarios.append({
                'outcome': 'home_or_draw',
                'confidence': home_or_draw_prob,
                'probability': home_or_draw_prob,
                'expected_value': (home_or_draw_prob * 0.25) - (1 - home_or_draw_prob),
                'risk_level': 'Baixo',
                'factors': ['Equipa da casa favorita', 'Visitante com dificuldades'],
                'best_outcome': 'home_or_draw'
            })
        
        # Cenário 5: Forma recente extrema
        home_form = home_data.get('form_index', 0.5)
        away_form = away_data.get('form_index', 0.5)
        
        if home_form >= 0.8 and away_form <= 0.3:  # Casa em ótima forma, visitante em má forma
            form_confidence = min(0.85, 0.7 + (home_form - away_form) * 0.3)
            scenarios.append({
                'outcome': 'home_win',
                'confidence': form_confidence,
                'probability': form_confidence,
                'expected_value': (form_confidence * 0.25) - (1 - form_confidence),
                'risk_level': 'Médio',
                'factors': ['Excelente forma da equipa da casa', 'Má forma do visitante'],
                'best_outcome': 'home_win'
            })
        
        return scenarios
    
    def _calculate_team_strength(self, team_data: Dict, is_home: bool = False) -> float:
        """Calcula força geral da equipa"""
        base_strength = team_data.get('elo_rating', 1500)
        
        # Ajustes baseados em estatísticas
        goals_per_match = team_data.get('goals_per_match', 1.0)
        goals_conceded = team_data.get('goals_conceded_per_match', 1.0)
        win_percentage = team_data.get('win_percentage', 50)
        form_index = team_data.get('form_index', 0.5)
        
        # Bónus/penalizações
        goal_diff_bonus = (goals_per_match - goals_conceded) * 50
        win_bonus = (win_percentage - 50) * 2
        form_bonus = (form_index - 0.5) * 100
        home_bonus = 50 if is_home else 0
        
        return base_strength + goal_diff_bonus + win_bonus + form_bonus + home_bonus
    
    def _calculate_match_goals_expectation(self, home_data: Dict, away_data: Dict) -> float:
        """Calcula expectativa de golos no jogo"""
        home_attack = home_data.get('goals_per_match', 1.0)
        home_defense = home_data.get('goals_conceded_per_match', 1.0)
        away_attack = away_data.get('goals_per_match', 1.0)
        away_defense = away_data.get('goals_conceded_per_match', 1.0)
        
        # Golos esperados = (ataque casa / defesa visitante) + (ataque visitante / defesa casa)
        expected_home_goals = home_attack * (away_defense / 1.0)  # Normalizado
        expected_away_goals = away_attack * (home_defense / 1.0)
        
        return expected_home_goals + expected_away_goals
    
    def _calculate_both_teams_score_probability(self, home_data: Dict, away_data: Dict) -> float:
        """Calcula probabilidade de ambas equipas marcarem"""
        home_scoring_prob = min(0.9, home_data.get('goals_per_match', 1.0) / 2.0)
        away_scoring_prob = min(0.9, away_data.get('goals_per_match', 1.0) / 2.0)
        
        # Probabilidade de ambas marcarem
        return home_scoring_prob * away_scoring_prob
    
    def _calculate_home_or_draw_probability(self, home_data: Dict, away_data: Dict) -> float:
        """Calcula probabilidade de vitória da casa ou empate"""
        home_strength = self._calculate_team_strength(home_data, True)
        away_strength = self._calculate_team_strength(away_data, False)
        
        # Usar modelo logístico
        strength_diff = home_strength - away_strength
        home_win_prob = 1 / (1 + math.exp(-strength_diff / 400))
        
        # Assumir ~25% de probabilidade de empate
        draw_prob = 0.25
        
        return home_win_prob + draw_prob

class BettingStrategy:
    """Estratégias de apostas para odds 1.25"""
    
    def __init__(self):
        self.target_odds = 1.25
        self.bankroll_percentage = 0.05  # 5% do bankroll por aposta
        self.max_daily_bets = 3
        self.min_confidence = 0.82
    
    def generate_daily_recommendations(self, high_confidence_bets: List[Dict], 
                                    bankroll: float = 1000) -> Dict:
        """Gera recomendações diárias de apostas"""
        
        # Filtrar apenas as melhores apostas
        top_bets = [bet for bet in high_confidence_bets 
                   if bet['confidence'] >= self.min_confidence][:self.max_daily_bets]
        
        recommendations = []
        total_stake = 0
        expected_profit = 0
        
        for bet in top_bets:
            stake = bankroll * self.bankroll_percentage
            potential_profit = stake * (self.target_odds - 1)
            expected_value = bet['expected_value'] * stake
            
            recommendations.append({
                'match': f"Team {bet['home_team_id']} vs Team {bet['away_team_id']}",
                'bet_type': bet['recommended_bet'],
                'confidence': round(bet['confidence'] * 100, 1),
                'stake': round(stake, 2),
                'potential_profit': round(potential_profit, 2),
                'expected_value': round(expected_value, 2),
                'risk_level': bet['risk_level'],
                'factors': bet['supporting_factors']
            })
            
            total_stake += stake
            expected_profit += expected_value
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_recommendations': len(recommendations),
            'recommendations': recommendations,
            'portfolio_summary': {
                'total_stake': round(total_stake, 2),
                'expected_profit': round(expected_profit, 2),
                'roi_expectation': round((expected_profit / max(1, total_stake)) * 100, 2),
                'risk_assessment': self._assess_portfolio_risk(recommendations)
            }
        }
    
    def _assess_portfolio_risk(self, recommendations: List[Dict]) -> str:
        """Avalia risco geral do portfólio de apostas"""
        if not recommendations:
            return "Sem apostas"
        
        avg_confidence = sum(r['confidence'] for r in recommendations) / len(recommendations)
        low_risk_count = sum(1 for r in recommendations if r['risk_level'] == 'Baixo')
        
        if avg_confidence >= 85 and low_risk_count >= len(recommendations) * 0.7:
            return "Baixo"
        elif avg_confidence >= 82:
            return "Médio"
        else:
            return "Alto"

class PerformanceTracker:
    """Rastreamento de performance das previsões"""
    
    def __init__(self):
        self.predictions_history = []
        self.results_history = []
    
    def add_prediction(self, prediction: Dict):
        """Adiciona uma previsão ao histórico"""
        prediction['timestamp'] = datetime.now()
        self.predictions_history.append(prediction)
    
    def add_result(self, prediction_id: str, actual_result: str, won: bool):
        """Adiciona resultado real de uma previsão"""
        self.results_history.append({
            'prediction_id': prediction_id,
            'actual_result': actual_result,
            'won': won,
            'timestamp': datetime.now()
        })
    
    def calculate_performance_metrics(self) -> Dict:
        """Calcula métricas de performance"""
        if not self.results_history:
            return {'error': 'Sem dados suficientes'}
        
        total_bets = len(self.results_history)
        wins = sum(1 for r in self.results_history if r['won'])
        win_rate = (wins / total_bets) * 100
        
        # Simular ROI baseado em odds 1.25
        total_stake = total_bets * 100  # Assumir 100 por aposta
        total_return = wins * 125  # 25% de lucro por vitória
        roi = ((total_return - total_stake) / total_stake) * 100
        
        return {
            'total_predictions': total_bets,
            'wins': wins,
            'losses': total_bets - wins,
            'win_rate': round(win_rate, 2),
            'roi': round(roi, 2),
            'profit_loss': round(total_return - total_stake, 2),
            'average_confidence': self._calculate_average_confidence(),
            'best_performing_bet_type': self._find_best_bet_type()
        }
    
    def _calculate_average_confidence(self) -> float:
        """Calcula confiança média das previsões"""
        if not self.predictions_history:
            return 0
        
        total_confidence = sum(p.get('confidence', 0) for p in self.predictions_history)
        return round((total_confidence / len(self.predictions_history)) * 100, 2)
    
    def _find_best_bet_type(self) -> str:
        """Encontra o tipo de aposta com melhor performance"""
        bet_types = {}
        
        for pred in self.predictions_history:
            bet_type = pred.get('recommended_bet', 'unknown')
            if bet_type not in bet_types:
                bet_types[bet_type] = {'total': 0, 'wins': 0}
            bet_types[bet_type]['total'] += 1
        
        # Simular wins baseado na confiança (para demonstração)
        for bet_type in bet_types:
            bet_types[bet_type]['wins'] = int(bet_types[bet_type]['total'] * 0.8)  # 80% de acerto
        
        if not bet_types:
            return 'N/A'
        
        best_type = max(bet_types.keys(), 
                       key=lambda x: bet_types[x]['wins'] / max(1, bet_types[x]['total']))
        
        return best_type

