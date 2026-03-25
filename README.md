# Flask MCP-Style Sample Server (Dockerized)

This project provides a lightweight Flask API server that is ready to run in Docker and host on **Azure Container Apps**.

## Endpoints

1. **IFSC Search (sample)**
   - `GET /api/v1/ifsc/<ifsc_code>`
   - Returns the same sample bank details for any IFSC.
   - Echoes back the requested IFSC in `requested_ifsc`.

2. **Sample FX Quote**
   - `POST /api/v1/fx-quote`
   - Accepts JSON: `base_currency`, `quote_currency`, `amount`
   - Returns a deterministic sample conversion quote.

3. **Health**
   - `GET /health`

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Server starts on `http://localhost:8000`.

## Docker

Build and run:

```bash
docker build -t flask-mcp-server:latest .
docker run --rm -p 8000:8000 flask-mcp-server:latest
```

## Azure Container Apps deployment

Example using Azure CLI (replace names as needed):

```bash
# Variables
RESOURCE_GROUP=rg-mcp-demo
LOCATION=eastus
ACR_NAME=mcpdemoacr123
ENV_NAME=mcp-env
APP_NAME=flask-mcp-server
IMAGE_NAME=flask-mcp-server
TAG=v1

# Login
az login

# Resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# ACR
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic
az acr login --name $ACR_NAME

# Build + push image
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
docker build -t $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG .
docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG

# Container Apps environment
az containerapp env create \
  --name $ENV_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Create app
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENV_NAME \
  --image $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG \
  --target-port 8000 \
  --ingress external \
  --registry-server $ACR_LOGIN_SERVER
```

## Sample requests

```bash
curl http://localhost:8000/api/v1/ifsc/SBIN0000123
```

```bash
curl -X POST http://localhost:8000/api/v1/fx-quote \
  -H "Content-Type: application/json" \
  -d '{"base_currency":"USD", "quote_currency":"INR", "amount":100}'
```
