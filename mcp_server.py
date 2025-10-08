#!/usr/bin/env python3
import asyncio
import os
from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent, PromptMessage
import mcp.server.stdio
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from workspace .env
load_dotenv(dotenv_path="d:/sadapurne-ai/.env")

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

server = Server("supabase-agent1-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_verified_producer_by_aadhar",
            description="Get verified producer information by Aadhaar number",
            inputSchema={
                "type": "object",
                "properties": {
                    "aadhar": {"type": "string", "description": "The Aadhaar number of the producer"}
                },
                "required": ["aadhar"]
            }
        ),
        Tool(
            name="get_verified_producer_by_name",
            description="Search for verified producers by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The name to search for"}
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="get_all_verified_producers",
            description="Get all verified producers",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_producer_by_fssai",
            description="Get verified producer information by FSSAI license number",
            inputSchema={
                "type": "object",
                "properties": {
                    "fssai_number": {"type": "string", "description": "The FSSAI license number"}
                },
                "required": ["fssai_number"]
            }
        ),
        Tool(
            name="get_producer_by_pin",
            description="Get verified producer information by PIN",
            inputSchema={
                "type": "object",
                "properties": {
                    "pin": {"type": "integer", "description": "The PIN number"}
                },
                "required": ["pin"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_verified_producer_by_aadhar":
        aadhar = arguments["aadhar"]
        try:
            result = supabase.table('verified_producers').select('*').eq('aadhar', aadhar).execute()

            if result.data:
                import json
                return [TextContent(type="text", text=json.dumps(result.data[0], indent=2))]
            else:
                return [TextContent(type="text", text="No verified producer found with this Aadhaar number")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "get_verified_producer_by_name":
        name_search = arguments["name"]
        try:
            result = supabase.table('verified_producers').select('*').ilike('name', f'%{name_search}%').execute()

            if result.data:
                import json
                return [TextContent(type="text", text=json.dumps(result.data, indent=2))]
            else:
                return [TextContent(type="text", text="No verified producers found with this name")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "get_all_verified_producers":
        try:
            result = supabase.table('verified_producers').select('*').execute()

            if result.data:
                import json
                return [TextContent(type="text", text=json.dumps(result.data, indent=2))]
            else:
                return [TextContent(type="text", text="No verified producers found")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "get_producer_by_fssai":
        fssai_number = arguments["fssai_number"]
        try:
            result = supabase.table('verified_producers').select('*').eq('fssai_license_number', fssai_number).execute()

            if result.data:
                import json
                return [TextContent(type="text", text=json.dumps(result.data[0], indent=2))]
            else:
                return [TextContent(type="text", text="No verified producer found with this FSSAI number")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "get_producer_by_pin":
        pin = arguments["pin"]
        try:
            result = supabase.table('verified_producers').select('*').eq('pin', pin).execute()

            if result.data:
                import json
                return [TextContent(type="text", text=json.dumps(result.data[0], indent=2))]
            else:
                return [TextContent(type="text", text="No verified producer found with this PIN")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    # Import here to avoid issues if stdio is not available
    import mcp.server.stdio
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())