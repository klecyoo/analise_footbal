from flask import Blueprint, request, jsonify
from src.models.football import db, Team, Player, Match, TeamStats, Prediction
from src.services.football_api import FootballAPIService, DataProcessor, StatsCalculator
from datetime import datetime, timedelta
import os

football_bp = Blueprint('football', __name__)

# Configuração da API (usar chave de teste por padrão)
API_KEY = os.getenv('FOOTBALL_API_KEY', 'test_a8c37778328495ac24c5d0d3c3923b')
api_service = FootballAPIService(API_KEY)

@football_bp.route('/championships', methods=['GET'])
def get_championships():
    """Busca lista de campeonatos"""
    championships = api_service.get_championships()
    return jsonify(championships)

@football_bp.route('/sync-championship/<int:championship_id>', methods=['POST'])
def sync_championship_data(championship_id):
    """Sincroniza dados de um campeonato específico"""
    try:
        # Buscar dados do campeonato
        championship_data = api_service.get_championship_matches(championship_id)
        
        if not championship_data:
            return jsonify({'error': 'Campeonato não encontrado'}), 404
        
        teams_synced = 0
        matches_synced = 0
        
        # Processar partidas
        partidas = championship_data.get('partidas', {})
        
        for fase_name, fase_data in partidas.items():
            if isinstance(fase_data, dict):
                for chave_name, chave_data in fase_data.items():
                    if isinstance(chave_data, dict):
                        for tipo_jogo, jogo_data in chave_data.items():
                            if isinstance(jogo_data, dict) and 'partida_id' in jogo_data:
                                # Processar equipa mandante
                                home_team_data = jogo_data.get('time_mandante', {})
                                if home_team_data:
                                    team_data = DataProcessor.process_team_data(home_team_data)
                                    if team_data['api_id']:
                                        existing_team = Team.query.filter_by(api_id=team_data['api_id']).first()
                                        if not existing_team:
                                            new_team = Team(**team_data)
                                            db.session.add(new_team)
                                            teams_synced += 1
                                
                                # Processar equipa visitante
                                away_team_data = jogo_data.get('time_visitante', {})
                                if away_team_data:
                                    team_data = DataProcessor.process_team_data(away_team_data)
                                    if team_data['api_id']:
                                        existing_team = Team.query.filter_by(api_id=team_data['api_id']).first()
                                        if not existing_team:
                                            new_team = Team(**team_data)
                                            db.session.add(new_team)
                                            teams_synced += 1
                                
                                # Processar partida
                                match_data = DataProcessor.process_match_data(jogo_data)
                                match_data['championship_id'] = championship_id
                                match_data['championship_name'] = championship_data.get('campeonato', {}).get('nome', '')
                                
                                if match_data['api_id']:
                                    existing_match = Match.query.filter_by(api_id=match_data['api_id']).first()
                                    if not existing_match:
                                        new_match = Match(**match_data)
                                        db.session.add(new_match)
                                        matches_synced += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Dados sincronizados com sucesso',
            'teams_synced': teams_synced,
            'matches_synced': matches_synced
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@football_bp.route('/calculate-stats', methods=['POST'])
def calculate_team_stats():
    """Calcula estatísticas para todas as equipas"""
    try:
        teams = Team.query.all()
        stats_updated = 0
        
        for team in teams:
            # Buscar todas as partidas da equipa
            matches = Match.query.filter(
                (Match.home_team_id == team.api_id) | (Match.away_team_id == team.api_id)
            ).all()
            
            # Converter para formato dict
            match_dicts = []
            for match in matches:
                match_dicts.append({
                    'home_team_id': match.home_team_id,
                    'away_team_id': match.away_team_id,
                    'home_score': match.home_score,
                    'away_score': match.away_score,
                    'status': match.status
                })
            
            # Calcular estatísticas
            stats = StatsCalculator.calculate_team_stats(match_dicts, team.api_id)
            
            # Atualizar ou criar registo de estatísticas
            existing_stats = TeamStats.query.filter_by(team_id=team.id).first()
            if existing_stats:
                for key, value in stats.items():
                    setattr(existing_stats, key, value)
                existing_stats.last_updated = datetime.utcnow()
            else:
                stats['team_id'] = team.id
                new_stats = TeamStats(**stats)
                db.session.add(new_stats)
            
            stats_updated += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Estatísticas calculadas com sucesso',
            'teams_updated': stats_updated
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@football_bp.route('/teams', methods=['GET'])
def get_teams():
    """Lista todas as equipas com suas estatísticas"""
    teams = db.session.query(Team, TeamStats).outerjoin(TeamStats).all()
    
    result = []
    for team, stats in teams:
        team_data = {
            'id': team.id,
            'api_id': team.api_id,
            'name': team.name,
            'popular_name': team.popular_name,
            'abbreviation': team.abbreviation,
            'logo_url': team.logo_url,
            'stats': None
        }
        
        if stats:
            team_data['stats'] = {
                'matches_played': stats.matches_played,
                'wins': stats.wins,
                'draws': stats.draws,
                'losses': stats.losses,
                'goals_for': stats.goals_for,
                'goals_against': stats.goals_against,
                'goals_per_match': round(stats.goals_per_match, 2),
                'goals_conceded_per_match': round(stats.goals_conceded_per_match, 2),
                'win_percentage': round(stats.win_percentage, 2),
                'last_updated': stats.last_updated.isoformat() if stats.last_updated else None
            }
        
        result.append(team_data)
    
    return jsonify(result)

@football_bp.route('/matches', methods=['GET'])
def get_matches():
    """Lista todas as partidas"""
    matches = db.session.query(Match, Team.popular_name.label('home_name'), Team.popular_name.label('away_name')).join(
        Team, Team.api_id == Match.home_team_id
    ).join(
        Team.query.filter(Team.api_id == Match.away_team_id).subquery(), 
        Team.api_id == Match.away_team_id
    ).all()
    
    # Simplificar a consulta
    matches = Match.query.all()
    result = []
    
    for match in matches:
        home_team = Team.query.filter_by(api_id=match.home_team_id).first()
        away_team = Team.query.filter_by(api_id=match.away_team_id).first()
        
        result.append({
            'id': match.id,
            'api_id': match.api_id,
            'home_team': home_team.popular_name if home_team else 'Desconhecido',
            'away_team': away_team.popular_name if away_team else 'Desconhecido',
            'home_score': match.home_score,
            'away_score': match.away_score,
            'status': match.status,
            'match_date': match.match_date.isoformat() if match.match_date else None,
            'championship_name': match.championship_name
        })
    
    return jsonify(result)

@football_bp.route('/predict-odds', methods=['POST'])
def predict_odds():
    """Gera previsões com odds 1.25"""
    try:
        data = request.get_json()
        home_team_id = data.get('home_team_id')
        away_team_id = data.get('away_team_id')
        
        if not home_team_id or not away_team_id:
            return jsonify({'error': 'IDs das equipas são obrigatórios'}), 400
        
        # Buscar estatísticas das equipas
        home_team = Team.query.filter_by(api_id=home_team_id).first()
        away_team = Team.query.filter_by(api_id=away_team_id).first()
        
        if not home_team or not away_team:
            return jsonify({'error': 'Equipas não encontradas'}), 404
        
        home_stats = TeamStats.query.filter_by(team_id=home_team.id).first()
        away_stats = TeamStats.query.filter_by(team_id=away_team.id).first()
        
        if not home_stats or not away_stats:
            return jsonify({'error': 'Estatísticas não disponíveis para as equipas'}), 400
        
        # Algoritmo simples de previsão baseado em estatísticas
        home_strength = (home_stats.win_percentage + home_stats.goals_per_match * 10) / 2
        away_strength = (away_stats.win_percentage + away_stats.goals_per_match * 10) / 2
        
        # Vantagem de jogar em casa (5%)
        home_strength += 5
        
        # Determinar resultado mais provável
        if home_strength > away_strength + 10:
            predicted_result = 'home'
            confidence = min(85, 60 + (home_strength - away_strength) / 2)
        elif away_strength > home_strength + 10:
            predicted_result = 'away'
            confidence = min(85, 60 + (away_strength - home_strength) / 2)
        else:
            predicted_result = 'draw'
            confidence = 50
        
        # Calcular odds para atingir 1.25
        # Odds = 1 / probabilidade
        # Para odds 1.25, probabilidade = 1/1.25 = 0.8 = 80%
        target_odds = 1.25
        
        # Salvar previsão
        prediction = Prediction(
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            predicted_result=predicted_result,
            confidence=confidence,
            odds=target_odds,
            match_date=datetime.utcnow() + timedelta(days=1)  # Exemplo: jogo amanhã
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'prediction': {
                'home_team': home_team.popular_name,
                'away_team': away_team.popular_name,
                'predicted_result': predicted_result,
                'confidence': round(confidence, 2),
                'odds': target_odds,
                'home_stats': {
                    'win_percentage': home_stats.win_percentage,
                    'goals_per_match': home_stats.goals_per_match,
                    'matches_played': home_stats.matches_played
                },
                'away_stats': {
                    'win_percentage': away_stats.win_percentage,
                    'goals_per_match': away_stats.goals_per_match,
                    'matches_played': away_stats.matches_played
                }
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@football_bp.route('/predictions', methods=['GET'])
def get_predictions():
    """Lista todas as previsões"""
    predictions = Prediction.query.order_by(Prediction.created_at.desc()).all()
    
    result = []
    for pred in predictions:
        home_team = Team.query.get(pred.home_team_id)
        away_team = Team.query.get(pred.away_team_id)
        
        result.append({
            'id': pred.id,
            'home_team': home_team.popular_name if home_team else 'Desconhecido',
            'away_team': away_team.popular_name if away_team else 'Desconhecido',
            'predicted_result': pred.predicted_result,
            'confidence': pred.confidence,
            'odds': pred.odds,
            'match_date': pred.match_date.isoformat() if pred.match_date else None,
            'created_at': pred.created_at.isoformat()
        })
    
    return jsonify(result)

