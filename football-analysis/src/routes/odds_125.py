from flask import Blueprint, request, jsonify
from src.models.football import db, Team, Match, TeamStats, Prediction
from src.services.odds_125_system import OddsTargetSystem, BettingStrategy, PerformanceTracker
from datetime import datetime, timedelta
import os

odds_bp = Blueprint('odds', __name__)

# Instâncias dos sistemas
odds_system = OddsTargetSystem()
betting_strategy = BettingStrategy()
performance_tracker = PerformanceTracker()

@odds_bp.route('/find-125-opportunities', methods=['POST'])
def find_125_opportunities():
    """Encontra oportunidades de apostas com odds 1.25"""
    try:
        data = request.get_json()
        championship_id = data.get('championship_id')
        days_ahead = data.get('days_ahead', 7)  # Próximos 7 dias por padrão
        
        # Buscar partidas futuras
        future_date = datetime.now() + timedelta(days=days_ahead)
        
        if championship_id:
            matches = Match.query.filter(
                Match.championship_id == championship_id,
                Match.match_date <= future_date,
                Match.status != 'finalizado'
            ).all()
        else:
            matches = Match.query.filter(
                Match.match_date <= future_date,
                Match.status != 'finalizado'
            ).limit(50).all()  # Limitar a 50 jogos
        
        if not matches:
            return jsonify({'message': 'Nenhuma partida encontrada para análise'}), 404
        
        # Preparar dados das partidas
        matches_data = []
        team_ids = set()
        
        for match in matches:
            matches_data.append({
                'home_team_id': match.home_team_id,
                'away_team_id': match.away_team_id,
                'match_date': match.match_date,
                'championship_name': match.championship_name
            })
            team_ids.add(match.home_team_id)
            team_ids.add(match.away_team_id)
        
        # Buscar dados das equipas
        teams_data = {}
        for team_id in team_ids:
            team = Team.query.filter_by(api_id=team_id).first()
            if team:
                stats = TeamStats.query.filter_by(team_id=team.id).first()
                if stats:
                    teams_data[team_id] = {
                        'name': team.popular_name,
                        'elo_rating': 1500,  # Valor padrão, seria calculado
                        'goals_per_match': stats.goals_per_match,
                        'goals_conceded_per_match': stats.goals_conceded_per_match,
                        'win_percentage': stats.win_percentage,
                        'form_index': 0.6  # Seria calculado dinamicamente
                    }
        
        # Encontrar oportunidades de alta confiança
        opportunities = odds_system.find_high_confidence_bets(matches_data, teams_data)
        
        # Preparar resposta
        formatted_opportunities = []
        for opp in opportunities[:10]:  # Top 10
            home_team = Team.query.filter_by(api_id=opp['home_team_id']).first()
            away_team = Team.query.filter_by(api_id=opp['away_team_id']).first()
            
            formatted_opportunities.append({
                'match': f"{home_team.popular_name if home_team else 'N/A'} vs {away_team.popular_name if away_team else 'N/A'}",
                'home_team': home_team.popular_name if home_team else 'N/A',
                'away_team': away_team.popular_name if away_team else 'N/A',
                'recommended_bet': opp['recommended_bet'],
                'confidence': round(opp['confidence'] * 100, 1),
                'probability': round(opp['probability'] * 100, 1),
                'expected_value': round(opp['expected_value'] * 100, 2),
                'risk_level': opp['risk_level'],
                'supporting_factors': opp['supporting_factors'],
                'match_date': opp['match_date'].strftime('%Y-%m-%d %H:%M') if opp['match_date'] else 'N/A'
            })
        
        return jsonify({
            'total_opportunities': len(opportunities),
            'high_confidence_bets': formatted_opportunities,
            'analysis_summary': {
                'matches_analyzed': len(matches_data),
                'teams_analyzed': len(teams_data),
                'avg_confidence': round(sum(o['confidence'] for o in opportunities) / max(1, len(opportunities)) * 100, 1),
                'low_risk_count': len([o for o in opportunities if o['risk_level'] == 'Baixo']),
                'medium_risk_count': len([o for o in opportunities if o['risk_level'] == 'Médio'])
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@odds_bp.route('/daily-recommendations', methods=['GET'])
def daily_recommendations():
    """Gera recomendações diárias de apostas"""
    try:
        bankroll = request.args.get('bankroll', 1000, type=float)
        
        # Buscar partidas de hoje e amanhã
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        matches = Match.query.filter(
            Match.match_date >= datetime.combine(today, datetime.min.time()),
            Match.match_date <= datetime.combine(tomorrow, datetime.max.time()),
            Match.status != 'finalizado'
        ).all()
        
        if not matches:
            return jsonify({
                'message': 'Nenhuma partida encontrada para hoje/amanhã',
                'recommendations': [],
                'portfolio_summary': {
                    'total_stake': 0,
                    'expected_profit': 0,
                    'roi_expectation': 0,
                    'risk_assessment': 'Sem apostas'
                }
            })
        
        # Preparar dados (similar ao endpoint anterior)
        matches_data = []
        team_ids = set()
        
        for match in matches:
            matches_data.append({
                'home_team_id': match.home_team_id,
                'away_team_id': match.away_team_id,
                'match_date': match.match_date,
                'championship_name': match.championship_name
            })
            team_ids.add(match.home_team_id)
            team_ids.add(match.away_team_id)
        
        # Buscar dados das equipas
        teams_data = {}
        for team_id in team_ids:
            team = Team.query.filter_by(api_id=team_id).first()
            if team:
                stats = TeamStats.query.filter_by(team_id=team.id).first()
                if stats:
                    teams_data[team_id] = {
                        'name': team.popular_name,
                        'elo_rating': 1500 + (stats.win_percentage - 50) * 10,
                        'goals_per_match': stats.goals_per_match,
                        'goals_conceded_per_match': stats.goals_conceded_per_match,
                        'win_percentage': stats.win_percentage,
                        'form_index': min(1.0, stats.win_percentage / 100)
                    }
        
        # Encontrar oportunidades
        opportunities = odds_system.find_high_confidence_bets(matches_data, teams_data)
        
        # Gerar recomendações
        recommendations = betting_strategy.generate_daily_recommendations(opportunities, bankroll)
        
        return jsonify(recommendations)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@odds_bp.route('/bet-calculator', methods=['POST'])
def bet_calculator():
    """Calculadora de apostas para odds 1.25"""
    try:
        data = request.get_json()
        stake = data.get('stake', 100)
        confidence = data.get('confidence', 80)  # Percentagem
        bet_type = data.get('bet_type', 'single')
        
        # Cálculos básicos
        odds = 1.25
        potential_profit = stake * (odds - 1)
        potential_return = stake * odds
        
        # Valor esperado baseado na confiança
        confidence_decimal = confidence / 100
        expected_value = (confidence_decimal * potential_profit) - ((1 - confidence_decimal) * stake)
        
        # Critério de Kelly
        kelly_fraction = ((confidence_decimal * odds) - 1) / (odds - 1)
        kelly_percentage = max(0, min(25, kelly_fraction * 100))  # Limitar a 25%
        
        # Análise de risco
        risk_level = "Baixo" if confidence >= 85 else "Médio" if confidence >= 80 else "Alto"
        
        # Simulação de cenários
        scenarios = []
        for prob in [confidence - 5, confidence, confidence + 5]:
            prob_decimal = max(0.01, min(0.99, prob / 100))
            scenario_ev = (prob_decimal * potential_profit) - ((1 - prob_decimal) * stake)
            scenarios.append({
                'probability': prob,
                'expected_value': round(scenario_ev, 2),
                'roi': round((scenario_ev / stake) * 100, 2)
            })
        
        return jsonify({
            'bet_details': {
                'stake': stake,
                'odds': odds,
                'confidence': confidence,
                'bet_type': bet_type
            },
            'calculations': {
                'potential_profit': round(potential_profit, 2),
                'potential_return': round(potential_return, 2),
                'expected_value': round(expected_value, 2),
                'roi': round((expected_value / stake) * 100, 2),
                'break_even_probability': round((1 / odds) * 100, 2)
            },
            'kelly_criterion': {
                'recommended_fraction': round(kelly_fraction, 4),
                'recommended_percentage': round(kelly_percentage, 2),
                'interpretation': 'Conservador' if kelly_percentage <= 5 else 'Moderado' if kelly_percentage <= 15 else 'Agressivo'
            },
            'risk_analysis': {
                'risk_level': risk_level,
                'confidence_margin': abs(confidence - 80),
                'scenarios': scenarios
            },
            'recommendations': {
                'should_bet': expected_value > 0 and confidence >= 80,
                'max_recommended_stake': round(stake * kelly_percentage / 100, 2) if kelly_percentage > 0 else 0,
                'reasoning': f"Valor esperado {'positivo' if expected_value > 0 else 'negativo'}, confiança {'adequada' if confidence >= 80 else 'baixa'}"
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@odds_bp.route('/performance-tracking', methods=['GET'])
def performance_tracking():
    """Rastreamento de performance das previsões"""
    try:
        # Buscar previsões dos últimos 30 dias
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_predictions = Prediction.query.filter(
            Prediction.created_at >= thirty_days_ago
        ).all()
        
        if not recent_predictions:
            return jsonify({
                'message': 'Nenhuma previsão encontrada nos últimos 30 dias',
                'metrics': {
                    'total_predictions': 0,
                    'win_rate': 0,
                    'roi': 0
                }
            })
        
        # Simular resultados para demonstração
        # Em implementação real, teria resultados reais das apostas
        total_predictions = len(recent_predictions)
        simulated_wins = int(total_predictions * 0.78)  # 78% de acerto simulado
        
        # Calcular métricas
        win_rate = (simulated_wins / total_predictions) * 100
        total_stake = total_predictions * 100  # 100 por aposta
        total_return = simulated_wins * 125  # 25% de lucro por vitória
        roi = ((total_return - total_stake) / total_stake) * 100
        
        # Análise por tipo de aposta
        bet_types = {}
        for pred in recent_predictions:
            bet_type = pred.predicted_result
            if bet_type not in bet_types:
                bet_types[bet_type] = {'count': 0, 'avg_confidence': 0}
            bet_types[bet_type]['count'] += 1
            bet_types[bet_type]['avg_confidence'] += pred.confidence
        
        # Calcular médias
        for bet_type in bet_types:
            bet_types[bet_type]['avg_confidence'] /= bet_types[bet_type]['count']
            bet_types[bet_type]['avg_confidence'] = round(bet_types[bet_type]['avg_confidence'], 2)
        
        return jsonify({
            'period': '30 dias',
            'overall_metrics': {
                'total_predictions': total_predictions,
                'wins': simulated_wins,
                'losses': total_predictions - simulated_wins,
                'win_rate': round(win_rate, 2),
                'roi': round(roi, 2),
                'profit_loss': round(total_return - total_stake, 2),
                'average_confidence': round(sum(p.confidence for p in recent_predictions) / total_predictions, 2)
            },
            'bet_type_analysis': bet_types,
            'monthly_trend': {
                'improving': roi > 0,
                'trend_direction': 'Positiva' if roi > 0 else 'Negativa',
                'consistency': 'Alta' if win_rate >= 75 else 'Média' if win_rate >= 65 else 'Baixa'
            },
            'recommendations': {
                'continue_strategy': win_rate >= 75 and roi > 0,
                'adjust_stake': roi < 0,
                'focus_on_best_bet_type': max(bet_types.keys(), key=lambda x: bet_types[x]['count']) if bet_types else 'N/A'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@odds_bp.route('/market-analysis', methods=['GET'])
def market_analysis():
    """Análise do mercado para identificar tendências"""
    try:
        # Buscar dados dos últimos jogos finalizados
        recent_matches = Match.query.filter(
            Match.status == 'finalizado',
            Match.match_date >= datetime.now() - timedelta(days=30)
        ).limit(200).all()
        
        if not recent_matches:
            return jsonify({'error': 'Dados insuficientes para análise'}), 404
        
        # Análises estatísticas
        total_matches = len(recent_matches)
        home_wins = sum(1 for m in recent_matches if m.home_score > m.away_score)
        draws = sum(1 for m in recent_matches if m.home_score == m.away_score)
        away_wins = sum(1 for m in recent_matches if m.home_score < m.away_score)
        
        total_goals = sum(m.home_score + m.away_score for m in recent_matches)
        avg_goals = total_goals / total_matches
        
        over_25_count = sum(1 for m in recent_matches if (m.home_score + m.away_score) > 2.5)
        over_25_percentage = (over_25_count / total_matches) * 100
        
        both_scored = sum(1 for m in recent_matches if m.home_score > 0 and m.away_score > 0)
        btts_percentage = (both_scored / total_matches) * 100
        
        # Identificar padrões para odds 1.25
        patterns = []
        
        # Padrão 1: Vantagem de casa
        home_advantage = (home_wins / total_matches) * 100
        if home_advantage >= 45:
            patterns.append({
                'pattern': 'Forte vantagem de casa',
                'percentage': round(home_advantage, 1),
                'opportunity': 'Apostas em vitória da casa ou dupla hipótese (1X)',
                'confidence': 'Alta' if home_advantage >= 50 else 'Média'
            })
        
        # Padrão 2: Jogos com muitos golos
        if over_25_percentage >= 60:
            patterns.append({
                'pattern': 'Tendência de jogos com muitos golos',
                'percentage': round(over_25_percentage, 1),
                'opportunity': 'Apostas em Over 2.5 golos',
                'confidence': 'Alta' if over_25_percentage >= 70 else 'Média'
            })
        
        # Padrão 3: Ambas equipas marcam
        if btts_percentage >= 55:
            patterns.append({
                'pattern': 'Ambas equipas tendem a marcar',
                'percentage': round(btts_percentage, 1),
                'opportunity': 'Apostas em ambas equipas marcam',
                'confidence': 'Alta' if btts_percentage >= 65 else 'Média'
            })
        
        # Padrão 4: Poucos empates
        draw_percentage = (draws / total_matches) * 100
        if draw_percentage <= 20:
            patterns.append({
                'pattern': 'Poucos empates',
                'percentage': round(draw_percentage, 1),
                'opportunity': 'Evitar apostas em empate, focar em resultado definido',
                'confidence': 'Média'
            })
        
        return jsonify({
            'analysis_period': '30 dias',
            'sample_size': total_matches,
            'market_statistics': {
                'home_wins': home_wins,
                'draws': draws,
                'away_wins': away_wins,
                'home_win_percentage': round(home_advantage, 1),
                'draw_percentage': round(draw_percentage, 1),
                'away_win_percentage': round((away_wins / total_matches) * 100, 1),
                'average_goals_per_match': round(avg_goals, 2),
                'over_25_percentage': round(over_25_percentage, 1),
                'btts_percentage': round(btts_percentage, 1)
            },
            'identified_patterns': patterns,
            'market_opportunities': {
                'best_markets_for_125_odds': [
                    pattern['opportunity'] for pattern in patterns 
                    if pattern['confidence'] == 'Alta'
                ],
                'market_efficiency': 'Baixa' if len(patterns) >= 3 else 'Média' if len(patterns) >= 2 else 'Alta',
                'recommendation': 'Mercado favorável para odds 1.25' if len(patterns) >= 2 else 'Mercado neutro'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

