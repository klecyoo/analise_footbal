import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class FootballAPIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.api-futebol.com.br/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_championships(self) -> List[Dict]:
        """Busca lista de campeonatos disponíveis"""
        try:
            response = requests.get(f"{self.base_url}/campeonatos", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar campeonatos: {e}")
            return []
    
    def get_championship_matches(self, championship_id: int) -> Dict:
        """Busca todas as partidas de um campeonato"""
        try:
            response = requests.get(f"{self.base_url}/campeonatos/{championship_id}/partidas", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar partidas do campeonato {championship_id}: {e}")
            return {}
    
    def get_match_details(self, match_id: int) -> Dict:
        """Busca detalhes de uma partida específica"""
        try:
            response = requests.get(f"{self.base_url}/partidas/{match_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar detalhes da partida {match_id}: {e}")
            return {}
    
    def get_team_details(self, team_id: int) -> Dict:
        """Busca detalhes de uma equipa"""
        try:
            response = requests.get(f"{self.base_url}/times/{team_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar detalhes da equipa {team_id}: {e}")
            return {}
    
    def get_championship_table(self, championship_id: int) -> List[Dict]:
        """Busca tabela de classificação de um campeonato"""
        try:
            response = requests.get(f"{self.base_url}/campeonatos/{championship_id}/tabela", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar tabela do campeonato {championship_id}: {e}")
            return []
    
    def get_live_matches(self) -> List[Dict]:
        """Busca partidas ao vivo"""
        try:
            response = requests.get(f"{self.base_url}/ao-vivo", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar partidas ao vivo: {e}")
            return []

class DataProcessor:
    """Classe para processar e normalizar dados da API"""
    
    @staticmethod
    def process_team_data(team_data: Dict) -> Dict:
        """Processa dados de uma equipa"""
        return {
            'api_id': team_data.get('time_id'),
            'name': team_data.get('nome', ''),
            'popular_name': team_data.get('nome_popular', ''),
            'abbreviation': team_data.get('sigla', ''),
            'logo_url': team_data.get('escudo', '')
        }
    
    @staticmethod
    def process_match_data(match_data: Dict) -> Dict:
        """Processa dados de uma partida"""
        return {
            'api_id': match_data.get('partida_id'),
            'home_team_id': match_data.get('time_mandante', {}).get('time_id'),
            'away_team_id': match_data.get('time_visitante', {}).get('time_id'),
            'home_score': match_data.get('placar_mandante', 0),
            'away_score': match_data.get('placar_visitante', 0),
            'status': match_data.get('status', ''),
            'match_date': DataProcessor.parse_date(match_data.get('data_realizacao_iso')),
            'championship_id': match_data.get('campeonato', {}).get('campeonato_id'),
            'championship_name': match_data.get('campeonato', {}).get('nome', '')
        }
    
    @staticmethod
    def process_player_data(player_data: Dict, team_id: int) -> Dict:
        """Processa dados de um jogador"""
        return {
            'api_id': player_data.get('atleta', {}).get('atleta_id'),
            'name': player_data.get('atleta', {}).get('nome_popular', ''),
            'popular_name': player_data.get('atleta', {}).get('nome_popular', ''),
            'position': player_data.get('posicao', {}).get('nome', ''),
            'team_id': team_id
        }
    
    @staticmethod
    def parse_date(date_string: str) -> Optional[datetime]:
        """Converte string de data ISO para datetime"""
        if not date_string:
            return None
        try:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except ValueError:
            return None

class StatsCalculator:
    """Classe para calcular estatísticas das equipas"""
    
    @staticmethod
    def calculate_team_stats(matches: List[Dict], team_id: int) -> Dict:
        """Calcula estatísticas de uma equipa baseado nas suas partidas"""
        stats = {
            'matches_played': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_for': 0,
            'goals_against': 0,
            'goals_per_match': 0.0,
            'goals_conceded_per_match': 0.0,
            'win_percentage': 0.0
        }
        
        for match in matches:
            if match['status'] != 'finalizado':
                continue
                
            is_home = match['home_team_id'] == team_id
            is_away = match['away_team_id'] == team_id
            
            if not (is_home or is_away):
                continue
            
            stats['matches_played'] += 1
            
            if is_home:
                goals_for = match['home_score']
                goals_against = match['away_score']
            else:
                goals_for = match['away_score']
                goals_against = match['home_score']
            
            stats['goals_for'] += goals_for
            stats['goals_against'] += goals_against
            
            if goals_for > goals_against:
                stats['wins'] += 1
            elif goals_for == goals_against:
                stats['draws'] += 1
            else:
                stats['losses'] += 1
        
        # Calcular médias
        if stats['matches_played'] > 0:
            stats['goals_per_match'] = stats['goals_for'] / stats['matches_played']
            stats['goals_conceded_per_match'] = stats['goals_against'] / stats['matches_played']
            stats['win_percentage'] = (stats['wins'] / stats['matches_played']) * 100
        
        return stats

