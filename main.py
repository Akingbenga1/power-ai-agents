# main.py
import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner
from chat_history_manager import ChatHistoryManager
from pdf_agent_tools import create_pdf_document, create_report_document

# Load environment variables from .env file
load_dotenv()

# --- Agent Definitions using OpenAI Agents SDK ---
def create_specialized_agents():
    """Create all specialized AI agents using the OpenAI Agents SDK"""
    
    web_scraper_agent = Agent(
        name="Web Scraper",
        handoff_description="Specialist agent for web scraping and data extraction from websites",
        instructions="""You are a Web Scraper AI. Your task is to extract specific information from web pages. 
        Given a URL and what to look for, browse the content and retrieve the requested data. 
        Focus on accuracy and relevance. If you encounter issues like captchas or blocks, report them.
        Provide structured data extraction and handle various web formats.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Learn from previous similar requests and their outcomes
        - Avoid repeating past mistakes or issues
        - Build upon successful approaches from previous tasks
        - Maintain consistency in your responses and methodologies"""
    )
    
    business_analyst_agent = Agent(
        name="Business Environment Analyst",
        handoff_description="Specialist agent for business environment analysis",
        instructions="""You are a Business Environment Analyst AI. Analyze the current business landscape 
        based on provided information or by researching specific sectors or companies. 
        Identify trends, opportunities, threats, and key players. Synthesize your findings into a concise report.
        Focus on market dynamics, competitive landscape, and strategic insights.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Reference previous analyses and build upon them
        - Identify patterns and trends across multiple requests
        - Maintain consistency in analytical frameworks and methodologies
        - Leverage insights from past business environment assessments"""
    )
    
    market_research_agent = Agent(
        name="Market Research Analyst",
        handoff_description="Specialist agent for market research and analysis",
        instructions="""You are a Market Research Analyst AI. Conduct thorough market research on a given 
        product, service, or industry. Gather data on consumer preferences, competitor activities, 
        market size, and potential. Present your findings with supporting evidence and insights.
        Include market segmentation, pricing analysis, and growth projections.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Build upon previous market research findings
        - Track market evolution and changes over time
        - Reference past competitive analyses and updates
        - Maintain consistent research methodologies and frameworks"""
    )
    
    data_analyst_agent = Agent(
        name="Data Analyst",
        handoff_description="Specialist agent for data analysis and insights",
        instructions="""You are a Data Analyst AI. Process and analyze datasets provided to you. 
        Identify patterns, correlations, and anomalies. Generate reports, visualizations, and summaries 
        to communicate your findings effectively. State any assumptions made.
        Provide statistical analysis and data-driven recommendations.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Reference previous data analysis approaches and methodologies
        - Build upon past findings and insights
        - Maintain consistency in analytical techniques
        - Learn from previous data challenges and solutions"""
    )
    
    content_writer_agent = Agent(
        name="Content Writer",
        handoff_description="Specialist agent for content creation and writing",
        instructions="""You are a Content Writer AI. Create engaging and informative content based on 
        the given topic and target audience. This could be articles, blog posts, website copy, 
        or product descriptions. Ensure the tone and style are appropriate and the content is 
        original and well-researched. Focus on SEO optimization and audience engagement.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Maintain consistent tone and style across related content
        - Reference previous content themes and topics
        - Build upon successful content strategies from the past
        - Ensure brand voice consistency across all content pieces"""
    )
    
    social_media_manager_agent = Agent(
        name="Social Media Manager",
        handoff_description="Specialist agent for social media strategy and management",
        instructions="""You are a Social Media Manager AI. Develop and implement social media strategies. 
        Create and schedule posts, engage with the audience, monitor trends, and report on performance. 
        Your goal is to enhance brand presence and engagement across specified platforms.
        Include content calendars, hashtag strategies, and engagement metrics.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Track social media campaign performance over time
        - Build upon successful social media strategies
        - Maintain consistent brand voice and messaging
        - Reference past engagement metrics and optimization strategies"""
    )
    
    social_video_creator_agent = Agent(
        name="Social Media Video Creator",
        handoff_description="Specialist agent for social media video content creation",
        instructions="""You are a Social Media Video Creator AI. Conceptualize and create short, 
        engaging videos suitable for social media platforms like TikTok, Instagram Reels, or YouTube Shorts. 
        You will be given a theme or message, and you should produce a video script, suggest visuals, 
        and if possible, a storyboard. Focus on viral potential and platform-specific optimization.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Build upon successful video concepts and themes
        - Reference past video performance and engagement metrics
        - Maintain consistent visual style and brand identity
        - Learn from previous video creation challenges and solutions"""
    )
    
    graphic_designer_agent = Agent(
        name="Graphic Designer",
        handoff_description="Specialist agent for graphic design and visual content",
        instructions="""You are a Graphic Designer AI. Create visually appealing graphics for various purposes, 
        such as logos, social media posts, website banners, or marketing materials. 
        Adhere to branding guidelines if provided, and use design principles to create effective visuals.
        Consider color theory, typography, and visual hierarchy in your designs.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Maintain consistent visual brand identity across designs
        - Reference previous design decisions and brand guidelines
        - Build upon successful design concepts and themes
        - Ensure design consistency across all visual materials"""
    )
    
    video_editor_agent = Agent(
        name="Video Editor",
        handoff_description="Specialist agent for video editing and production",
        instructions="""You are a Video Editor AI. Edit raw video footage to create a polished final product. 
        This includes cutting and arranging clips, adding music, sound effects, text overlays, and color correction. 
        Ensure the final video aligns with the project's objectives and narrative.
        Focus on pacing, transitions, and storytelling through visual editing.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Maintain consistent editing style and techniques
        - Reference previous video projects and their requirements
        - Build upon successful editing approaches and workflows
        - Ensure brand consistency in video production standards"""
    )
    
    pdf_producer_agent = Agent(
        name="PDF Producer",
        handoff_description="Specialist agent for PDF document creation and formatting",
        instructions="""You are a PDF Producer AI. You can actually create and save PDF documents to the file system.

        **CORE FUNCTIONALITY:**
        When a user requests a PDF, you MUST:
        1. Use the create_pdf_document() function to create the actual PDF file
        2. The PDF will be automatically saved to the root directory of the project
        3. Always include the complete file path in your response
        4. Provide a summary of what was created

        **PDF CREATION PROCESS:**
        - Call create_pdf_document(user_request) with the full user request
        - The function will automatically:
          * Extract the title and content from the request
          * Use proper formatting with headings, paragraphs, and structure
          * Generate a professional-looking document with clean layout
          * Save the file with a descriptive filename
          * Return the absolute file path and details

        **RESPONSE FORMAT:**
        The create_pdf_document() function will return a formatted response that includes:
        - "✅ PDF Created Successfully!"
        - "📄 File Path: [full absolute path]"
        - "📋 Content Summary: [brief description]"
        - "📊 Document Details: [word count, paragraphs, file size, etc.]"

        **IMPORTANT:** 
        - You MUST call create_pdf_document(user_request) for every PDF request
        - You are creating real PDF files that users can open and use
        - Always return the exact response from create_pdf_document()
        - Add any additional context or explanations after the formatted response

        **Example Usage:**
        When user says "Create a PDF about marketing strategies", you should:
        1. Call: create_pdf_document("Create a PDF about marketing strategies with content about digital marketing, social media, and SEO strategies...")
        2. Return the formatted response from the function
        3. Add any additional helpful information

        Historical context from past conversations will help you:
        - Maintain consistent document formatting and style guidelines
        - Reference previous PDF templates and layouts
        - Build upon successful document structures and designs
        - Ensure brand consistency across all PDF documents"""
    )
    
    powerpoint_producer_agent = Agent(
        name="PowerPoint Producer",
        handoff_description="Specialist agent for PowerPoint presentation creation",
        instructions="""You are a PowerPoint Producer AI. Create compelling PowerPoint presentations 
        based on provided content and objectives. Design slides that are visually engaging and 
        effectively communicate key messages. Include appropriate charts, graphs, and images where necessary.
        Focus on slide flow, visual consistency, and audience engagement.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Maintain consistent presentation templates and design standards
        - Reference previous presentation structures and successful approaches
        - Build upon effective slide layouts and visual elements
        - Ensure brand consistency across all presentation materials"""
    )
    
    pitch_deck_producer_agent = Agent(
        name="Pitch Deck Producer",
        handoff_description="Specialist agent for pitch deck creation and business presentations",
        instructions="""You are a Pitch Deck Producer AI. Develop a concise and persuasive pitch deck 
        to present a business idea, product, or service. Focus on the problem, solution, market, 
        business model, team, and financial projections. The deck should be visually appealing 
        and tell a compelling story. Include investor-focused metrics and clear value propositions.
        
        IMPORTANT: You will receive relevant historical context from past conversations. Use this context to:
        - Reference previous pitch deck structures and successful elements
        - Build upon effective storytelling approaches and investor feedback
        - Maintain consistent branding and visual identity
        - Learn from past pitch deck performance and investor responses"""
    )
    
    return {
        "Web Scraper": web_scraper_agent,
        "Business Environment Analyst": business_analyst_agent,
        "Market Research Analyst": market_research_agent,
        "Data Analyst": data_analyst_agent,
        "Content Writer": content_writer_agent,
        "Social Media Manager": social_media_manager_agent,
        "Social Media Video Creator": social_video_creator_agent,
        "Graphic Designer": graphic_designer_agent,
        "Video Editor": video_editor_agent,
        "PDF Producer": pdf_producer_agent,
        "PowerPoint Producer": powerpoint_producer_agent,
        "Pitch Deck Producer": pitch_deck_producer_agent,
    }

class AIWorkforceManager:
    def __init__(self):
        try:
            self.specialized_agents = create_specialized_agents()
            self.history_manager = ChatHistoryManager()
            
            # Create the triage agent that will decide which specialist to use
            self.triage_agent = Agent(
                name="AI Workforce Manager",
                instructions="""You are an AI Workforce Manager. Your job is to analyze the user's request 
                and assign it to the most suitable specialized AI agent. You should only allocate ONE agent per task.
                
                If multiple agents seem necessary for a task, ask the user if they want to proceed with 
                breaking it down or if they prefer to provide a more specific prompt.
                
                If no suitable agent exists for the task, suggest creating a new agent type.
                
                Available specialist agents and their capabilities:
                - Web Scraper: Extract information from websites and web pages
                - Business Environment Analyst: Analyze business landscapes and environments
                - Market Research Analyst: Conduct market research and competitive analysis
                - Data Analyst: Process and analyze datasets and data
                - Content Writer: Create written content like articles, blogs, copy
                - Social Media Manager: Develop social media strategies and content
                - Social Media Video Creator: Create video content for social platforms
                - Graphic Designer: Design graphics, logos, and visual materials
                - Video Editor: Edit and produce video content
                - PDF Producer: Create and format PDF documents
                - PowerPoint Producer: Create PowerPoint presentations
                - Pitch Deck Producer: Create business pitch decks and investor presentations
                
                Respond with ONLY the name of the chosen agent, or ask for clarification if needed.""",
                handoffs=list(self.specialized_agents.values())
            )
            
            print("AI Workforce Manager initialized with OpenAI Agents SDK.")
            print("Available agent types:")
            for agent_name in self.specialized_agents.keys():
                print(f"- {agent_name}")
            
            # Show vector database stats
            stats = self.history_manager.get_collection_stats()
            print(f"\n📊 Vector Database Stats:")
            print(f"- Total conversations stored: {stats['total_conversations']}")
            print(f"- Database path: {stats['database_path']}")
            print(f"- Collection name: {stats['collection_name']}")
            print(f"- Embedding dimension: {stats['embedding_dimension']}")
            
            print("\n--- Enter 'quit' to exit ---")
            print("--- Enter 'search <query>' to search similar conversations ---")
            print("--- Enter 'history' to view recent conversations ---\n")
            
        except Exception as e:
            print(f"❌ Failed to initialize AI Workforce Manager: {e}")
            print("Please ensure sentence-transformers and scikit-learn are properly installed.")
            raise

    async def decide_agent(self, user_prompt):
        """
        Uses the triage agent to decide which specialist agent should handle the task
        """
        try:
            # Retrieve complete chat history for better decision making
            print(f"[DEBUG] Retrieving complete chat history for agent selection...")
            chat_history = self.history_manager.get_recent_history(limit=1000)  # Get last 20 conversations for decision making
            
            # Format chat history for decision making
            decision_context = ""
            if chat_history:
                decision_context = "\n\nCOMPLETE CHAT HISTORY FOR REFERENCE:\n"
                decision_context += f"Here are the last {len(chat_history)} conversations to help you make consistent decisions:\n\n"
                
                for i, conv in enumerate(chat_history, 1):
                    timestamp = conv.get('timestamp', 'Unknown')[:19]
                    chosen_agent = conv.get('chosen_agent', 'Unknown')
                    user_request = conv.get('user_prompt', '')[:150]
                    
                    decision_context += f"{i}. [{timestamp}] \"{user_request}{'...' if len(conv.get('user_prompt', '')) > 150 else ''}\"\n"
                    decision_context += f"   → Agent chosen: {chosen_agent}\n\n"
                
                decision_context += "Consider this complete history when making your current choice. Look for patterns, maintain consistency with similar past requests, but adapt based on the specific requirements of the new request."
            
            decision_prompt = f"""Analyze this user request and determine which single specialist agent 
            should handle it: '{user_prompt}'
            
            Respond with ONLY the exact name of the chosen agent from the available list, 
            or if multiple agents are needed, state that clearly and ask for user confirmation.{decision_context}"""
            
            print(f"[DEBUG] Sending decision request to AI Workforce Manager with complete history...")
            
            result = await Runner.run(self.triage_agent, decision_prompt)
            chosen_agent_response = result.final_output.strip()
            
            print(f"[DEBUG] AI Workforce Manager decided: {chosen_agent_response}")
            return chosen_agent_response
            
        except Exception as e:
            print(f"Error in agent decision: {e}")
            return f"Error: Could not decide agent - {str(e)}"

    def format_historical_context(self, chat_history: list, agent_name: str) -> str:
        """
        Format the entire chat history for injection into agent prompts.
        
        Args:
            chat_history: List of all past conversations
            agent_name: Name of the current agent being called
            
        Returns:
            Formatted context string for the agent
        """
        if not chat_history:
            return "No chat history available."
        
        context_parts = []
        context_parts.append("=== COMPLETE CHAT HISTORY ===")
        context_parts.append(f"The following is the complete chat history ({len(chat_history)} conversations) for your reference:")
        context_parts.append("Use this history to maintain consistency, learn from past interactions, and build upon previous work.")
        context_parts.append("")
        
        # Sort by timestamp (most recent first)
        sorted_history = sorted(chat_history, key=lambda x: x.get('timestamp', ''), reverse=True)
        
        for i, conv in enumerate(sorted_history, 1):
            timestamp = conv.get('timestamp', 'Unknown')[:19]
            chosen_agent = conv.get('chosen_agent', 'Unknown')
            user_prompt = conv.get('user_prompt', '')
            manager_response = conv.get('manager_response', '')
            
            # Limit length for very long conversations to avoid token limits
            user_prompt_display = user_prompt[:300] + "..." if len(user_prompt) > 300 else user_prompt
            manager_response_display = manager_response[:400] + "..." if len(manager_response) > 400 else manager_response
            
            context_parts.append(f"--- Conversation {i} ---")
            context_parts.append(f"Date: {timestamp}")
            context_parts.append(f"Agent Used: {chosen_agent}")
            context_parts.append(f"User Request: {user_prompt_display}")
            context_parts.append(f"Response: {manager_response_display}")
            context_parts.append("")
        
        context_parts.append("=== END CHAT HISTORY ===")
        context_parts.append("")
        context_parts.append("Please use this complete chat history to inform your response. Maintain consistency with past approaches, learn from previous successes and challenges, and build upon the established context.")
        context_parts.append("")
        
        return "\n".join(context_parts)

    async def delegate_task(self, agent_name, user_prompt):
        """
        Delegates the task to the chosen specialist agent with complete chat history.
        """
        if agent_name not in self.specialized_agents:
            error_message = f"Agent '{agent_name}' not found in available specialists."
            print(error_message)
            return error_message

        try:
            # Special handling for PDF Producer agent - actually create PDFs
            if agent_name == "PDF Producer":
                print(f"[DEBUG] PDF Producer agent activated - creating actual PDF file...")
                
                # Create the actual PDF using the PDF tools
                pdf_result = create_pdf_document(user_prompt)
                
                # Retrieve chat history for context
                chat_history = self.history_manager.get_recent_history(limit=10)
                
                # Add context about previous PDFs if any
                pdf_context = ""
                if chat_history:
                    pdf_conversations = [conv for conv in chat_history if conv.get('chosen_agent') == 'PDF Producer']
                    if pdf_conversations:
                        pdf_context = f"\n\n📚 Previous PDF Creation History:\n"
                        for i, conv in enumerate(pdf_conversations[:3], 1):
                            timestamp = conv.get('timestamp', 'Unknown')[:19]
                            request = conv.get('user_prompt', '')[:100]
                            pdf_context += f"{i}. [{timestamp}] {request}{'...' if len(conv.get('user_prompt', '')) > 100 else ''}\n"
                
                # Combine the PDF creation result with context
                final_response = f"{pdf_result}{pdf_context}"
                
                print(f"[DEBUG] PDF Producer completed - file created and saved to root directory.")
                return final_response
            
            # Regular handling for other agents
            # Retrieve the entire chat history from vector database
            print(f"[DEBUG] Retrieving complete chat history for {agent_name}...")
            chat_history = self.history_manager.get_recent_history(limit=50)  # Get last 50 conversations
            
            # Format the complete chat history
            historical_context = self.format_historical_context(chat_history, agent_name)
            
            # Create enhanced prompt with complete chat history
            enhanced_prompt = f"""{historical_context}

=== CURRENT REQUEST ===
{user_prompt}

Please respond to the current request above, taking into account the complete chat history provided. Maintain consistency with past approaches, learn from previous interactions, and build upon the established context and relationships."""

            specialist_agent = self.specialized_agents[agent_name]
            print(f"[DEBUG] Delegating task to {agent_name} with complete chat history...")
            
            # Log the context retrieval
            if chat_history:
                print(f"[DEBUG] Providing {len(chat_history)} conversations from vector database")
                # Show breakdown by agent
                agent_counts = {}
                for conv in chat_history:
                    agent = conv.get('chosen_agent', 'Unknown')
                    agent_counts[agent] = agent_counts.get(agent, 0) + 1
                print(f"[DEBUG] History breakdown by agent: {agent_counts}")
            else:
                print(f"[DEBUG] No chat history available in vector database")
            
            result = await Runner.run(specialist_agent, enhanced_prompt)
            agent_response = result.final_output
            
            print(f"[DEBUG] {agent_name} completed the task with complete chat history context from vector database.")
            return agent_response
            
        except Exception as e:
            error_message = f"Error: Agent {agent_name} failed to process the task - {str(e)}"
            print(error_message)
            return error_message

    async def handle_prompt(self, user_prompt):
        manager_response = ""
        chosen_agent_log = None
        agent_suggestion_log = None

        try:
            # 1. Decide which agent should handle the task
            decision_response = await self.decide_agent(user_prompt)

            # Check if the response indicates multiple agents are needed
            if "multiple agents" in decision_response.lower() or "ask" in decision_response.lower():
                manager_response = f"{decision_response} Do you want to proceed by breaking this down, or should I stop and ask for another prompt? (yes/no)"
                print(f"AI Workforce Manager: {manager_response}")
                
                user_confirmation = input("> User: ").strip().lower()
                self.history_manager.add_entry(user_prompt, manager_response + f" User replied: {user_confirmation}", chosen_agent_log, agent_suggestion_log)
                
                if user_confirmation != 'yes':
                    final_manager_response = "Okay, I will stop. Please provide another prompt."
                    print(f"AI Workforce Manager: {final_manager_response}")
                    self.history_manager.add_entry(user_prompt, final_manager_response, chosen_agent_log, agent_suggestion_log)
                    return
                else:
                    # Ask user to specify which single agent they want to use
                    print("AI Workforce Manager: Please specify which single agent you'd like me to use for this task.")
                    return

            # Check if no suitable agent was found
            elif "no suitable agent" in decision_response.lower() or "suggest creating" in decision_response.lower():
                manager_response = f"{decision_response} Would you like to suggest how this new agent should work, or provide a different prompt?"
                print(f"AI Workforce Manager: {manager_response}")
                agent_suggestion_log = decision_response
                self.history_manager.add_entry(user_prompt, manager_response, chosen_agent_log, agent_suggestion_log)
                return

            # Check if a valid agent was chosen
            elif decision_response in self.specialized_agents:
                chosen_agent = decision_response
                chosen_agent_log = chosen_agent
                
                print(f"AI Workforce Manager: Allocating task '{user_prompt}' to agent: {chosen_agent}")
                agent_response = await self.delegate_task(chosen_agent, user_prompt)
                manager_response = f"Task allocated to {chosen_agent}. Agent response:\n{agent_response}"
                print(f"\n{chosen_agent}: {agent_response}")
                
            else:
                # Handle unexpected responses
                manager_response = f"I received an unexpected decision: '{decision_response}'. Could you please rephrase your request or specify an agent?"
                print(f"AI Workforce Manager: {manager_response}")

            # Log the interaction to vector database
            self.history_manager.add_entry(user_prompt, manager_response, chosen_agent_log, agent_suggestion_log)
            
        except Exception as e:
            error_message = f"Error handling prompt: {str(e)}"
            print(f"❌ {error_message}")
            # Still try to log the error
            try:
                self.history_manager.add_entry(user_prompt, error_message, None, None)
            except:
                print("❌ Failed to log error to vector database")

    async def run(self):
        while True:
            try:
                user_input = input("\nUser Prompt: ").strip()
                if user_input.lower() == 'quit':
                    print("Exiting AI Workforce Manager.")
                    break
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower().startswith('search '):
                    query = user_input[7:]  # Remove 'search ' prefix
                    if query:
                        print(f"🔍 Searching vector database for similar conversations: '{query}'")
                        similar = self.history_manager.search_similar_conversations(query, n_results=5)
                        if similar:
                            print(f"Found {len(similar)} similar conversations:")
                            for i, conv in enumerate(similar, 1):
                                print(f"\n{i}. Similarity: {conv['similarity_score']:.3f}")
                                print(f"   User: {conv['user_prompt'][:80]}...")
                                print(f"   Agent: {conv['metadata']['chosen_agent']}")
                                print(f"   Time: {conv['metadata']['timestamp'][:19]}")
                        else:
                            print("No similar conversations found in vector database.")
                    else:
                        print("Please provide a search query. Example: search web scraping")
                    continue
                
                elif user_input.lower() == 'history':
                    print("📚 Recent conversation history from vector database:")
                    recent = self.history_manager.get_recent_history(limit=10)
                    if recent:
                        for i, entry in enumerate(recent, 1):
                            print(f"\n{i}. {entry['timestamp'][:19]}")
                            print(f"   User: {entry['user_prompt'][:60]}...")
                            print(f"   Agent: {entry['chosen_agent']}")
                    else:
                        print("No conversation history found in vector database.")
                    continue
                
                # Handle regular prompts
                await self.handle_prompt(user_input)
                print("----")
                
            except KeyboardInterrupt:
                print("\n\nExiting AI Workforce Manager.")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("Continuing...")

async def main():
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("Please create a .env file in the project root with:")
        print("OPENAI_API_KEY=your_api_key_here")
        print("\nOr set it as an environment variable:")
        print("export OPENAI_API_KEY='your_api_key_here'")
        return
    
    print("✅ OpenAI API key loaded successfully!")
    print("🗄️ Initializing vector database for chat history...")
    
    try:
        manager = AIWorkforceManager()
        print("✅ AI Workforce Manager is ready to use with vector database.\n")
        await manager.run()
    except Exception as e:
        print(f"❌ Failed to start AI Workforce Manager: {e}")
        print("Please check your vector database installation and configuration.")

if __name__ == "__main__":
    asyncio.run(main()) 