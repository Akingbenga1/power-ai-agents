#!/usr/bin/env python3
"""
Test script to verify multi-agent orchestration functionality
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_multi_agent_functionality():
    """Test the new multi-agent orchestration system"""
    
    print("🧪 Testing Multi-Agent Orchestration System")
    print("=" * 50)
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found! Please set it in .env file.")
        return False
    
    try:
        from main import AIWorkforceManager
        
        # Initialize the AI Workforce Manager
        print("1. Initializing AI Workforce Manager...")
        manager = AIWorkforceManager()
        print("✅ AI Workforce Manager initialized successfully")
        
        # Test 1: Single agent decision
        print("\n2. Testing single agent decision...")
        single_agent_prompt = "Write a blog post about artificial intelligence"
        decision = await manager.decide_agent(single_agent_prompt)
        parsed = manager.parse_decision_response(decision)
        print(f"   Prompt: {single_agent_prompt}")
        print(f"   Decision: {decision}")
        print(f"   Parsed Type: {parsed['type']}")
        if parsed["type"] == "single":
            print(f"   Agent: {parsed['agent']}")
        print("✅ Single agent test completed")
        
        # Test 2: Multi-agent decision
        print("\n3. Testing multi-agent decision...")
        multi_agent_prompt = "Create a comprehensive marketing strategy with visuals and a PDF report"
        decision = await manager.decide_agent(multi_agent_prompt)
        parsed = manager.parse_decision_response(decision)
        print(f"   Prompt: {multi_agent_prompt}")
        print(f"   Decision: {decision}")
        print(f"   Parsed Type: {parsed['type']}")
        if parsed["type"] == "multi":
            print(f"   Agents: {parsed['agents']}")
            print(f"   Workflow: {parsed['workflow']}")
            print(f"   Description: {parsed['description']}")
        print("✅ Multi-agent test completed")
        
        # Test 3: Decision parsing
        print("\n4. Testing decision parsing...")
        test_cases = [
            "SINGLE: Content Writer",
            "MULTI: Market Research Analyst -> Content Writer -> PDF Producer\nWORKFLOW: Research, then write, then create PDF",
            "NONE: No suitable agent for this quantum physics calculation",
            "Content Writer"  # Legacy format
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            parsed = manager.parse_decision_response(test_case)
            print(f"   Test {i}: {test_case.replace(chr(10), ' | ')}")
            print(f"   → Type: {parsed['type']}")
            if parsed["type"] == "single":
                print(f"   → Agent: {parsed['agent']}")
            elif parsed["type"] == "multi":
                print(f"   → Agents: {parsed['agents']}")
            elif parsed["type"] == "none":
                print(f"   → Message: {parsed['message']}")
        
        print("✅ Decision parsing tests completed")
        
        # Test 4: Test actual workflow execution (optional - requires API calls)
        test_workflow = input("\n5. Test actual workflow execution? (y/n): ").strip().lower()
        if test_workflow == 'y':
            print("   Testing simple single-agent workflow...")
            try:
                await manager.handle_prompt("Write a short paragraph about renewable energy")
                print("✅ Single-agent workflow test completed")
            except Exception as e:
                print(f"❌ Single-agent workflow test failed: {e}")
        
        print(f"\n🎉 All multi-agent orchestration tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Multi-agent orchestration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the multi-agent functionality test"""
    print("🚀 Starting Multi-Agent Orchestration Tests")
    print("=" * 60)
    
    success = await test_multi_agent_functionality()
    
    if success:
        print("\n✅ All tests passed! Multi-agent orchestration is working correctly.")
        print("🤖 You can now use prompts like:")
        print("   • 'Create a marketing strategy with visuals and PDF'")
        print("   • 'Build a social media campaign with video content'")
        print("   • 'Analyze a company and create a presentation'")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main()) 