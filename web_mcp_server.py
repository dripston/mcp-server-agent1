#!/usr/bin/env python3
"""
Web wrapper for MCP server to expose functionality via HTTP endpoints
"""
import os
import json
import asyncio
from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "message": "Sadapurne MCP Server API",
        "version": "1.0.0",
        "endpoints": {
            "get_verified_producer_by_aadhar": "POST /api/producer/aadhar",
            "get_verified_producer_by_name": "POST /api/producer/name",
            "get_all_verified_producers": "GET /api/producers",
            "get_producer_by_fssai": "POST /api/producer/fssai"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "MCP Server API is running"}), 200

@app.route('/api/producer/aadhar', methods=['POST'])
def get_verified_producer_by_aadhar():
    """Get verified producer information by Aadhaar number"""
    try:
        data = request.get_json()
        if not data or 'aadhar' not in data:
            return jsonify({"error": "Missing 'aadhar' in request body"}), 400
        
        aadhar = data['aadhar']
        result = supabase.table('verified_producers').select('*').eq('aadhar', aadhar).execute()

        if result.data:
            return jsonify({
                "status": "success",
                "data": result.data[0]
            }), 200
        else:
            return jsonify({
                "status": "not_found",
                "message": "No verified producer found with this Aadhaar number"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/producer/name', methods=['POST'])
def get_verified_producer_by_name():
    """Search for verified producers by name"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Missing 'name' in request body"}), 400
        
        name_search = data['name']
        result = supabase.table('verified_producers').select('*').ilike('name', f'%{name_search}%').execute()

        if result.data:
            return jsonify({
                "status": "success",
                "data": result.data
            }), 200
        else:
            return jsonify({
                "status": "not_found",
                "message": "No verified producers found with this name"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/producers', methods=['GET'])
def get_all_verified_producers():
    """Get all verified producers"""
    try:
        result = supabase.table('verified_producers').select('*').execute()

        if result.data:
            return jsonify({
                "status": "success",
                "data": result.data
            }), 200
        else:
            return jsonify({
                "status": "not_found",
                "message": "No verified producers found"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/producer/fssai', methods=['POST'])
def get_producer_by_fssai():
    """Get verified producer information by FSSAI license number"""
    try:
        data = request.get_json()
        if not data or 'fssai_number' not in data:
            return jsonify({"error": "Missing 'fssai_number' in request body"}), 400
        
        fssai_number = data['fssai_number']
        result = supabase.table('verified_producers').select('*').eq('fssai_license_number', fssai_number).execute()

        if result.data:
            return jsonify({
                "status": "success",
                "data": result.data[0]
            }), 200
        else:
            return jsonify({
                "status": "not_found",
                "message": "No verified producer found with this FSSAI number"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

if __name__ == "__main__":
    # Run the Flask app
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)