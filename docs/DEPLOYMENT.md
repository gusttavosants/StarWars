# Guia de Deployment - Star Wars API

## Visão Geral

Este guia descreve como fazer deploy da Star Wars API em diferentes ambientes.

## Pré-requisitos

- Google Cloud SDK instalado
- Conta GCP com projeto criado
- Permissões de Cloud Functions, API Gateway e Secret Manager
- Git configurado

## Deployment em GCP Cloud Functions

### 1. Preparar Projeto GCP

```bash
# Instalar Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Autenticar
gcloud auth login

# Definir projeto
gcloud config set project YOUR_PROJECT_ID

# Habilitar APIs necessárias
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com
gcloud services enable memorystore.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable logging.googleapis.com
```

### 2. Configurar Secret Manager

```bash
# Criar secret para JWT
echo -n "your-secure-secret-key-here" | gcloud secrets create jwt-secret-key \
  --replication-policy="automatic" \
  --data-file=-

# Criar secret para Redis URL (se usar Redis Cloud)
echo -n "redis://your-redis-host:6379/0" | gcloud secrets create redis-url \
  --replication-policy="automatic" \
  --data-file=-

# Listar secrets
gcloud secrets list
```

### 3. Criar Redis Cache (Memorystore)

```bash
# Criar instância Redis
gcloud redis instances create starwars-cache \
  --size=1 \
  --region=us-central1 \
  --redis-version=7.0

# Obter detalhes da instância
gcloud redis instances describe starwars-cache --region=us-central1

# Copiar host e porta para REDIS_URL
# Formato: redis://HOST:PORT/0
```

### 4. Deploy da Cloud Function

```bash
# Deploy básico
gcloud functions deploy starwars-api \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point starwars_api \
  --source . \
  --region us-central1 \
  --timeout 60 \
  --memory 512MB \
  --set-env-vars ENVIRONMENT=production,DEBUG=False,LOG_LEVEL=INFO

# Deploy com secrets
gcloud functions deploy starwars-api \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point starwars_api \
  --source . \
  --region us-central1 \
  --timeout 60 \
  --memory 512MB \
  --set-env-vars ENVIRONMENT=production,DEBUG=False,LOG_LEVEL=INFO,REDIS_URL=redis://your-redis-host:6379/0 \
  --secret jwt-secret-key=latest \
  --secret redis-url=latest
```

### 5. Obter URL da Cloud Function

```bash
# Obter URL
gcloud functions describe starwars-api --region us-central1 --format='value(httpsTrigger.url)'

# Testar
curl https://us-central1-YOUR_PROJECT_ID.cloudfunctions.net/starwars-api/health
```

### 6. Configurar API Gateway

#### 6.1 Atualizar openapi.yaml

Substituir `REGION-PROJECT_ID` pela sua região e project ID:

```bash
sed -i 's/REGION-PROJECT_ID/us-central1-YOUR_PROJECT_ID/g' openapi.yaml
```

#### 6.2 Criar API Gateway

```bash
# Criar API
gcloud api-gateway apis create starwars-api \
  --project=YOUR_PROJECT_ID

# Criar configuração
gcloud api-gateway api-configs create v1 \
  --api=starwars-api \
  --openapi-spec=openapi.yaml \
  --backend-auth-service-account=default \
  --project=YOUR_PROJECT_ID

# Criar gateway
gcloud api-gateway gateways create starwars-gateway \
  --api=starwars-api \
  --api-config=v1 \
  --location=us-central1 \
  --project=YOUR_PROJECT_ID

# Obter URL
gcloud api-gateway gateways describe starwars-gateway \
  --location=us-central1 \
  --format='value(defaultHostname)' \
  --project=YOUR_PROJECT_ID
```

### 7. Configurar Domínio Customizado (Opcional)

```bash
# Criar mapeamento de domínio
gcloud api-gateway api-configs describe v1 \
  --api=starwars-api \
  --format='value(serviceConfig.apis[0].syntax)' \
  --project=YOUR_PROJECT_ID

# Configurar DNS para apontar para API Gateway
# Adicionar registro CNAME no seu DNS provider
```

## Deployment com Docker

### 1. Build da Imagem

```bash
# Build local
docker build -t starwars-api:latest .

# Build para GCP (Artifact Registry)
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/starwars-api:latest

# Ou com Cloud Build
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION=us-central1,_SERVICE_NAME=starwars-api
```

### 2. Deploy em Cloud Run

```bash
# Deploy
gcloud run deploy starwars-api \
  --image gcr.io/YOUR_PROJECT_ID/starwars-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60 \
  --set-env-vars ENVIRONMENT=production,DEBUG=False,REDIS_URL=redis://your-redis-host:6379/0

# Obter URL
gcloud run services describe starwars-api \
  --region us-central1 \
  --format='value(status.url)'
```

## CI/CD com Cloud Build

### 1. Configurar Cloud Build

```bash
# Conectar repositório GitHub
gcloud builds connect --repository-name=starwars-api \
  --repository-owner=YOUR_GITHUB_USERNAME \
  --region=us-central1

# Ou usar Cloud Source Repositories
gcloud source repos create starwars-api
git remote add google https://source.developers.google.com/p/YOUR_PROJECT_ID/r/starwars-api
git push google main
```

### 2. Criar Trigger

```bash
# Criar trigger para branch main
gcloud builds triggers create github \
  --repo-name=starwars-api \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern=^main$ \
  --build-config=cloudbuild.yaml \
  --name=starwars-api-main
```

## Monitoramento e Logging

### 1. Visualizar Logs

```bash
# Logs da Cloud Function
gcloud functions logs read starwars-api --region us-central1 --limit 50

# Logs em tempo real
gcloud functions logs read starwars-api --region us-central1 --limit 50 --follow

# Logs com filtro
gcloud logging read "resource.type=cloud_function AND resource.labels.function_name=starwars-api" \
  --limit 50 \
  --format json
```

### 2. Criar Alertas

```bash
# Criar política de alerta para erros
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Star Wars API Errors" \
  --condition-display-name="High Error Rate" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

## Testes Pós-Deploy

### 1. Health Check

```bash
# Testar health endpoint
curl https://your-api-domain.com/health

# Resposta esperada:
# {
#   "status": "healthy",
#   "app": "Star Wars API",
#   "version": "1.0.0"
# }
```

### 2. Testar Endpoints

```bash
# Listar personagens
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-api-domain.com/api/characters

# Obter personagem específico
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-api-domain.com/api/characters/1

# Buscar personagens
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-api-domain.com/api/characters/search/luke
```

### 3. Teste de Carga

```bash
# Instalar Apache Bench
# macOS: brew install httpd
# Ubuntu: sudo apt-get install apache2-utils

# Teste de carga
ab -n 1000 -c 10 -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-api-domain.com/api/characters
```

## Rollback

### 1. Rollback de Cloud Function

```bash
# Listar versões
gcloud functions list-versions starwars-api --region us-central1

# Descrever versão específica
gcloud functions describe starwars-api --region us-central1 --gen2

# Fazer rollback (redeploy versão anterior)
gcloud functions deploy starwars-api \
  --runtime python39 \
  --trigger-http \
  --source . \
  --region us-central1
```

### 2. Rollback de API Gateway

```bash
# Listar configurações
gcloud api-gateway api-configs list --api=starwars-api

# Atualizar gateway para configuração anterior
gcloud api-gateway gateways update starwars-gateway \
  --api=starwars-api \
  --api-config=v0 \
  --location=us-central1
```

## Troubleshooting

### Problema: "Permission denied"

```bash
# Verificar permissões
gcloud projects get-iam-policy YOUR_PROJECT_ID

# Adicionar permissões
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member=serviceAccount:YOUR_SERVICE_ACCOUNT \
  --role=roles/cloudfunctions.developer
```

### Problema: "Function failed on loading user code"

```bash
# Verificar logs
gcloud functions logs read starwars-api --region us-central1 --limit 50

# Verificar requirements.txt
pip install -r requirements.txt

# Testar localmente
python -m src.presentation.main
```

### Problema: "Timeout"

```bash
# Aumentar timeout
gcloud functions deploy starwars-api \
  --timeout 120 \
  --region us-central1

# Aumentar memória
gcloud functions deploy starwars-api \
  --memory 1024MB \
  --region us-central1
```

### Problema: "Redis connection refused"

```bash
# Verificar instância Redis
gcloud redis instances describe starwars-cache --region us-central1

# Testar conexão
redis-cli -h YOUR_REDIS_HOST -p 6379 ping

# Verificar firewall
gcloud compute firewall-rules list --filter="name:redis"
```

## Checklist de Deploy

- [ ] Projeto GCP criado e configurado
- [ ] APIs habilitadas (Cloud Functions, API Gateway, etc)
- [ ] Secrets criados (JWT_SECRET_KEY, REDIS_URL)
- [ ] Redis Memorystore criado
- [ ] Cloud Function deployada
- [ ] API Gateway configurado
- [ ] Domínio customizado configurado (opcional)
- [ ] Cloud Build configurado
- [ ] Alertas configurados
- [ ] Testes pós-deploy realizados
- [ ] Documentação atualizada
- [ ] Backup configurado

## Próximos Passos

1. Configurar auto-scaling
2. Implementar CDN com Cloud CDN
3. Configurar WAF (Web Application Firewall)
4. Implementar rate limiting avançado
5. Configurar backup automático
6. Implementar disaster recovery
