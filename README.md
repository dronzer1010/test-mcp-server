# MCP-Compliant Sample Server (Dockerized, Azure-ready)

This repository now contains a **real MCP server** (Model Context Protocol) built with the official Python MCP SDK (`FastMCP`).

It is designed for remote hosting on **Azure Container Apps** using **Streamable HTTP** transport.

## Exposed MCP Tools

1. `search_ifsc`
   - Input: `ifsc_code: string`
   - Behavior: Always returns the same sample bank details and echoes `requested_ifsc`.

2. `sample_fx_quote`
   - Input: `amount?: number`, `base_currency?: string`, `quote_currency?: string`
   - Behavior: Returns a deterministic sample FX quote payload.

## Run locally (MCP over HTTP)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python mcp_server.py
```

Default server URL: `http://localhost:8000/mcp`

## Docker

```bash
docker build -t ifsc-fx-mcp:latest .
docker run --rm -p 8000:8000 ifsc-fx-mcp:latest
```

The container starts the MCP server in `streamable-http` mode.

## Azure Container Apps deployment

```bash
RESOURCE_GROUP=rg-mcp-demo
LOCATION=eastus
ACR_NAME=mcpdemoacr123
ENV_NAME=mcp-env
APP_NAME=ifsc-fx-mcp-server
IMAGE_NAME=ifsc-fx-mcp-server
TAG=v1

az login
az group create --name $RESOURCE_GROUP --location $LOCATION

az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic
az acr login --name $ACR_NAME

ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
docker build -t $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG .
docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG

az containerapp env create \
  --name $ENV_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENV_NAME \
  --image $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG \
  --target-port 8000 \
  --ingress external \
  --registry-server $ACR_LOGIN_SERVER \
  --env-vars MCP_TRANSPORT=streamable-http
```

After deployment, your MCP endpoint is:

`https://<your-container-app-domain>/mcp`

## Testing the MCP server

### Option A: MCP Inspector

```bash
npx -y @modelcontextprotocol/inspector
```

Then connect to:
- Transport: Streamable HTTP
- URL: `http://localhost:8000/mcp` (or your Azure URL)

### Option B: Any MCP client

Use any MCP-compatible client and point it to your `/mcp` URL.

## Access from OpenAI

To use this with OpenAI-powered apps, use an MCP-capable OpenAI integration path (for example, an OpenAI app/agent runtime that supports remote MCP servers), then register your MCP URL:

- Local: `http://localhost:8000/mcp`
- Azure: `https://<your-container-app-domain>/mcp`

Once connected, the client will discover the tools (`search_ifsc`, `sample_fx_quote`) via `tools/list` and invoke them via `tools/call`.

## Notes

- This is now MCP protocol-native, not plain REST.
- The responses are deterministic and intended for integration testing/demo use.
