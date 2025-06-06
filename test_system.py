#!/usr/bin/env python3
"""
Test script for AI Workforce Manager system with ChromaDB vector database integration.
This script verifies that all components are working correctly.
"""

import os
import asyncio
from dotenv import load_dotenv

def test_chat_history_manager():
    """Test the ChatHistoryManager with ChromaDB vector database"""
    print("🧪 Testing ChatHistoryManager with ChromaDB")
    print("=" * 50)
    
    try:
        from chat_history_manager import ChatHistoryManager
        
        # Initialize the history manager
        history_manager = ChatHistoryManager()
        print("✅ ChatHistoryManager initialized successfully")
        
        # Test adding entries
        print("\n📝 Adding test entries to ChromaDB...")
        history_manager.add_entry(
            "Test user prompt 1", 
            "Test manager response 1", 
            chosen_agent="Web Scraper"
        )
        
        history_manager.add_entry(
            "Create a marketing analysis", 
            "Task allocated to Market Research Analyst", 
            chosen_agent="Market Research Analyst"
        )
        
        print("✅ Test entries added successfully")
        
        # Test similarity search
        print("\n🔍 Testing similarity search...")
        similar = history_manager.search_similar_conversations("marketing", n_results=2)
        print(f"Found {len(similar)} similar conversations")
        
        if similar:
            for i, conv in enumerate(similar, 1):
                similarity_score = conv.get('similarity_score', conv.get('similarity', 0))
                chosen_agent = conv.get('metadata', {}).get('chosen_agent', conv.get('chosen_agent', 'Unknown'))
                print(f"{i}. Similarity: {similarity_score:.3f}, Agent: {chosen_agent}")
        else:
            print("No similar conversations found")
        
        # Test recent history
        print("\n📚 Testing recent history retrieval...")
        recent = history_manager.get_recent_history(limit=5)
        print(f"Retrieved {len(recent)} recent conversations")
        
        if recent:
            for entry in recent[:2]:  # Show first 2
                print(f"- {entry['timestamp'][:19]}: {entry['user_prompt'][:30]}... -> {entry['chosen_agent']}")
        else:
            print("No recent history found")
        
        # Test collection stats
        print("\n📊 Testing collection statistics...")
        stats = history_manager.get_collection_stats()
        print(f"Total conversations: {stats['total_conversations']}")
        print(f"Collection: {stats['collection_name']}")
        print(f"Database path: {stats['database_path']}")
        
        print("✅ ChatHistoryManager tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ ChatHistoryManager test failed: {e}")
        return False

def test_environment_setup():
    """Test environment setup and dependencies"""
    print("🧪 Testing Environment Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key found")
    else:
        print("❌ OpenAI API key not found")
        return False
    
    # Test ChromaDB import
    try:
        import chromadb
        print("✅ ChromaDB imported successfully")
    except ImportError as e:
        print(f"❌ ChromaDB import failed: {e}")
        return False
    
    # Test other dependencies
    try:
        from agents import Agent, Runner
        print("✅ OpenAI Agents SDK imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI Agents SDK import failed: {e}")
        return False
    
    print("✅ Environment setup tests completed successfully")
    return True

async def test_agent_initialization():
    """Test agent initialization"""
    print("🧪 Testing Agent Initialization")
    print("=" * 50)
    
    try:
        from main import AIWorkforceManager
        
        # This will test the full initialization including ChromaDB
        manager = AIWorkforceManager()
        print("✅ AI Workforce Manager initialized successfully")
        
        # Test that we have the expected agents
        expected_agents = [
            "Web Scraper", "Business Environment Analyst", "Market Research Analyst",
            "Data Analyst", "Content Writer", "Social Media Manager", 
            "Social Media Video Creator", "Graphic Designer", "Video Editor",
            "PDF Producer", "PowerPoint Producer", "Pitch Deck Producer"
        ]
        
        for agent_name in expected_agents:
            if agent_name in manager.specialized_agents:
                print(f"✅ {agent_name} agent found")
            else:
                print(f"❌ {agent_name} agent missing")
                return False
        
        print("✅ Agent initialization tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AI Workforce Manager System Tests")
    print("=" * 60)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("ChatHistoryManager with ChromaDB", test_chat_history_manager),
        ("Agent Initialization", lambda: asyncio.run(test_agent_initialization())),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")
            results.append((test_name, False))
        
        print("-" * 50)
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 30)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
        print("\nCommon fixes:")
        print("- Ensure .env file exists with OPENAI_API_KEY")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Check ChromaDB installation: pip install chromadb==0.3.21")
        print("- Ensure proper file permissions for ChromaDB database directory")

if __name__ == "__main__":
    main() 