# Guia Rápido de Instalação - Sistema de Análise de Futebol

## Instalação em 5 Minutos

### Pré-requisitos
- Python 3.11 ou superior
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Passos de Instalação

#### 1. Preparar o Ambiente
```bash
# Navegar para o diretório do sistema
cd /home/ubuntu/football-analysis

# Ativar ambiente virtual
source venv/bin/activate
```

#### 2. Verificar Dependências
```bash
# As dependências já estão instaladas, mas pode verificar:
pip list
```

#### 3. Iniciar o Sistema
```bash
# Executar o servidor Flask
python src/main.py
```

#### 4. Aceder à Interface
1. Abrir navegador web
2. Navegar para: `http://localhost:5000`
3. O dashboard será carregado automaticamente

### Primeiro Uso

#### Sincronizar Dados
1. Clicar no botão "Sincronizar Dados" no canto superior direito
2. Aguardar o processamento (pode demorar alguns minutos)
3. Verificar se as estatísticas foram atualizadas no dashboard

#### Encontrar Oportunidades
1. Navegar para a seção "Odds 1.25"
2. Definir o bankroll (valor padrão: €1000)
3. Clicar em "Encontrar Oportunidades"
4. Analisar as recomendações apresentadas

### Estrutura de Ficheiros

```
football-analysis/
├── src/
│   ├── main.py              # Servidor principal
│   ├── models/              # Modelos de dados
│   ├── routes/              # Endpoints da API
│   ├── services/            # Lógica de negócio
│   └── static/              # Interface web
├── venv/                    # Ambiente virtual Python
├── requirements.txt         # Dependências
└── DOCUMENTACAO_COMPLETA.md # Documentação detalhada
```

### Resolução Rápida de Problemas

**Erro "Port already in use":**
```bash
# Encontrar processo na porta 5000
lsof -i :5000
# Terminar processo se necessário
kill -9 [PID]
```

**Erro de módulos Python:**
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

**Interface não carrega:**
- Verificar se o servidor Flask está em execução
- Confirmar URL: http://localhost:5000 (não https)
- Verificar mensagens de erro no terminal

### Comandos Úteis

```bash
# Parar o servidor
Ctrl+C

# Verificar logs
tail -f logs/app.log

# Backup da base de dados
cp src/database/app.db backup/

# Atualizar dependências
pip freeze > requirements.txt
```

### Configuração da API (Opcional)

Para dados reais, editar `src/services/football_api.py`:
```python
# Substituir pela sua chave de API
API_KEY = "sua_chave_api_aqui"
```

### Suporte

- **Documentação Completa**: `DOCUMENTACAO_COMPLETA.md`
- **Logs do Sistema**: Verificar terminal onde o Flask está em execução
- **Base de Dados**: SQLite em `src/database/app.db`

---

**Tempo de Instalação**: ~5 minutos  
**Tempo de Primeira Sincronização**: ~10-15 minutos  
**Sistema Pronto para Uso**: Imediatamente após sincronização

