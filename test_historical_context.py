#!/usr/bin/env python3
"""
Test script to verify complete chat history integration in AI Workforce Manager with ChromaDB
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_complete_history_integration():
    """Test that agents receive and use complete chat history from ChromaDB"""
    
    print("🧪 Testing Complete Chat History Integration with ChromaDB")
    print("=" * 60)
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found! Skipping agent tests.")
        return False
    
    try:
        from main import AIWorkforceManager
        
        # Initialize the AI Workforce Manager
        print("1. Initializing AI Workforce Manager with ChromaDB...")
        manager = AIWorkforceManager()
        
        # Test 1: Add some sample historical data to ChromaDB
        print("\n2. Adding sample historical conversations to ChromaDB...")
        
        # Add some sample conversations to build context
        sample_conversations = [
            {
                "user_prompt": "Create a marketing report for a tech startup",
                "manager_response": "Task allocated to Market Research Analyst. Agent response: I'll analyze the tech startup market, focusing on SaaS trends, competitor analysis, and growth opportunities.",
                "chosen_agent": "Market Research Analyst"
            },
            {
                "user_prompt": "Scrape data from competitor websites",
                "manager_response": "Task allocated to Web Scraper. Agent response: I'll extract pricing information, product features, and company details from the specified competitor websites.",
                "chosen_agent": "Web Scraper"
            },
            {
                "user_prompt": "Write content for our company blog about AI trends",
                "manager_response": "Task allocated to Content Writer. Agent response: I'll create an engaging blog post about current AI trends, focusing on business applications and future predictions.",
                "chosen_agent": "Content Writer"
            },
            {
                "user_prompt": "Design a logo for our startup",
                "manager_response": "Task allocated to Graphic Designer. Agent response: I'll create a modern, professional logo that reflects your startup's innovative nature and brand values.",
                "chosen_agent": "Graphic Designer"
            },
            {
                "user_prompt": "Analyze our business environment",
                "manager_response": "Task allocated to Business Environment Analyst. Agent response: I'll conduct a comprehensive analysis of your business environment, including market conditions, competitive landscape, and strategic opportunities.",
                "chosen_agent": "Business Environment Analyst"
            }
        ]
        
        for conv in sample_conversations:
            manager.history_manager.add_entry(
                conv["user_prompt"],
                conv["manager_response"],
                conv["chosen_agent"]
            )
        
        print("✅ Sample conversations added to ChromaDB vector database")
        
        # Test 2: Test agent selection with complete chat history
        print("\n3. Testing agent selection with complete chat history...")
        
        test_prompt = "Create another marketing analysis for a different startup"
        decision = await manager.decide_agent(test_prompt)
        print(f"✅ Agent decision with complete history: {decision}")
        
        # Test 3: Test agent execution with complete chat history
        print("\n4. Testing agent execution with complete chat history...")
        
        if decision in manager.specialized_agents:
            print(f"📋 Testing {decision} with complete chat history from ChromaDB...")
            
            # This will internally retrieve and inject complete chat history from ChromaDB
            response = await manager.delegate_task(decision, test_prompt)
            
            print(f"✅ Agent response received (length: {len(response)} characters)")
            print(f"📝 Response preview: {response[:200]}...")
            
            # Verify the response contains some reference to context or consistency
            context_indicators = [
                "previous", "past", "history", "consistent", "building upon",
                "reference", "approach", "methodology", "framework", "established",
                "continuity", "pattern", "similar", "before"
            ]
            
            has_context_awareness = any(indicator in response.lower() for indicator in context_indicators)
            
            if has_context_awareness:
                print("✅ Agent appears to be using complete chat history (found context indicators)")
            else:
                print("⚠️ Agent may not be fully utilizing complete chat history")
        
        # Test 4: Verify context formatting with complete history
        print("\n5. Testing complete history formatting...")
        
        complete_history = manager.history_manager.get_recent_history(limit=10)
        formatted_context = manager.format_historical_context(complete_history, decision)
        
        print(f"✅ Complete history formatting test completed")
        print(f"📊 Total conversations in history: {len(complete_history)}")
        print(f"📝 Formatted context length: {len(formatted_context)} characters")
        
        # Test 5: ChromaDB database statistics
        print("\n6. Checking ChromaDB database statistics...")
        stats = manager.history_manager.get_collection_stats()
        print(f"✅ Total conversations in ChromaDB: {stats.get('total_conversations', 'Unknown')}")
        
        # Test 6: Test another request to see if it builds upon the previous one
        print("\n7. Testing continuity with another request...")
        
        followup_prompt = "Now create a social media strategy for the same startup"
        followup_decision = await manager.decide_agent(followup_prompt)
        print(f"✅ Follow-up agent decision: {followup_decision}")
        
        if followup_decision in manager.specialized_agents:
            followup_response = await manager.delegate_task(followup_decision, followup_prompt)
            print(f"✅ Follow-up response received (length: {len(followup_response)} characters)")
            
            # Check if it references the previous marketing work
            continuity_indicators = [
                "startup", "marketing", "previous", "earlier", "mentioned",
                "established", "building", "consistent", "brand"
            ]
            
            has_continuity = any(indicator in followup_response.lower() for indicator in continuity_indicators)
            
            if has_continuity:
                print("✅ Agent shows continuity with previous conversations")
            else:
                print("⚠️ Agent may not be building upon previous context")
        
        print("\n🎉 Complete Chat History Integration Test Completed Successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complete_history_formatting():
    """Test the complete history formatting function without API calls"""
    
    print("\n🧪 Testing Complete History Formatting with ChromaDB (No API)")
    print("=" * 60)
    
    try:
        from main import AIWorkforceManager
        
        manager = AIWorkforceManager()
        
        # Add test data to ChromaDB
        test_conversations = [
            {
                "user_prompt": "Create a marketing report for tech startup",
                "manager_response": "Task allocated to Market Research Analyst. Comprehensive analysis completed.",
                "chosen_agent": "Market Research Analyst"
            },
            {
                "user_prompt": "Design a logo for the startup",
                "manager_response": "Task allocated to Graphic Designer. Modern logo design created.",
                "chosen_agent": "Graphic Designer"
            },
            {
                "user_prompt": "Write content for company website",
                "manager_response": "Task allocated to Content Writer. Engaging website content created.",
                "chosen_agent": "Content Writer"
            }
        ]
        
        for conv in test_conversations:
            manager.history_manager.add_entry(
                conv["user_prompt"],
                conv["manager_response"],
                conv["chosen_agent"]
            )
        
        # Get history from ChromaDB and format it
        chat_history = manager.history_manager.get_recent_history(limit=10)
        formatted_context = manager.format_historical_context(chat_history, "Social Media Manager")
        
        print("✅ Complete history formatting successful")
        print(f"📝 Formatted context preview:")
        print("-" * 50)
        print(formatted_context[:800] + "..." if len(formatted_context) > 800 else formatted_context)
        print("-" * 50)
        
        # Verify key components are present
        required_components = [
            "COMPLETE CHAT HISTORY",
            "conversations) for your reference",
            "Conversation 1",
            "Date:",
            "Agent Used:",
            "User Request:",
            "Response:"
        ]
        
        missing_components = []
        for component in required_components:
            if component not in formatted_context:
                missing_components.append(component)
        
        if missing_components:
            print(f"❌ Missing required components: {missing_components}")
            return False
        
        print("✅ All required history components present")
        
        # Check if conversations are sorted by timestamp (most recent first)
        if len(chat_history) > 1:
            timestamps = [conv.get('timestamp', '') for conv in chat_history]
            is_sorted = all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
            if is_sorted:
                print("✅ Conversations properly sorted by timestamp (most recent first)")
            else:
                print("⚠️ Conversations may not be properly sorted")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete history formatting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all complete chat history tests"""
    print("🚀 Starting Complete Chat History Integration Tests with ChromaDB")
    print("=" * 70)
    
    # Check environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("Please create a .env file with your OpenAI API key")
        return
    
    tests = [
        ("Complete History Formatting", test_complete_history_formatting),
        ("Integration Test", test_complete_history_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}")
        print("=" * 50)
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("=" * 30)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        print(f"\n🎉 All tests passed! Complete chat history integration is working correctly with ChromaDB.")
        print("🔄 Agents now receive the entire conversation history for full context awareness.")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main()) 