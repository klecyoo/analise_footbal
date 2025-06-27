# Guia de Deployment na Vercel - Sistema de Análise de Futebol

## Pré-requisitos

1. **Conta na Vercel**: Criar conta em [vercel.com](https://vercel.com)
2. **Vercel CLI**: Instalar globalmente
   ```bash
   npm install -g vercel
   ```
3. **Git**: Repositório Git configurado (opcional, mas recomendado)

## Opção 1: Deploy via Vercel CLI (Recomendado)

### Passo 1: Preparar o Projeto
```bash
# Navegar para o diretório do projeto
cd /home/ubuntu/football-analysis

# Verificar se todos os arquivos estão presentes
ls -la
```

### Passo 2: Login na Vercel
```bash
# Fazer login na Vercel
vercel login
```

### Passo 3: Deploy
```bash
# Fazer o primeiro deploy
vercel

# Seguir as instruções:
# - Set up and deploy? [Y/n] Y
# - Which scope? (selecionar sua conta)
# - Link to existing project? [y/N] N
# - What's your project's name? football-analysis-odds
# - In which directory is your code located? ./
```

### Passo 4: Deploy de Produção
```bash
# Para deploy de produção
vercel --prod
```

## Opção 2: Deploy via GitHub (Automático)

### Passo 1: Criar Repositório no GitHub
1. Criar novo repositório no GitHub
2. Fazer push do código:
   ```bash
   git init
   git add .
   git commit -m "Sistema de Análise de Futebol - Odds 1.25"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/football-analysis.git
   git push -u origin main
   ```

### Passo 2: Conectar à Vercel
1. Ir para [vercel.com/dashboard](https://vercel.com/dashboard)
2. Clicar em "New Project"
3. Importar repositório do GitHub
4. Configurar:
   - **Framework Preset**: Other
   - **Build Command**: (deixar vazio)
   - **Output Directory**: (deixar vazio)
   - **Install Command**: `pip install -r requirements.txt`

## Configurações Importantes

### Variáveis de Ambiente na Vercel
No dashboard da Vercel, adicionar:
- `VERCEL=1`
- `FLASK_ENV=production`

### Estrutura de Arquivos Necessária
```
football-analysis/
├── vercel.json          # Configuração da Vercel
├── requirements.txt     # Dependências Python
├── runtime.txt         # Versão do Python
├── .env               # Variáveis de ambiente
├── src/
│   ├── main.py        # Aplicação Flask principal
│   ├── models/        # Modelos de dados
│   ├── routes/        # Rotas da API
│   ├── services/      # Lógica de negócio
│   └── static/        # Interface web
└── README.md
```

## Verificação do Deploy

### URLs de Teste
Após o deploy, testar:
- `https://SEU_PROJETO.vercel.app/` - Interface principal
- `https://SEU_PROJETO.vercel.app/health` - Health check
- `https://SEU_PROJETO.vercel.app/api/football/teams` - API de equipas

### Logs e Debug
```bash
# Ver logs do deployment
vercel logs

# Ver logs em tempo real
vercel logs --follow
```

## Limitações da Vercel para Flask

### Limitações Conhecidas
1. **Timeout**: Máximo 30 segundos por request
2. **Base de Dados**: SQLite em memória (dados não persistem)
3. **Armazenamento**: Apenas arquivos estáticos
4. **Recursos**: CPU e memória limitados

### Soluções Alternativas
Para produção real, considerar:
- **Base de Dados**: PostgreSQL (Supabase, Neon)
- **Cache**: Redis (Upstash)
- **Armazenamento**: AWS S3, Cloudinary

## Configuração de Domínio Personalizado

### Adicionar Domínio
1. No dashboard Vercel, ir para Settings > Domains
2. Adicionar domínio personalizado
3. Configurar DNS conforme instruções

### SSL/HTTPS
- Automático pela Vercel
- Certificados Let's Encrypt

## Monitorização

### Analytics
- Ativar Vercel Analytics no dashboard
- Monitorizar performance e uso

### Logs
- Logs disponíveis no dashboard
- Integração com ferramentas de monitorização

## Troubleshooting

### Problemas Comuns

**Erro de Import:**
```python
# Verificar imports relativos em src/main.py
sys.path.insert(0, os.path.dirname(__file__))
```

**Timeout:**
```python
# Otimizar queries e reduzir processamento
# Usar cache quando possível
```

**Base de Dados:**
```python
# Para produção, usar base de dados externa
# Configurar connection string nas variáveis de ambiente
```

### Comandos Úteis
```bash
# Ver status do projeto
vercel ls

# Ver informações do deployment
vercel inspect

# Remover projeto
vercel remove
```

## Exemplo de URL Final

Após deployment bem-sucedido:
- **URL Principal**: `https://football-analysis-odds.vercel.app`
- **API**: `https://football-analysis-odds.vercel.app/api/`
- **Health Check**: `https://football-analysis-odds.vercel.app/health`

## Custos

### Plano Gratuito Vercel
- 100GB bandwidth/mês
- 100 deployments/dia
- Domínios .vercel.app incluídos
- SSL automático

### Upgrade para Pro
- Bandwidth ilimitado
- Domínios personalizados
- Analytics avançados
- Suporte prioritário

---

**Nota**: Este sistema está otimizado para demonstração na Vercel. Para uso em produção com dados reais, recomenda-se configurar uma base de dados externa e otimizações adicionais.

