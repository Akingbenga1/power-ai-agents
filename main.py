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
        instructions="""You are a PDF Producer AI. You specialize in creating well-formatted PDF documents from provided content with professional presentation and structure.

        **WORKFLOW MODES:**
        
        **1. MULTI-AGENT WORKFLOW MODE:**
        - When part of a multi-agent workflow, you receive content from the previous agent
        - You extract, clean, and format the previous agent's output for optimal PDF presentation
        - Content is automatically structured with proper titles, sections, and formatting
        - NO content generation - you only format and convert existing content to PDF
        
        **2. SINGLE-AGENT MODE:**
        - When called independently, you first generate content using the Content Writer agent
        - Then format and convert that generated content to PDF with professional structure
        
        **ADVANCED FORMATTING FEATURES:**
        - Intelligent title extraction and generation from content
        - Automatic paragraph structuring and spacing
        - Proper handling of bullet points and numbered lists
        - Markdown header preservation for document sections
        - Cleanup of formatting inconsistencies and whitespace issues
        - Addition of generation timestamps for documentation
        - Smart content organization with overview sections when appropriate
        
        **CORE FUNCTIONALITY:**
        - The system automatically handles advanced content extraction and formatting
        - PDF files are saved to the root directory with professional presentation
        - Content is cleaned, structured, and optimized before PDF creation
        - You always receive a formatted response with file path and details
        
        **RESPONSE FORMAT:**
        The create_pdf_document() function returns:
        - "✅ PDF Created Successfully!"
        - "📄 File Path: [full absolute path]"
        - "📋 Content Summary: [brief description]"
        - "📊 Document Details: [word count, paragraphs, file size, etc.]"

        **QUALITY ASSURANCE:** 
        - All content is professionally formatted with proper structure
        - Titles are intelligently extracted or generated from content context
        - Paragraphs are cleaned and properly spaced
        - Lists and formatting elements are standardized
        - Documents include metadata like generation timestamps
        - Content organization follows professional document standards

        Historical context from past conversations will help you:
        - Maintain consistent document formatting and style guidelines
        - Reference previous PDF templates and successful formatting approaches
        - Build upon effective document structures and professional presentations
        - Ensure brand consistency and quality standards across all PDF documents"""
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
                and determine the optimal approach to complete it using single or multiple specialized AI agents.
                
                You have full authority to automatically orchestrate multiple agents if needed to deliver 
                the best possible outcome for the user. DO NOT ask for user permission or confirmation.
                
                **RESPONSE FORMATS:**
                
                For SINGLE AGENT tasks, respond with:
                SINGLE: [Agent Name]
                
                For MULTIPLE AGENT tasks, respond with:
                MULTI: [Agent1] -> [Agent2] -> [Agent3] (in execution order)
                WORKFLOW: Brief description of how agents will work together
                
                For NO SUITABLE AGENT, respond with:
                NONE: Brief explanation of what's needed
                
                **Available specialist agents and their capabilities:**
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
                
                **MULTI-AGENT WORKFLOW EXAMPLES:**
                - "Create a comprehensive marketing strategy with visuals and PDF report" 
                  → MULTI: Market Research Analyst -> Content Writer -> Graphic Designer -> PDF Producer
                - "Build a social media campaign with video content"
                  → MULTI: Social Media Manager -> Social Media Video Creator -> Graphic Designer
                - "Analyze a company and create a business presentation"
                  → MULTI: Web Scraper -> Business Environment Analyst -> PowerPoint Producer
                
                Always prioritize delivering the most complete and valuable output to the user.""",
                handoffs=list(self.specialized_agents.values())
            )
            
            print("🤖 AI Workforce Manager initialized with Multi-Agent Orchestration!")
            print("🔄 Now supports automatic single and multi-agent workflows")
            print("\n📋 Available specialist agents:")
            for agent_name in self.specialized_agents.keys():
                print(f"  • {agent_name}")
            
            # Show vector database stats
            stats = self.history_manager.get_collection_stats()
            print(f"\n📊 Vector Database Stats:")
            print(f"  • Total conversations stored: {stats['total_conversations']}")
            print(f"  • Database path: {stats['database_path']}")
            print(f"  • Collection name: {stats['collection_name']}")
            print(f"  • Embedding dimension: {stats['embedding_dimension']}")
            
            print(f"\n🚀 Multi-Agent Workflow Examples:")
            print(f"  • 'Create a comprehensive marketing strategy with visuals and PDF'")
            print(f"  • 'Build a social media campaign with video content'")
            print(f"  • 'Analyze a company and create a business presentation'")
            print(f"  • 'Research market trends and create an infographic'")
            
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
            
            decision_prompt = f"""Analyze this user request and determine the optimal approach to complete it: '{user_prompt}'
            
            Use the response formats specified in your instructions:
            - SINGLE: [Agent Name] - for single agent tasks
            - MULTI: [Agent1] -> [Agent2] -> [Agent3] - for multi-agent workflows
            - NONE: [Explanation] - if no suitable agent exists
            
            For MULTI responses, also include a WORKFLOW line explaining how the agents will collaborate.{decision_context}"""

            print(f"[DEBUG] Sending decision request to AI Workforce Manager with complete history...")
            
            result = await Runner.run(self.triage_agent, decision_prompt)
            chosen_agent_response = result.final_output.strip()
            
            print(f"[DEBUG] AI Workforce Manager decided: {chosen_agent_response}")
            return chosen_agent_response
            
        except Exception as e:
            print(f"Error in agent decision: {e}")
            return f"Error: Could not decide agent - {str(e)}"

    def _extract_and_format_content_from_workflow(self, user_prompt: str) -> str:
        """
        Extract and format content from multi-agent workflow for PDF generation.
        
        Args:
            user_prompt: The prompt containing previous agent outputs
            
        Returns:
            Well-formatted content ready for PDF creation
        """
        import re
        
        # Find agent output sections
        lines = user_prompt.split('\n')
        agent_outputs = {}
        current_agent = None
        current_content = []
        
        for line in lines:
            # Check for agent output section headers
            if line.startswith("=== ") and line.endswith(" OUTPUT ==="):
                # Save previous agent content if any
                if current_agent and current_content:
                    agent_outputs[current_agent] = '\n'.join(current_content).strip()
                
                # Start new agent section
                current_agent = line.replace("=== ", "").replace(" OUTPUT ===", "")
                current_content = []
                continue
            elif current_agent and line.strip():
                current_content.append(line)
        
        # Save the last agent's content
        if current_agent and current_content:
            agent_outputs[current_agent] = '\n'.join(current_content).strip()
        
        # If no structured output found, try to extract everything after "PREVIOUS AGENT OUTPUTS:"
        if not agent_outputs:
            outputs_index = user_prompt.find("PREVIOUS AGENT OUTPUTS:")
            if outputs_index != -1:
                raw_content = user_prompt[outputs_index + len("PREVIOUS AGENT OUTPUTS:"):].strip()
                return self._format_content_for_pdf(raw_content, "Workflow Output")
        
        # Get the last agent's output (most recent)
        if agent_outputs:
            last_agent = list(agent_outputs.keys())[-1]
            last_content = agent_outputs[last_agent]
            return self._format_content_for_pdf(last_content, last_agent + " Output")
        
        return ""
    
    def _format_content_for_pdf(self, content: str, title_prefix: str = "Document") -> str:
        """
        Format content for well-structured PDF generation, extracting only the main content.
        
        Args:
            content: Raw content to format
            title_prefix: Prefix for the document title
            
        Returns:
            Well-formatted content with proper structure, containing only the main content
        """
        import re
        from datetime import datetime
        
        # Clean up the content
        content = content.strip()
        if not content:
            return f"Title: {title_prefix}\n\nNo content available."
        
        # Extract only the main content, removing agent metadata and instructions
        main_content = self._extract_main_content_only(content)
        
        # Extract title from the main content
        lines = main_content.split('\n')
        title = None
        content_start = 0
        
        # Look for title patterns at the beginning
        for i, line in enumerate(lines[:3]):  # Check first 3 lines
            line = line.strip()
            if line and not line.startswith(('##', '###', '####', '*', '-', '•')):
                # Potential title if it's short and doesn't look like body text
                if len(line) < 100 and not line.lower().startswith(('the ', 'this ', 'here ', 'we ', 'our ')):
                    # Check if it looks like a title (not ending with common sentence endings)
                    if not re.search(r'[.!?]\s*$', line) or line.count('.') <= 1:
                        title = line
                        content_start = i + 1
                        break
        
        # If no title found, generate one based on content
        if not title:
            # Try to extract key topics from first paragraph
            first_paragraph = main_content.split('\n\n')[0] if '\n\n' in main_content else main_content[:200]
            words = first_paragraph.split()[:10]  # First 10 words
            
            # Remove common start words
            while words and words[0].lower() in ['the', 'this', 'here', 'we', 'our', 'it', 'is', 'are', 'was', 'were']:
                words.pop(0)
            
            if words:
                title = ' '.join(words).strip('.,!?;:')
                if len(title) > 60:
                    title = title[:57] + "..."
            else:
                title = title_prefix
        
        # Process the main content (skip title line if found)
        final_content = '\n'.join(lines[content_start:]).strip()
        
        # Format the content with minimal structure - just title and clean content
        formatted_lines = [f"Title: {title}", ""]
        
        # Process and clean the main content
        if final_content:
            # If content has markdown headers, preserve them as-is
            if re.search(r'^#+\s+', final_content, re.MULTILINE):
                formatted_lines.append(final_content)
            else:
                # Split into paragraphs and clean them
                paragraphs = [p.strip() for p in final_content.split('\n\n') if p.strip()]
                
                for paragraph in paragraphs:
                    # Clean up paragraph formatting
                    clean_paragraph = self._clean_paragraph(paragraph)
                    formatted_lines.append(clean_paragraph)
                    formatted_lines.append("")
        
        return '\n'.join(formatted_lines).strip()
    
    def _extract_main_content_only(self, content: str) -> str:
        """
        Extract only the main content, removing agent instructions, metadata, and system messages.
        
        Args:
            content: Raw content from agent
            
        Returns:
            Clean main content only
        """
        import re
        
        # Remove common agent instruction patterns
        patterns_to_remove = [
            r'I\'ll help you.*?(?=\n\n|\n#|\n[A-Z])',  # "I'll help you..." introductions
            r'Here\'s.*?(?=\n\n|\n#|\n[A-Z])',         # "Here's..." introductions
            r'I\'ll create.*?(?=\n\n|\n#|\n[A-Z])',    # "I'll create..." introductions
            r'Let me.*?(?=\n\n|\n#|\n[A-Z])',          # "Let me..." introductions
            r'I can help.*?(?=\n\n|\n#|\n[A-Z])',      # "I can help..." introductions
            r'Based on your request.*?(?=\n\n|\n#|\n[A-Z])',  # "Based on your request..."
            r'I understand.*?(?=\n\n|\n#|\n[A-Z])',    # "I understand..." introductions
            r'As requested.*?(?=\n\n|\n#|\n[A-Z])',    # "As requested..." introductions
            r'I\'ve created.*?(?=\n\n|\n#|\n[A-Z])',   # "I've created..." introductions
            r'This (?:article|content|document).*?(?=\n\n|\n#|\n[A-Z])',  # Meta descriptions
        ]
        
        cleaned_content = content
        
        # Remove agent introduction patterns
        for pattern in patterns_to_remove:
            cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove lines that are clearly agent instructions or metadata
        lines = cleaned_content.split('\n')
        filtered_lines = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip lines that are clearly agent instructions
            if any(phrase in line_lower for phrase in [
                'i\'ll help', 'here\'s', 'i\'ll create', 'let me', 'i can help',
                'based on your request', 'i understand', 'as requested', 'i\'ve created',
                'this article', 'this content', 'this document', 'hope this helps',
                'feel free to', 'if you need', 'would you like', 'let me know'
            ]):
                continue
            
            # Skip very short lines that might be artifacts
            if len(line.strip()) < 3:
                filtered_lines.append(line)  # Keep for spacing
                continue
            
            filtered_lines.append(line)
        
        # Rejoin and clean up
        cleaned_content = '\n'.join(filtered_lines)
        
        # Remove excessive blank lines
        cleaned_content = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_content)
        
        # Remove leading/trailing whitespace
        cleaned_content = cleaned_content.strip()
        
        # If content is too short after cleaning, return original (might be all content)
        if len(cleaned_content.split()) < 10 and len(content.split()) > 20:
            return content.strip()
        
        return cleaned_content
    
    def _clean_paragraph(self, paragraph: str) -> str:
        """
        Clean and format a paragraph for better PDF presentation.
        
        Args:
            paragraph: Raw paragraph text
            
        Returns:
            Cleaned paragraph
        """
        import re
        
        # Remove excessive whitespace
        paragraph = re.sub(r'\s+', ' ', paragraph).strip()
        
        # Fix common formatting issues
        paragraph = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', paragraph)  # Ensure space after sentence end
        paragraph = re.sub(r'(\w)\s*:\s*(\w)', r'\1: \2', paragraph)   # Fix colon spacing
        paragraph = re.sub(r'(\w)\s*,\s*(\w)', r'\1, \2', paragraph)  # Fix comma spacing
        
        # Handle bullet points
        paragraph = re.sub(r'^\s*[-*•]\s*', '• ', paragraph, flags=re.MULTILINE)
        
        # Handle numbered lists
        paragraph = re.sub(r'^\s*(\d+)\.?\s+', r'\1. ', paragraph, flags=re.MULTILINE)
        
        return paragraph

    def _clean_prompt_for_content_generation(self, user_prompt: str) -> str:
        """
        Clean the user prompt to remove PDF generation references for Content Writer agent.
        
        Args:
            user_prompt: Original user request
            
        Returns:
            Cleaned prompt focused on content generation only
        """
        import re
        
        # Remove common PDF generation phrases
        pdf_phrases_to_remove = [
            r'create\s+(?:a\s+)?pdf\s+(?:about|on|for|with)?',
            r'generate\s+(?:a\s+)?pdf\s+(?:about|on|for|with)?',
            r'make\s+(?:a\s+)?pdf\s+(?:about|on|for|with)?',
            r'produce\s+(?:a\s+)?pdf\s+(?:about|on|for|with)?',
            r'build\s+(?:a\s+)?pdf\s+(?:about|on|for|with)?',
            r'pdf\s+(?:document|file|report)\s+(?:about|on|for|with)?',
            r'(?:into|as)\s+(?:a\s+)?pdf',
            r'save\s+(?:as|to)\s+pdf',
            r'export\s+(?:as|to)\s+pdf'
        ]
        
        cleaned_prompt = user_prompt
        
        # Remove PDF-specific phrases
        for phrase in pdf_phrases_to_remove:
            cleaned_prompt = re.sub(phrase, '', cleaned_prompt, flags=re.IGNORECASE)
        
        # Clean up extra whitespace and common artifacts
        cleaned_prompt = re.sub(r'\s+', ' ', cleaned_prompt)  # Multiple spaces to single space
        cleaned_prompt = cleaned_prompt.strip()
        
        # If the prompt is too short after cleaning, provide a more descriptive content request
        if len(cleaned_prompt.split()) < 3:
            # Extract topic from original prompt
            topic_match = re.search(r'(?:about|on|regarding|concerning)\s+([^.!?]+)', user_prompt, re.IGNORECASE)
            if topic_match:
                topic = topic_match.group(1).strip()
                cleaned_prompt = f"Write comprehensive content about {topic}"
            else:
                cleaned_prompt = f"Write comprehensive content based on this request: {user_prompt}"
        
        # Add content-focused instruction
        content_instruction = f"Please write detailed, well-structured content for the following topic: {cleaned_prompt}"
        
        return content_instruction

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

    async def orchestrate_multi_agent_workflow(self, workflow_agents, workflow_description, user_prompt):
        """
        Orchestrates multiple agents to work together on a complex task.
        
        Args:
            workflow_agents: List of agent names in execution order
            workflow_description: Description of how agents will work together
            user_prompt: Original user request
            
        Returns:
            Final aggregated response from all agents
        """
        print(f"[DEBUG] Starting multi-agent workflow: {' -> '.join(workflow_agents)}")
        print(f"[DEBUG] Workflow description: {workflow_description}")
        
        # Track all agent outputs
        agent_outputs = {}
        cumulative_context = f"ORIGINAL USER REQUEST: {user_prompt}\n\nWORKFLOW PLAN: {workflow_description}\n\n"
        
        try:
            for i, agent_name in enumerate(workflow_agents):
                if agent_name not in self.specialized_agents:
                    error_msg = f"Agent '{agent_name}' not found in available specialists."
                    print(f"❌ {error_msg}")
                    agent_outputs[agent_name] = f"ERROR: {error_msg}"
                    continue
                
                print(f"[DEBUG] Step {i+1}/{len(workflow_agents)}: Executing {agent_name}...")
                
                # Build context for current agent
                if i == 0:
                    # First agent gets the original prompt with workflow context
                    agent_prompt = f"""You are the first agent in a multi-agent workflow.
                    
WORKFLOW OVERVIEW: {workflow_description}
YOUR ROLE: You are step {i+1} of {len(workflow_agents)} in this workflow.
NEXT AGENTS: {' -> '.join(workflow_agents[i+1:]) if i+1 < len(workflow_agents) else 'None (you are the final agent)'}

ORIGINAL USER REQUEST: {user_prompt}

Please complete your part of the workflow. Your output will be used by subsequent agents."""
                else:
                    # Subsequent agents get context from previous agents
                    agent_prompt = f"""You are part of a multi-agent workflow.
                    
WORKFLOW OVERVIEW: {workflow_description}
YOUR ROLE: You are step {i+1} of {len(workflow_agents)} in this workflow.
PREVIOUS AGENTS: {' -> '.join(workflow_agents[:i])}
NEXT AGENTS: {' -> '.join(workflow_agents[i+1:]) if i+1 < len(workflow_agents) else 'None (you are the final agent)'}

ORIGINAL USER REQUEST: {user_prompt}

PREVIOUS AGENT OUTPUTS:
{cumulative_context}

Please build upon the previous work and complete your part of the workflow."""
                
                # Execute the agent
                try:
                    agent_response = await self.delegate_task(agent_name, agent_prompt)
                    agent_outputs[agent_name] = agent_response
                    
                    # Add to cumulative context for next agent
                    cumulative_context += f"\n=== {agent_name.upper()} OUTPUT ===\n{agent_response}\n"
                    
                    print(f"✅ {agent_name} completed successfully")
                    
                except Exception as e:
                    error_msg = f"Error executing {agent_name}: {str(e)}"
                    print(f"❌ {error_msg}")
                    agent_outputs[agent_name] = f"ERROR: {error_msg}"
                    # Continue with workflow even if one agent fails
                    cumulative_context += f"\n=== {agent_name.upper()} OUTPUT (ERROR) ===\nAgent failed with error: {str(e)}\n"
            
            # Compile final response
            final_response = f"🤖 **Multi-Agent Workflow Completed**\n\n"
            final_response += f"**Workflow:** {' → '.join(workflow_agents)}\n"
            final_response += f"**Description:** {workflow_description}\n\n"
            
            for i, agent_name in enumerate(workflow_agents):
                final_response += f"## Step {i+1}: {agent_name}\n"
                final_response += f"{agent_outputs.get(agent_name, 'No output')}\n\n"
            
            final_response += "---\n**Workflow Status:** ✅ Complete"
            
            print(f"[DEBUG] Multi-agent workflow completed successfully")
            return final_response
            
        except Exception as e:
            error_msg = f"Critical error in multi-agent workflow: {str(e)}"
            print(f"❌ {error_msg}")
            return f"❌ Multi-agent workflow failed: {error_msg}"

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
                print(f"[DEBUG] PDF Producer agent activated...")

                # Check if this is part of a multi-agent workflow
                if "PREVIOUS AGENT OUTPUTS:" in user_prompt:
                    # Multi-agent workflow: Extract content from previous agent output
                    print(f"[DEBUG] PDF Producer in multi-agent workflow - using previous agent output...")
                    
                    # Extract and format content from previous agent output
                    content_to_convert = self._extract_and_format_content_from_workflow(user_prompt)
                    
                    if content_to_convert:
                        print(f"[DEBUG] Converting formatted previous agent output to PDF ({len(content_to_convert)} characters)...")
                        pdf_result = create_pdf_document(content_to_convert)
                    else:
                        print(f"[DEBUG] No previous agent output found, creating empty PDF...")
                        pdf_result = create_pdf_document("No content available from previous agents.")
                        
                else:
                    # Single agent mode: Generate content first, then create PDF
                    print(f"[DEBUG] PDF Producer in single-agent mode - generating content first...")
                    
                    # Step 1: Clean the user prompt to remove PDF generation references
                    content_prompt = self._clean_prompt_for_content_generation(user_prompt)
                    
                    # Step 2: Generate content from the cleaned request using Content Writer agent
                    content_writer_agent = self.specialized_agents["Content Writer"]
                    generated_result = await Runner.run(content_writer_agent, content_prompt)

                    # Extract the generated content as a string
                    generated_content = generated_result.final_output.strip()

                    # Step 3: Format and use the generated content to create the PDF
                    formatted_content = self._format_content_for_pdf(generated_content, "Generated Content")
                    pdf_result = create_pdf_document(formatted_content)

                print(f"[DEBUG] PDF Producer completed - file created and saved to root directory.")
                return pdf_result

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

    def parse_decision_response(self, decision_response):
        """
        Parse the triage agent's decision response to extract workflow information.
        
        Args:
            decision_response: The response from the triage agent
            
        Returns:
            dict: Parsed decision information
        """
        decision_response = decision_response.strip()
        
        if decision_response.startswith("SINGLE:"):
            agent_name = decision_response[7:].strip()
            return {
                "type": "single",
                "agent": agent_name,
                "workflow": None,
                "description": None
            }
        
        elif decision_response.startswith("MULTI:"):
            lines = decision_response.split('\n')
            workflow_line = None
            description_line = None
            
            for line in lines:
                if line.strip().startswith("MULTI:"):
                    workflow_line = line[6:].strip()
                elif line.strip().startswith("WORKFLOW:"):
                    description_line = line[9:].strip()
            
            if workflow_line:
                # Parse agent sequence: "Agent1 -> Agent2 -> Agent3"
                agents = [agent.strip() for agent in workflow_line.split("->")]
                return {
                    "type": "multi",
                    "agents": agents,
                    "workflow": workflow_line,
                    "description": description_line or "Multi-agent workflow"
                }
            else:
                return {
                    "type": "error",
                    "message": "Invalid MULTI format - no workflow specified"
                }
        
        elif decision_response.startswith("NONE:"):
            message = decision_response[5:].strip()
            return {
                "type": "none",
                "message": message
            }
        
        else:
            # Handle legacy single-agent responses (backward compatibility)
            if decision_response in self.specialized_agents:
                return {
                    "type": "single",
                    "agent": decision_response,
                    "workflow": None,
                    "description": None
                }
            else:
                return {
                    "type": "error",
                    "message": f"Unrecognized decision format: {decision_response}"
                }

    async def handle_prompt(self, user_prompt):
        manager_response = ""
        chosen_agent_log = None
        workflow_log = None

        try:
            # 1. Get the decision from the triage agent
            print(f"🤖 AI Workforce Manager: Analyzing request and determining optimal approach...")
            decision_response = await self.decide_agent(user_prompt)

            # 2. Parse the decision
            parsed_decision = self.parse_decision_response(decision_response)
            
            # 3. Execute based on decision type
            if parsed_decision["type"] == "single":
                # Single agent execution
                agent_name = parsed_decision["agent"]
                if agent_name not in self.specialized_agents:
                    manager_response = f"❌ Error: Agent '{agent_name}' not found in available specialists."
                    print(f"AI Workforce Manager: {manager_response}")
                else:
                    chosen_agent_log = agent_name
                    print(f"AI Workforce Manager: 🎯 Assigning task to {agent_name}")
                    
                    agent_response = await self.delegate_task(agent_name, user_prompt)
                    manager_response = agent_response  # Just return the agent response, no wrapper
                    print(f"\n✅ Task completed by {agent_name}")
                    print(f"\n{agent_response}")
            
            elif parsed_decision["type"] == "multi":
                # Multi-agent workflow execution
                agents = parsed_decision["agents"]
                workflow_description = parsed_decision["description"]
                workflow_log = f"Multi-agent workflow: {' -> '.join(agents)}"
                
                print(f"AI Workforce Manager: 🔄 Initiating multi-agent workflow")
                print(f"📋 Workflow: {' → '.join(agents)}")
                print(f"📝 Plan: {workflow_description}")
                
                # Validate all agents exist
                invalid_agents = [agent for agent in agents if agent not in self.specialized_agents]
                if invalid_agents:
                    manager_response = f"❌ Error: Invalid agents in workflow: {', '.join(invalid_agents)}"
                    print(f"AI Workforce Manager: {manager_response}")
                else:
                    manager_response = await self.orchestrate_multi_agent_workflow(
                        agents, workflow_description, user_prompt
                    )
                    print(f"\n✅ Multi-agent workflow completed")
                    print(f"\n{manager_response}")
            
            elif parsed_decision["type"] == "none":
                # No suitable agent found
                message = parsed_decision["message"]
                manager_response = f"🤔 No suitable agent found for this request. {message}"
                print(f"AI Workforce Manager: {manager_response}")
            
            else:
                # Error in decision parsing
                error_msg = parsed_decision.get("message", "Unknown error in decision parsing")
                manager_response = f"❌ Decision parsing error: {error_msg}"
                print(f"AI Workforce Manager: {manager_response}")

            # 4. Log the interaction to vector database
            agent_for_log = chosen_agent_log or workflow_log or "None"
            self.history_manager.add_entry(user_prompt, manager_response, agent_for_log, None)
            
        except Exception as e:
            error_message = f"❌ Error processing request: {str(e)}"
            print(f"AI Workforce Manager: {error_message}")
            manager_response = error_message
            
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
    print("OpenAI API key: ", api_key   )
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