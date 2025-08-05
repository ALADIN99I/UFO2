#!/usr/bin/env python3
"""
Quick test of the improved LLM client to verify fixes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from llm.llm_client import LLMClient
import json

def test_llm_client():
    """Test the improved LLM client with various scenarios"""
    
    # Load config
    import configparser
    config = configparser.ConfigParser()
    config_path = os.path.join('config', 'config.ini')
    config.read(config_path)
    
    print("🧪 Testing improved LLM client...")
    print(f"Model: anthropic/claude-3-haiku:beta")
    
    # Initialize client
    llm_client = LLMClient(api_key=config['openrouter']['api_key'])
    
    # Test simple prompt
    test_prompt = """
Please respond with a simple JSON object testing connection:
{
    "status": "success",
    "message": "LLM client working properly",
    "test_value": 123
}
"""
    
    print("\n📡 Sending test request...")
    response = llm_client.generate_response(test_prompt, timeout=30)
    
    print("\n📥 Response received:")
    print("=" * 50)
    print(response)
    print("=" * 50)
    
    # Try to parse as JSON if possible
    try:
        if '{' in response and '}' in response:
            # Extract JSON part
            import re
            json_match = re.search(r'{.*}', response, re.DOTALL)
            if json_match:
                json_response = json.loads(json_match.group(0))
                print("\n✅ JSON validation successful:")
                print(json.dumps(json_response, indent=2))
    except Exception as e:
        print(f"\n⚠️ JSON parsing failed: {e}")
    
    print("\n🎯 LLM client test completed!")

if __name__ == "__main__":
    test_llm_client()
