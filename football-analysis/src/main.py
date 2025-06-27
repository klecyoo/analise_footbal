import os
import sys
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

# Adicionar o diretório src ao path para imports
sys.path.insert(0, os.path.dirname(__file__))

from models.user import db
from models.football import Team, Player, Match, TeamStats, Prediction
from routes.user import user_bp
from routes.football import football_bp
from routes.advanced import advanced_bp
from routes.odds_125 import odds_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para todas as rotas
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(football_bp, url_prefix='/api/football')
app.register_blueprint(advanced_bp, url_prefix='/api/advanced')
app.register_blueprint(odds_bp, url_prefix='/api/odds')

# Configuração da base de dados para Vercel (usar SQLite em memória para demo)
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar base de dados
db.init_app(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Sistema de Análise de Futebol Online'})

# Criar tabelas se não existirem
with app.app_context():
    try:
        db.create_all()
        
        # Dados de demonstração para Vercel
        if os.environ.get('VERCEL') and Team.query.count() == 0:
            # Adicionar algumas equipas de demonstração
            demo_teams = [
                Team(api_id=1, name='Flamengo', popular_name='Flamengo', abbreviation='FLA'),
                Team(api_id=2, name='Palmeiras', popular_name='Palmeiras', abbreviation='PAL'),
                Team(api_id=3, name='São Paulo', popular_name='São Paulo', abbreviation='SAO'),
                Team(api_id=4, name='Corinthians', popular_name='Corinthians', abbreviation='COR'),
            ]
            
            for team in demo_teams:
                db.session.add(team)
            
            # Adicionar estatísticas de demonstração
            demo_stats = [
                TeamStats(team_id=1, matches_played=20, wins=12, draws=5, losses=3, 
                         goals_for=35, goals_against=18, win_percentage=60.0, 
                         goals_per_match=1.75, goals_conceded_per_match=0.9),
                TeamStats(team_id=2, matches_played=20, wins=14, draws=4, losses=2, 
                         goals_for=38, goals_against=15, win_percentage=70.0, 
                         goals_per_match=1.9, goals_conceded_per_match=0.75),
                TeamStats(team_id=3, matches_played=20, wins=10, draws=6, losses=4, 
                         goals_for=28, goals_against=22, win_percentage=50.0, 
                         goals_per_match=1.4, goals_conceded_per_match=1.1),
                TeamStats(team_id=4, matches_played=20, wins=8, draws=7, losses=5, 
                         goals_for=25, goals_against=24, win_percentage=40.0, 
                         goals_per_match=1.25, goals_conceded_per_match=1.2),
            ]
            
            for stat in demo_stats:
                db.session.add(stat)
            
            db.session.commit()
            
    except Exception as e:
        print(f"Erro ao inicializar base de dados: {e}")

# Para Vercel, exportar a aplicação
if __name__ == '__main__':
    if os.environ.get('VERCEL'):
        # Em produção na Vercel, não executar o servidor
        pass
    else:
        # Desenvolvimento local
        app.run(host='0.0.0.0', port=5000, debug=True)

