# Sadapurne MCP Server (Web API Version)

This is a web API wrapper for the MCP (Model Context Protocol) server functionality that provides HTTP endpoints for accessing verified producer data from Supabase.

## API Endpoints

### Root Endpoint
```
GET /
```
Returns API information and available endpoints.

### Health Check
```
GET /health
```
Returns the health status of the API.

### Get Producer by Aadhaar Number
```
POST /api/producer/aadhar
```
Get verified producer information by Aadhaar number.

**Request Body:**
```json
{
  "aadhar": "string"
}
```

### Search Producers by Name
```
POST /api/producer/name
```
Search for verified producers by name.

**Request Body:**
```json
{
  "name": "string"
}
```

### Get All Verified Producers
```
GET /api/producers
```
Get all verified producers.

### Get Producer by FSSAI License Number
```
POST /api/producer/fssai
```
Get verified producer information by FSSAI license number.

**Request Body:**
```json
{
  "fssai_number": "string"
}
```

## Deployment

This server is designed to be deployed on Render as a web service using the provided Dockerfile and render.yaml configuration.

## Environment Variables

The following environment variables must be set:
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key