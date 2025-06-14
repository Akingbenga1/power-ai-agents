import os
import asyncio
import gradio as gr
from datetime import datetime
from dotenv import load_dotenv
from main import AIWorkforceManager

# Load environment variables
load_dotenv()

class GradioAIWorkforceManager:
    def __init__(self):
        self.manager = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the AI Workforce Manager"""
        if not self.is_initialized:
            try:
                self.manager = AIWorkforceManager()
                self.is_initialized = True
                return "✅ AI Workforce Manager initialized successfully!"
            except Exception as e:
                return f"❌ Failed to initialize: {str(e)}"
        return "✅ AI Workforce Manager already initialized!"
    
    async def process_request(self, user_input, history):
        """Process user request and return response"""
        if not self.is_initialized:
            await self.initialize()
        
        if not user_input.strip():
            return history, ""
        
        # Add user message to history
        history.append([user_input, None])
        
        try:
            # Get agent decision
            decision_response = await self.manager.decide_agent(user_input)
            
            # Check if multiple agents are needed
            if "multiple agents" in decision_response.lower() or "ask" in decision_response.lower():
                bot_response = f"🤔 {decision_response}\n\nPlease provide a more specific request or choose a single agent."
                
            # Check if no suitable agent found
            elif "no suitable agent" in decision_response.lower() or "suggest creating" in decision_response.lower():
                bot_response = f"💡 {decision_response}"
                
            # Valid agent chosen
            elif decision_response in self.manager.specialized_agents:
                chosen_agent = decision_response
                bot_response = f"🔄 **Assigning to {chosen_agent}...**\n\n"
                
                # Get agent response
                agent_response = await self.manager.delegate_task(chosen_agent, user_input)
                bot_response += f"**{chosen_agent} Response:**\n{agent_response}"
                
                # Log the interaction
                manager_response = f"Task allocated to {chosen_agent}. Agent response:\n{agent_response}"
                self.manager.history_manager.add_entry(user_input, manager_response, chosen_agent, None)
                
            else:
                bot_response = f"❓ Unexpected response: {decision_response}\nPlease try rephrasing your request."
                
            # Update history with bot response
            history[-1][1] = bot_response
            
        except Exception as e:
            error_response = f"❌ Error processing request: {str(e)}"
            history[-1][1] = error_response
            
        return history, ""
    
    async def search_history(self, query):
        """Search chat history"""
        if not self.is_initialized:
            await self.initialize()
            
        if not query.strip():
            return "Please enter a search query."
            
        try:
            similar = self.manager.history_manager.search_similar_conversations(query, n_results=5)
            if similar:
                result = f"🔍 **Found {len(similar)} similar conversations:**\n\n"
                for i, conv in enumerate(similar, 1):
                    result += f"**{i}. Similarity: {conv['similarity_score']:.3f}**\n"
                    result += f"👤 User: {conv['user_prompt'][:100]}...\n"
                    result += f"🤖 Agent: {conv['metadata']['chosen_agent']}\n"
                    result += f"📅 Time: {conv['metadata']['timestamp'][:19]}\n\n"
                return result
            else:
                return "No similar conversations found."
        except Exception as e:
            return f"❌ Error searching history: {str(e)}"
    
    async def get_recent_history(self):
        """Get recent conversation history"""
        if not self.is_initialized:
            await self.initialize()
            
        try:
            recent = self.manager.history_manager.get_recent_history(limit=10)
            if recent:
                result = "📚 **Recent Conversations:**\n\n"
                for i, entry in enumerate(recent, 1):
                    result += f"**{i}. {entry['timestamp'][:19]}**\n"
                    result += f"👤 User: {entry['user_prompt'][:80]}...\n"
                    result += f"🤖 Agent: {entry['chosen_agent']}\n\n"
                return result
            else:
                return "No conversation history found."
        except Exception as e:
            return f"❌ Error retrieving history: {str(e)}"
    
    def get_agent_info(self):
        """Get information about available agents"""
        if not self.is_initialized:
            return "Please initialize the system first."
            
        info = "🤖 **Available AI Agents:**\n\n"
        
        agent_descriptions = {
            "Web Scraper": "🕷️ Extract information from websites and web pages",
            "Business Environment Analyst": "📊 Analyze business landscapes and environments", 
            "Market Research Analyst": "📈 Conduct market research and competitive analysis",
            "Data Analyst": "📉 Process and analyze datasets and data",
            "Content Writer": "✍️ Create written content like articles, blogs, copy",
            "Social Media Manager": "📱 Develop social media strategies and content",
            "Social Media Video Creator": "🎬 Create video content for social platforms",
            "Graphic Designer": "🎨 Design graphics, logos, and visual materials",
            "Video Editor": "🎞️ Edit and produce video content",
            "PDF Producer": "📄 Create and format PDF documents",
            "PowerPoint Producer": "📊 Create PowerPoint presentations",
            "Pitch Deck Producer": "💼 Create business pitch decks and investor presentations"
        }
        
        for agent, description in agent_descriptions.items():
            info += f"**{agent}**: {description}\n\n"
            
        return info

# Initialize the global manager
gradio_manager = GradioAIWorkforceManager()

# Async wrapper functions for Gradio
async def chat_interface(message, history):
    """Main chat interface"""
    return await gradio_manager.process_request(message, history)

async def search_interface(query):
    """Search interface"""
    return await gradio_manager.search_history(query)

async def history_interface():
    """History interface"""
    return await gradio_manager.get_recent_history()

def agent_info_interface():
    """Agent info interface"""
    return gradio_manager.get_agent_info()

# Create the Gradio interface
def create_gradio_app():
    """Create and configure the Gradio application"""
    
    # Custom CSS for better styling
    css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    .chat-container {
        height: 600px !important;
    }
    """
    
    with gr.Blocks(css=css, title="AI Workforce Manager", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🤖 AI Workforce Manager")
        gr.Markdown("### Intelligent task delegation to specialized AI agents")
        
        with gr.Tabs():
            # Main Chat Tab
            with gr.TabItem("💬 Chat with AI Agents"):
                chatbot = gr.Chatbot(
                    height=500,
                    label="AI Workforce Manager",
                    elem_classes=["chat-container"]
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Enter your request (e.g., 'Create a PDF report about market trends')",
                        label="Your Request",
                        scale=4
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                
                # Initialize the system on startup
                gr.Markdown("### 🔄 System Status")
                status_output = gr.Textbox(
                    label="Initialization Status",
                    interactive=False,
                    lines=2
                )
                
                # Initialize button
                init_btn = gr.Button("Initialize AI Workforce Manager", variant="secondary")
                
                # Event handlers
                msg.submit(chat_interface, [msg, chatbot], [chatbot, msg])
                submit_btn.click(chat_interface, [msg, chatbot], [chatbot, msg])
                init_btn.click(gradio_manager.initialize, outputs=status_output)
                
            # Search Tab
            with gr.TabItem("🔍 Search History"):
                gr.Markdown("### Search previous conversations")
                
                with gr.Row():
                    search_input = gr.Textbox(
                        placeholder="Enter search query (e.g., 'web scraping', 'PDF creation')",
                        label="Search Query",
                        scale=4
                    )
                    search_btn = gr.Button("Search", variant="primary", scale=1)
                
                search_output = gr.Markdown(
                    label="Search Results",
                    height=400
                )
                
                search_btn.click(search_interface, search_input, search_output)
                search_input.submit(search_interface, search_input, search_output)
                
            # History Tab
            with gr.TabItem("📚 Recent History"):
                gr.Markdown("### View recent conversations")
                
                history_btn = gr.Button("Load Recent History", variant="primary")
                history_output = gr.Markdown(
                    label="Recent Conversations",
                    height=500
                )
                
                history_btn.click(history_interface, outputs=history_output)
                
            # Agents Info Tab
            with gr.TabItem("🤖 Available Agents"):
                gr.Markdown("### Learn about available AI agents")
                
                agents_btn = gr.Button("Show Agent Information", variant="primary")
                agents_output = gr.Markdown(
                    label="Agent Information",
                    height=500
                )
                
                agents_btn.click(agent_info_interface, outputs=agents_output)
                
        # Footer
        gr.Markdown("---")
        gr.Markdown("**💡 Tips:**")
        gr.Markdown("- Be specific about what you want to accomplish")
        gr.Markdown("- The system will automatically choose the best agent for your task")
        gr.Markdown("- Use the search feature to find similar past conversations")
        gr.Markdown("- Check the agents tab to see what each specialist can do")
        
    return demo

# Main function to run the Gradio app
def main():
    """Main function to run the Gradio interface"""
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("Please create a .env file in the project root with:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    print("✅ OpenAI API key loaded successfully!")
    print("OpenAI API key: ", api_key)
    print("🚀 Starting Gradio AI Workforce Manager...")
    print("🌐 The web interface will open in your browser automatically")
    
    # Create and launch the Gradio app
    demo = create_gradio_app()
    
    # Launch with public sharing disabled by default for security
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Default Gradio port
        share=False,           # Set to True if you want a public URL
        show_api=False,        # Hide API docs
        show_error=True,       # Show errors in the interface
        debug=False            # Set to True for debugging
    )

if __name__ == "__main__":
    main() 