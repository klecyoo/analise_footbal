# 🚀 Deployment na Vercel - Guia Passo-a-Passo

## Método Mais Simples: Upload Direto

### Passo 1: Preparar o Arquivo
1. Descarregue o arquivo `football-analysis-system.zip`
2. Extraia o conteúdo para uma pasta no seu computador

### Passo 2: Aceder à Vercel
1. Vá para [vercel.com](https://vercel.com)
2. Crie uma conta gratuita ou faça login
3. Clique em "New Project"

### Passo 3: Upload do Projeto
1. Clique em "Browse" ou arraste a pasta do projeto
2. Selecione a pasta `football-analysis`
3. Configure:
   - **Project Name**: `football-analysis-odds`
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (deixar como está)
   - **Build Command**: (deixar vazio)
   - **Output Directory**: (deixar vazio)
   - **Install Command**: `pip install -r requirements.txt`

### Passo 4: Variáveis de Ambiente
1. Ir para "Environment Variables"
2. Adicionar:
   - `VERCEL` = `1`
   - `FLASK_ENV` = `production`

### Passo 5: Deploy
1. Clicar em "Deploy"
2. Aguardar o processo (2-5 minutos)
3. Receber o URL do site

---

## Método Alternativo: Via CLI

### Pré-requisitos
- Node.js instalado no seu computador
- Terminal/Command Prompt

### Passos
1. **Instalar Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Fazer Login**:
   ```bash
   vercel login
   ```

3. **Navegar para o Projeto**:
   ```bash
   cd caminho/para/football-analysis
   ```

4. **Deploy**:
   ```bash
   vercel --prod
   ```

5. **Seguir as Instruções**:
   - Project name: `football-analysis-odds`
   - Link to existing project: `N`
   - Directory: `./`

---

## Método GitHub (Automático)

### Passo 1: Criar Repositório
1. Criar repositório no GitHub
2. Upload dos arquivos do projeto

### Passo 2: Conectar à Vercel
1. Na Vercel, clicar "Import Git Repository"
2. Selecionar o repositório do GitHub
3. Configurar conforme instruções acima

---

## URLs Esperados

Após deployment bem-sucedido:
- **Site Principal**: `https://football-analysis-odds.vercel.app`
- **API Health Check**: `https://football-analysis-odds.vercel.app/health`
- **Dashboard**: Interface completa de análise

---

## Verificação do Funcionamento

### Testes Básicos
1. ✅ Site carrega corretamente
2. ✅ Dashboard mostra interface
3. ✅ Seção "Odds 1.25" funciona
4. ✅ Calculadora de apostas responde
5. ✅ API retorna dados de demonstração

### Resolução de Problemas

**Site não carrega:**
- Verificar logs no dashboard Vercel
- Confirmar se `vercel.json` está presente
- Verificar variáveis de ambiente

**Erro 500:**
- Verificar logs de Python
- Confirmar dependências no `requirements.txt`
- Verificar imports nos arquivos Python

**Interface sem dados:**
- Normal na primeira execução
- Dados de demonstração são carregados automaticamente
- Para dados reais, configurar API key

---

## Configurações Avançadas

### Domínio Personalizado
1. No dashboard Vercel: Settings > Domains
2. Adicionar domínio desejado
3. Configurar DNS conforme instruções

### Monitorização
- Analytics automático da Vercel
- Logs em tempo real no dashboard
- Alertas de performance

### Atualizações
- Redeployment automático via Git
- Ou upload manual de nova versão
- Rollback disponível no dashboard

---

## Suporte

### Documentação Oficial
- [Vercel Docs](https://vercel.com/docs)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

### Troubleshooting
- Logs disponíveis no dashboard
- Community forum da Vercel
- Documentação do projeto incluída

---

**🎯 Objetivo**: Ter o sistema funcionando em `https://SEU-PROJETO.vercel.app` em menos de 10 minutos!

**📞 Suporte**: Todos os arquivos de configuração já estão preparados e otimizados para a Vercel.

