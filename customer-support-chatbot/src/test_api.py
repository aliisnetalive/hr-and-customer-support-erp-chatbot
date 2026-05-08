#!/usr/bin/env python3
"""
Customer Support Chatbot API - Test Client
Interactive client to test the API
"""

import requests
import json
import sys
from typing import Dict, Any

API_BASE_URL = "http://localhost:5000"

class ChatbotAPIClient:
    """API client"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check health"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "unreachable"}
    
    def get_config(self) -> Dict[str, Any]:
        """Get config"""
        try:
            response = self.session.get(f"{self.base_url}/config")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask question"""
        try:
            response = self.session.post(
                f"{self.base_url}/ask",
                json={"question": question},
                timeout=120
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

def print_response(response: Dict[str, Any]):
    """Print response nicely"""
    print(f"\n{'='*60}")
    
    if "error" in response and not response.get("success", False):
        print(f"Error: {response.get('error')}")
    else:
        if "answer" in response:
            print(f"Answer:\n{response['answer']}")
        if "sources" in response:
            print(f"\nSources (Pages): {', '.join(map(str, response['sources']))}")
        if "processing_time_ms" in response:
            print(f"Time: {response['processing_time_ms']}ms")
    
    print(f"{'='*60}\n")

def main():
    """Main"""
    print("\n🤖 HR CHATBOT API - TEST CLIENT\n")
    
    client = ChatbotAPIClient()
    
    # 1. Health check
    print("1️⃣  Checking API Health...")
    health = client.health_check()
    if health.get("status") == "ok":
        print(f"✅ API is healthy | Chatbot Ready: {health.get('chatbot_ready')}\n")
    else:
        print(f"❌ API Error: {health.get('error')}\n")
        sys.exit(1)
    
    # 2. Config
    print("2️⃣  Configuration:")
    config = client.get_config()
    if "error" not in config:
        for key, value in config.items():
            print(f"   {key}: {value}")
        print()
    
    # 3. Sample questions
    print("3️⃣  Sample Questions:\n")
    
    samples = [
        "What is the policy on sick leave?",
        "How many days of casual leave am I entitled to?",
        "What is the maternity leave policy?"
    ]
    
    for question in samples:
        print(f"Q: {question}")
        response = client.ask_question(question)
        if response.get("success"):
            print(f"✅ Answer: {response.get('answer', '')[:100]}...")
        else:
            print(f"❌ Error: {response.get('error')}")
        print()
    
    # 4. Interactive
    print("\n4️⃣  Interactive Mode (type 'quit' to exit)\n")
    
    while True:
        try:
            question = input("❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
            
            response = client.ask_question(question)
            print_response(response)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
