from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    popular_name = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    logo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    matches_home = db.relationship('Match', foreign_keys='Match.home_team_id', backref='home_team')
    matches_away = db.relationship('Match', foreign_keys='Match.away_team_id', backref='away_team')
    players = db.relationship('Player', backref='team')

class Player(db.Model):
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    popular_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=True, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    home_score = db.Column(db.Integer, default=0)
    away_score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    championship_id = db.Column(db.Integer, nullable=False)
    championship_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TeamStats(db.Model):
    __tablename__ = 'team_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    matches_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    goals_for = db.Column(db.Integer, default=0)
    goals_against = db.Column(db.Integer, default=0)
    goals_per_match = db.Column(db.Float, default=0.0)
    goals_conceded_per_match = db.Column(db.Float, default=0.0)
    win_percentage = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    team = db.relationship('Team', backref='stats')

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    predicted_result = db.Column(db.String(20), nullable=False)  # 'home', 'away', 'draw'
    confidence = db.Column(db.Float, nullable=False)
    odds = db.Column(db.Float, nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    home_team = db.relationship('Team', foreign_keys=[home_team_id])
    away_team = db.relationship('Team', foreign_keys=[away_team_id])

