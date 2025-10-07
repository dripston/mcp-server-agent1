# Sadapurne MCP Server

This is an MCP (Model Context Protocol) server that provides tools for accessing verified producer data from Supabase.

## Tools Provided

1. `get_verified_producer_by_aadhar` - Get producer information by Aadhaar number
2. `get_verified_producer_by_name` - Search for producers by name
3. `get_all_verified_producers` - Get all verified producers
4. `get_producer_by_fssai` - Get producer information by FSSAI license number

## Deployment

This server is designed to be deployed on Render using the provided Dockerfile and render.yaml configuration.

## Environment Variables

The following environment variables must be set:
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key