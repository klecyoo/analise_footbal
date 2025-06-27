#!/bin/bash

# Script de Deployment para Vercel - Sistema de Análise de Futebol
# Execute este script após fazer login na Vercel

echo "🚀 Iniciando deployment do Sistema de Análise de Futebol na Vercel..."

# Verificar se está no diretório correto
if [ ! -f "vercel.json" ]; then
    echo "❌ Erro: vercel.json não encontrado. Execute este script no diretório do projeto."
    exit 1
fi

# Verificar se o Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "📦 Instalando Vercel CLI..."
    npm install -g vercel
fi

# Verificar se está logado na Vercel
echo "🔐 Verificando login na Vercel..."
if ! vercel whoami &> /dev/null; then
    echo "❌ Não está logado na Vercel. Execute 'vercel login' primeiro."
    exit 1
fi

echo "✅ Login verificado com sucesso!"

# Fazer o deployment
echo "🚀 Fazendo deployment..."
vercel --prod --yes --name football-analysis-odds

# Verificar se o deployment foi bem-sucedido
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment concluído com sucesso!"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Acesse o dashboard da Vercel para ver o URL do seu site"
    echo "2. Configure um domínio personalizado se desejar"
    echo "3. Monitore os logs e performance"
    echo ""
    echo "🔗 URLs importantes:"
    echo "- Dashboard: https://vercel.com/dashboard"
    echo "- Documentação: https://vercel.com/docs"
    echo ""
else
    echo "❌ Erro durante o deployment. Verifique os logs acima."
    exit 1
fi

