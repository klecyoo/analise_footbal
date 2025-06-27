import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from src.models.football import Match, Team, TeamStats
import math

class AdvancedStatsCalculator:
    """Classe para cálculos estatísticos avançados de futebol"""
    
    @staticmethod
    def calculate_elo_rating(team_matches: List[Dict], initial_rating: float = 1500) -> float:
        """
        Calcula o rating ELO de uma equipa baseado nos seus jogos
        Sistema ELO adaptado para futebol
        """
        current_rating = initial_rating
        k_factor = 32  # Fator K para futebol
        
        for match in sorted(team_matches, key=lambda x: x.get('match_date', datetime.min)):
            if match['status'] != 'finalizado':
                continue
                
            # Determinar se é casa ou fora
            is_home = match.get('is_home', False)
            opponent_rating = match.get('opponent_rating', 1500)
            
            # Calcular resultado esperado
            expected_score = 1 / (1 + 10**((opponent_rating - current_rating) / 400))
            
            # Determinar resultado real
            goals_for = match['goals_for']
            goals_against = match['goals_against']
            
            if goals_for > goals_against:
                actual_score = 1.0  # Vitória
            elif goals_for == goals_against:
                actual_score = 0.5  # Empate
            else:
                actual_score = 0.0  # Derrota
            
            # Atualizar rating
            current_rating += k_factor * (actual_score - expected_score)
        
        return current_rating
    
    @staticmethod
    def calculate_form_index(recent_matches: List[Dict], weight_decay: float = 0.9) -> float:
        """
        Calcula índice de forma baseado nos últimos jogos
        Jogos mais recentes têm maior peso
        """
        if not recent_matches:
            return 0.5
        
        form_score = 0
        total_weight = 0
        
        # Ordenar por data (mais recente primeiro)
        sorted_matches = sorted(recent_matches, 
                              key=lambda x: x.get('match_date', datetime.min), 
                              reverse=True)
        
        for i, match in enumerate(sorted_matches[:10]):  # Últimos 10 jogos
            if match['status'] != 'finalizado':
                continue
                
            weight = weight_decay ** i
            
            goals_for = match['goals_for']
            goals_against = match['goals_against']
            
            # Pontuação baseada no resultado
            if goals_for > goals_against:
                match_score = 1.0  # Vitória
            elif goals_for == goals_against:
                match_score = 0.5  # Empate
            else:
                match_score = 0.0  # Derrota
            
            # Bonus por diferença de golos
            goal_diff_bonus = min(0.2, abs(goals_for - goals_against) * 0.05)
            if goals_for > goals_against:
                match_score += goal_diff_bonus
            
            form_score += match_score * weight
            total_weight += weight
        
        return form_score / total_weight if total_weight > 0 else 0.5
    
    @staticmethod
    def calculate_attacking_efficiency(matches: List[Dict]) -> Dict[str, float]:
        """Calcula eficiência ofensiva da equipa"""
        if not matches:
            return {'goals_per_match': 0, 'shots_conversion': 0, 'attacking_third_entries': 0}
        
        total_goals = sum(match['goals_for'] for match in matches if match['status'] == 'finalizado')
        total_matches = len([m for m in matches if m['status'] == 'finalizado'])
        
        goals_per_match = total_goals / total_matches if total_matches > 0 else 0
        
        # Simulação de outras métricas (em implementação real, viriam da API)
        shots_conversion = min(0.3, goals_per_match * 0.15)  # Estimativa
        attacking_third_entries = goals_per_match * 8  # Estimativa
        
        return {
            'goals_per_match': goals_per_match,
            'shots_conversion': shots_conversion,
            'attacking_third_entries': attacking_third_entries
        }
    
    @staticmethod
    def calculate_defensive_solidity(matches: List[Dict]) -> Dict[str, float]:
        """Calcula solidez defensiva da equipa"""
        if not matches:
            return {'goals_conceded_per_match': 0, 'clean_sheets_ratio': 0, 'defensive_actions': 0}
        
        total_conceded = sum(match['goals_against'] for match in matches if match['status'] == 'finalizado')
        total_matches = len([m for m in matches if m['status'] == 'finalizado'])
        clean_sheets = len([m for m in matches if m['status'] == 'finalizado' and m['goals_against'] == 0])
        
        goals_conceded_per_match = total_conceded / total_matches if total_matches > 0 else 0
        clean_sheets_ratio = clean_sheets / total_matches if total_matches > 0 else 0
        
        # Estimativa de ações defensivas
        defensive_actions = max(0, 20 - goals_conceded_per_match * 5)
        
        return {
            'goals_conceded_per_match': goals_conceded_per_match,
            'clean_sheets_ratio': clean_sheets_ratio,
            'defensive_actions': defensive_actions
        }
    
    @staticmethod
    def calculate_head_to_head_record(team1_id: int, team2_id: int, matches: List[Dict]) -> Dict[str, any]:
        """Calcula histórico de confrontos diretos entre duas equipas"""
        h2h_matches = [
            m for m in matches 
            if ((m['home_team_id'] == team1_id and m['away_team_id'] == team2_id) or
                (m['home_team_id'] == team2_id and m['away_team_id'] == team1_id)) and
            m['status'] == 'finalizado'
        ]
        
        if not h2h_matches:
            return {'total_matches': 0, 'team1_wins': 0, 'team2_wins': 0, 'draws': 0, 'advantage': 'neutral'}
        
        team1_wins = 0
        team2_wins = 0
        draws = 0
        
        for match in h2h_matches:
            if match['home_team_id'] == team1_id:
                if match['home_score'] > match['away_score']:
                    team1_wins += 1
                elif match['home_score'] < match['away_score']:
                    team2_wins += 1
                else:
                    draws += 1
            else:
                if match['away_score'] > match['home_score']:
                    team1_wins += 1
                elif match['away_score'] < match['home_score']:
                    team2_wins += 1
                else:
                    draws += 1
        
        # Determinar vantagem
        if team1_wins > team2_wins:
            advantage = 'team1'
        elif team2_wins > team1_wins:
            advantage = 'team2'
        else:
            advantage = 'neutral'
        
        return {
            'total_matches': len(h2h_matches),
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'draws': draws,
            'advantage': advantage
        }
    
    @staticmethod
    def calculate_home_away_performance(matches: List[Dict]) -> Dict[str, Dict[str, float]]:
        """Calcula performance em casa vs fora"""
        home_matches = [m for m in matches if m.get('is_home', False) and m['status'] == 'finalizado']
        away_matches = [m for m in matches if not m.get('is_home', False) and m['status'] == 'finalizado']
        
        def calculate_performance(match_list):
            if not match_list:
                return {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0, 'points_per_match': 0}
            
            wins = sum(1 for m in match_list if m['goals_for'] > m['goals_against'])
            draws = sum(1 for m in match_list if m['goals_for'] == m['goals_against'])
            losses = sum(1 for m in match_list if m['goals_for'] < m['goals_against'])
            goals_for = sum(m['goals_for'] for m in match_list)
            goals_against = sum(m['goals_against'] for m in match_list)
            
            points = wins * 3 + draws * 1
            points_per_match = points / len(match_list)
            
            return {
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'points_per_match': points_per_match
            }
        
        return {
            'home': calculate_performance(home_matches),
            'away': calculate_performance(away_matches)
        }

class PredictionEngine:
    """Motor de previsões avançado"""
    
    def __init__(self):
        self.stats_calculator = AdvancedStatsCalculator()
    
    def calculate_match_probability(self, home_team_data: Dict, away_team_data: Dict, 
                                  h2h_data: Dict = None) -> Dict[str, float]:
        """
        Calcula probabilidades de resultado de uma partida
        Retorna probabilidades para vitória casa, empate, vitória fora
        """
        
        # Fatores base
        home_strength = home_team_data.get('elo_rating', 1500)
        away_strength = away_team_data.get('elo_rating', 1500)
        
        # Vantagem de jogar em casa
        home_advantage = 50
        home_strength += home_advantage
        
        # Forma recente
        home_form = home_team_data.get('form_index', 0.5)
        away_form = away_team_data.get('form_index', 0.5)
        
        # Ajuste baseado na forma
        form_adjustment = (home_form - away_form) * 100
        home_strength += form_adjustment
        
        # Histórico de confrontos diretos
        if h2h_data and h2h_data['total_matches'] > 0:
            if h2h_data['advantage'] == 'team1':  # home team
                home_strength += 25
            elif h2h_data['advantage'] == 'team2':  # away team
                away_strength += 25
        
        # Calcular probabilidades usando distribuição logística
        strength_diff = home_strength - away_strength
        
        # Probabilidade de vitória em casa
        home_win_prob = 1 / (1 + math.exp(-strength_diff / 400))
        
        # Ajustar para incluir empates (aproximadamente 25% dos jogos)
        draw_prob = 0.25
        home_win_prob = home_win_prob * (1 - draw_prob)
        away_win_prob = (1 - home_win_prob - draw_prob)
        
        # Normalizar para somar 1
        total = home_win_prob + draw_prob + away_win_prob
        
        return {
            'home_win': home_win_prob / total,
            'draw': draw_prob / total,
            'away_win': away_win_prob / total
        }
    
    def find_value_bets(self, probabilities: Dict[str, float], target_odds: float = 1.25) -> List[Dict]:
        """
        Encontra apostas com valor baseado nas probabilidades calculadas
        Procura por odds que ofereçam valor esperado positivo
        """
        value_bets = []
        
        # Probabilidade implícita das odds alvo
        implied_prob = 1 / target_odds
        
        for outcome, prob in probabilities.items():
            if prob > implied_prob:
                # Encontrou valor
                expected_value = (prob * (target_odds - 1)) - (1 - prob)
                confidence = (prob - implied_prob) / implied_prob * 100
                
                value_bets.append({
                    'outcome': outcome,
                    'probability': prob,
                    'odds': target_odds,
                    'expected_value': expected_value,
                    'confidence': confidence,
                    'recommended': expected_value > 0.05  # Pelo menos 5% de valor esperado
                })
        
        return sorted(value_bets, key=lambda x: x['expected_value'], reverse=True)
    
    def generate_comprehensive_analysis(self, home_team_id: int, away_team_id: int, 
                                     all_matches: List[Dict]) -> Dict:
        """Gera análise completa de uma partida"""
        
        # Filtrar jogos de cada equipa
        home_matches = [m for m in all_matches if m['home_team_id'] == home_team_id or m['away_team_id'] == home_team_id]
        away_matches = [m for m in all_matches if m['home_team_id'] == away_team_id or m['away_team_id'] == away_team_id]
        
        # Preparar dados dos jogos para análise
        def prepare_match_data(matches, team_id):
            prepared = []
            for match in matches:
                is_home = match['home_team_id'] == team_id
                prepared.append({
                    'is_home': is_home,
                    'goals_for': match['home_score'] if is_home else match['away_score'],
                    'goals_against': match['away_score'] if is_home else match['home_score'],
                    'status': match['status'],
                    'match_date': match.get('match_date', datetime.now())
                })
            return prepared
        
        home_prepared = prepare_match_data(home_matches, home_team_id)
        away_prepared = prepare_match_data(away_matches, away_team_id)
        
        # Calcular métricas avançadas
        home_elo = self.stats_calculator.calculate_elo_rating(home_prepared[-20:])  # Últimos 20 jogos
        away_elo = self.stats_calculator.calculate_elo_rating(away_prepared[-20:])
        
        home_form = self.stats_calculator.calculate_form_index(home_prepared[-10:])  # Últimos 10 jogos
        away_form = self.stats_calculator.calculate_form_index(away_prepared[-10:])
        
        home_attack = self.stats_calculator.calculate_attacking_efficiency(home_prepared)
        away_attack = self.stats_calculator.calculate_attacking_efficiency(away_prepared)
        
        home_defense = self.stats_calculator.calculate_defensive_solidity(home_prepared)
        away_defense = self.stats_calculator.calculate_defensive_solidity(away_prepared)
        
        home_performance = self.stats_calculator.calculate_home_away_performance(home_prepared)
        away_performance = self.stats_calculator.calculate_home_away_performance(away_prepared)
        
        h2h_record = self.stats_calculator.calculate_head_to_head_record(home_team_id, away_team_id, all_matches)
        
        # Dados das equipas para previsão
        home_team_data = {
            'elo_rating': home_elo,
            'form_index': home_form,
            'attacking_efficiency': home_attack,
            'defensive_solidity': home_defense,
            'home_performance': home_performance['home']
        }
        
        away_team_data = {
            'elo_rating': away_elo,
            'form_index': away_form,
            'attacking_efficiency': away_attack,
            'defensive_solidity': away_defense,
            'away_performance': away_performance['away']
        }
        
        # Calcular probabilidades
        probabilities = self.calculate_match_probability(home_team_data, away_team_data, h2h_record)
        
        # Encontrar apostas de valor
        value_bets = self.find_value_bets(probabilities, 1.25)
        
        return {
            'home_team_analysis': home_team_data,
            'away_team_analysis': away_team_data,
            'head_to_head': h2h_record,
            'match_probabilities': probabilities,
            'value_bets': value_bets,
            'recommendation': value_bets[0] if value_bets and value_bets[0]['recommended'] else None
        }

