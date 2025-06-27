from flask import Blueprint, request, jsonify
from src.models.football import db, Team, Player, Match, TeamStats, Prediction
from src.services.football_api import FootballAPIService, DataProcessor, StatsCalculator
from src.services.advanced_analytics import AdvancedStatsCalculator, PredictionEngine
from datetime import datetime, timedelta
import os

advanced_bp = Blueprint('advanced', __name__)

# Configuração da API
API_KEY = os.getenv('FOOTBALL_API_KEY', 'test_a8c37778328495ac24c5d0d3c3923b')
api_service = FootballAPIService(API_KEY)
prediction_engine = PredictionEngine()

@advanced_bp.route('/analyze-match', methods=['POST'])
def analyze_match():
    """Análise avançada de uma partida"""
    try:
        data = request.get_json()
        home_team_id = data.get('home_team_id')
        away_team_id = data.get('away_team_id')
        
        if not home_team_id or not away_team_id:
            return jsonify({'error': 'IDs das equipas são obrigatórios'}), 400
        
        # Buscar equipas
        home_team = Team.query.filter_by(api_id=home_team_id).first()
        away_team = Team.query.filter_by(api_id=away_team_id).first()
        
        if not home_team or not away_team:
            return jsonify({'error': 'Equipas não encontradas na base de dados'}), 404
        
        # Buscar todas as partidas para análise
        all_matches = Match.query.all()
        match_dicts = []
        
        for match in all_matches:
            match_dicts.append({
                'home_team_id': match.home_team_id,
                'away_team_id': match.away_team_id,
                'home_score': match.home_score,
                'away_score': match.away_score,
                'status': match.status,
                'match_date': match.match_date
            })
        
        # Gerar análise completa
        analysis = prediction_engine.generate_comprehensive_analysis(
            home_team_id, away_team_id, match_dicts
        )
        
        # Preparar resposta
        response = {
            'match_info': {
                'home_team': home_team.popular_name,
                'away_team': away_team.popular_name
            },
            'home_team_metrics': {
                'elo_rating': round(analysis['home_team_analysis']['elo_rating'], 2),
                'form_index': round(analysis['home_team_analysis']['form_index'], 3),
                'goals_per_match': round(analysis['home_team_analysis']['attacking_efficiency']['goals_per_match'], 2),
                'goals_conceded_per_match': round(analysis['home_team_analysis']['defensive_solidity']['goals_conceded_per_match'], 2),
                'home_points_per_match': round(analysis['home_team_analysis']['home_performance']['points_per_match'], 2)
            },
            'away_team_metrics': {
                'elo_rating': round(analysis['away_team_analysis']['elo_rating'], 2),
                'form_index': round(analysis['away_team_analysis']['form_index'], 3),
                'goals_per_match': round(analysis['away_team_analysis']['attacking_efficiency']['goals_per_match'], 2),
                'goals_conceded_per_match': round(analysis['away_team_analysis']['defensive_solidity']['goals_conceded_per_match'], 2),
                'away_points_per_match': round(analysis['away_team_analysis']['away_performance']['points_per_match'], 2)
            },
            'head_to_head': analysis['head_to_head'],
            'match_probabilities': {
                'home_win': round(analysis['match_probabilities']['home_win'] * 100, 2),
                'draw': round(analysis['match_probabilities']['draw'] * 100, 2),
                'away_win': round(analysis['match_probabilities']['away_win'] * 100, 2)
            },
            'value_bets': analysis['value_bets'],
            'recommendation': analysis['recommendation']
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/team-deep-analysis/<int:team_api_id>', methods=['GET'])
def team_deep_analysis(team_api_id):
    """Análise profunda de uma equipa"""
    try:
        team = Team.query.filter_by(api_id=team_api_id).first()
        if not team:
            return jsonify({'error': 'Equipa não encontrada'}), 404
        
        # Buscar jogos da equipa
        team_matches = Match.query.filter(
            (Match.home_team_id == team_api_id) | (Match.away_team_id == team_api_id)
        ).order_by(Match.match_date.desc()).all()
        
        # Preparar dados para análise
        match_data = []
        for match in team_matches:
            is_home = match.home_team_id == team_api_id
            match_data.append({
                'is_home': is_home,
                'goals_for': match.home_score if is_home else match.away_score,
                'goals_against': match.away_score if is_home else match.home_score,
                'status': match.status,
                'match_date': match.match_date,
                'opponent_id': match.away_team_id if is_home else match.home_team_id
            })
        
        # Calcular métricas avançadas
        stats_calc = AdvancedStatsCalculator()
        
        elo_rating = stats_calc.calculate_elo_rating(match_data[-20:])  # Últimos 20 jogos
        form_index = stats_calc.calculate_form_index(match_data[:10])   # Últimos 10 jogos
        attacking_stats = stats_calc.calculate_attacking_efficiency(match_data)
        defensive_stats = stats_calc.calculate_defensive_solidity(match_data)
        home_away_performance = stats_calc.calculate_home_away_performance(match_data)
        
        # Análise de tendências (últimos 5 vs anteriores 5)
        recent_5 = match_data[:5]
        previous_5 = match_data[5:10]
        
        recent_form = stats_calc.calculate_form_index(recent_5)
        previous_form = stats_calc.calculate_form_index(previous_5)
        trend = "Melhorando" if recent_form > previous_form else "Piorando" if recent_form < previous_form else "Estável"
        
        response = {
            'team_info': {
                'name': team.popular_name,
                'abbreviation': team.abbreviation,
                'logo_url': team.logo_url
            },
            'overall_metrics': {
                'elo_rating': round(elo_rating, 2),
                'form_index': round(form_index, 3),
                'matches_analyzed': len([m for m in match_data if m['status'] == 'finalizado']),
                'trend': trend
            },
            'attacking_metrics': {
                'goals_per_match': round(attacking_stats['goals_per_match'], 2),
                'estimated_shots_conversion': round(attacking_stats['shots_conversion'], 3),
                'attacking_third_entries': round(attacking_stats['attacking_third_entries'], 1)
            },
            'defensive_metrics': {
                'goals_conceded_per_match': round(defensive_stats['goals_conceded_per_match'], 2),
                'clean_sheets_ratio': round(defensive_stats['clean_sheets_ratio'], 3),
                'defensive_actions_per_match': round(defensive_stats['defensive_actions'], 1)
            },
            'home_performance': {
                'matches': home_away_performance['home']['wins'] + home_away_performance['home']['draws'] + home_away_performance['home']['losses'],
                'win_rate': round((home_away_performance['home']['wins'] / max(1, home_away_performance['home']['wins'] + home_away_performance['home']['draws'] + home_away_performance['home']['losses'])) * 100, 2),
                'points_per_match': round(home_away_performance['home']['points_per_match'], 2),
                'goals_per_match': round(home_away_performance['home']['goals_for'] / max(1, home_away_performance['home']['wins'] + home_away_performance['home']['draws'] + home_away_performance['home']['losses']), 2)
            },
            'away_performance': {
                'matches': home_away_performance['away']['wins'] + home_away_performance['away']['draws'] + home_away_performance['away']['losses'],
                'win_rate': round((home_away_performance['away']['wins'] / max(1, home_away_performance['away']['wins'] + home_away_performance['away']['draws'] + home_away_performance['away']['losses'])) * 100, 2),
                'points_per_match': round(home_away_performance['away']['points_per_match'], 2),
                'goals_per_match': round(home_away_performance['away']['goals_for'] / max(1, home_away_performance['away']['wins'] + home_away_performance['away']['draws'] + home_away_performance['away']['losses']), 2)
            },
            'recent_matches': [
                {
                    'is_home': match['is_home'],
                    'goals_for': match['goals_for'],
                    'goals_against': match['goals_against'],
                    'result': 'V' if match['goals_for'] > match['goals_against'] else 'E' if match['goals_for'] == match['goals_against'] else 'D',
                    'date': match['match_date'].strftime('%d/%m/%Y') if match['match_date'] else 'N/A'
                }
                for match in recent_5 if match['status'] == 'finalizado'
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/odds-calculator', methods=['POST'])
def odds_calculator():
    """Calculadora de odds baseada em probabilidades"""
    try:
        data = request.get_json()
        home_prob = data.get('home_probability', 0)
        draw_prob = data.get('draw_probability', 0)
        away_prob = data.get('away_probability', 0)
        target_odds = data.get('target_odds', 1.25)
        
        # Validar probabilidades
        total_prob = home_prob + draw_prob + away_prob
        if abs(total_prob - 100) > 1:  # Permitir pequena margem de erro
            return jsonify({'error': 'Probabilidades devem somar 100%'}), 400
        
        # Converter para decimais
        home_prob_decimal = home_prob / 100
        draw_prob_decimal = draw_prob / 100
        away_prob_decimal = away_prob / 100
        
        # Calcular odds justas (sem margem da casa)
        fair_odds = {
            'home': 1 / home_prob_decimal if home_prob_decimal > 0 else 0,
            'draw': 1 / draw_prob_decimal if draw_prob_decimal > 0 else 0,
            'away': 1 / away_prob_decimal if away_prob_decimal > 0 else 0
        }
        
        # Calcular valor esperado para odds alvo
        implied_prob_target = 1 / target_odds
        
        value_analysis = {}
        for outcome, prob in [('home', home_prob_decimal), ('draw', draw_prob_decimal), ('away', away_prob_decimal)]:
            if prob > implied_prob_target:
                expected_value = (prob * (target_odds - 1)) - (1 - prob)
                kelly_fraction = (prob * target_odds - 1) / (target_odds - 1)  # Critério de Kelly
                
                value_analysis[outcome] = {
                    'probability': prob * 100,
                    'fair_odds': round(fair_odds[outcome], 2),
                    'target_odds': target_odds,
                    'expected_value': round(expected_value * 100, 2),
                    'kelly_fraction': round(kelly_fraction * 100, 2),
                    'has_value': expected_value > 0,
                    'confidence_level': 'Alta' if expected_value > 0.1 else 'Média' if expected_value > 0.05 else 'Baixa'
                }
        
        # Recomendação geral
        best_bet = None
        if value_analysis:
            best_outcome = max(value_analysis.keys(), key=lambda x: value_analysis[x]['expected_value'])
            if value_analysis[best_outcome]['expected_value'] > 5:  # Pelo menos 5% de valor esperado
                best_bet = {
                    'outcome': best_outcome,
                    'reason': f"Maior valor esperado: {value_analysis[best_outcome]['expected_value']}%",
                    'recommended_stake': min(10, value_analysis[best_outcome]['kelly_fraction'])  # Máximo 10% do bankroll
                }
        
        response = {
            'input_probabilities': {
                'home': home_prob,
                'draw': draw_prob,
                'away': away_prob
            },
            'fair_odds': fair_odds,
            'value_analysis': value_analysis,
            'best_bet': best_bet,
            'risk_assessment': {
                'low_risk': len([v for v in value_analysis.values() if v['expected_value'] > 10]),
                'medium_risk': len([v for v in value_analysis.values() if 5 <= v['expected_value'] <= 10]),
                'high_risk': len([v for v in value_analysis.values() if 0 < v['expected_value'] < 5])
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/league-analysis/<int:championship_id>', methods=['GET'])
def league_analysis(championship_id):
    """Análise completa de um campeonato"""
    try:
        # Buscar partidas do campeonato
        league_matches = Match.query.filter_by(championship_id=championship_id).all()
        
        if not league_matches:
            return jsonify({'error': 'Campeonato não encontrado ou sem dados'}), 404
        
        # Estatísticas gerais do campeonato
        total_matches = len([m for m in league_matches if m.status == 'finalizado'])
        total_goals = sum(m.home_score + m.away_score for m in league_matches if m.status == 'finalizado')
        
        # Análise de equipas do campeonato
        teams_in_league = set()
        for match in league_matches:
            teams_in_league.add(match.home_team_id)
            teams_in_league.add(match.away_team_id)
        
        team_performances = []
        for team_id in teams_in_league:
            team = Team.query.filter_by(api_id=team_id).first()
            if team:
                team_matches = [m for m in league_matches if m.home_team_id == team_id or m.away_team_id == team_id]
                
                # Calcular estatísticas básicas
                wins = sum(1 for m in team_matches if m.status == 'finalizado' and 
                          ((m.home_team_id == team_id and m.home_score > m.away_score) or
                           (m.away_team_id == team_id and m.away_score > m.home_score)))
                
                draws = sum(1 for m in team_matches if m.status == 'finalizado' and m.home_score == m.away_score)
                
                losses = sum(1 for m in team_matches if m.status == 'finalizado' and 
                            ((m.home_team_id == team_id and m.home_score < m.away_score) or
                             (m.away_team_id == team_id and m.away_score < m.home_score)))
                
                points = wins * 3 + draws
                matches_played = wins + draws + losses
                
                if matches_played > 0:
                    team_performances.append({
                        'team_name': team.popular_name,
                        'matches_played': matches_played,
                        'wins': wins,
                        'draws': draws,
                        'losses': losses,
                        'points': points,
                        'points_per_match': round(points / matches_played, 2),
                        'win_percentage': round((wins / matches_played) * 100, 2)
                    })
        
        # Ordenar por pontos
        team_performances.sort(key=lambda x: x['points'], reverse=True)
        
        response = {
            'championship_info': {
                'championship_id': championship_id,
                'total_matches': total_matches,
                'total_goals': total_goals,
                'goals_per_match': round(total_goals / max(1, total_matches), 2),
                'teams_count': len(teams_in_league)
            },
            'league_table': team_performances[:10],  # Top 10
            'league_stats': {
                'highest_scoring_team': max(team_performances, key=lambda x: x['points'])['team_name'] if team_performances else 'N/A',
                'most_consistent_team': max(team_performances, key=lambda x: x['points_per_match'])['team_name'] if team_performances else 'N/A',
                'average_points_per_match': round(sum(t['points_per_match'] for t in team_performances) / max(1, len(team_performances)), 2)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

