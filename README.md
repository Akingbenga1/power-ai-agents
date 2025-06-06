# AI Workforce Manager

A dynamic AI Agent Hierarchy system built with the OpenAI Agents SDK that intelligently routes tasks to specialized AI agents and provides each agent with complete conversation history for full context awareness using ChromaDB vector database.

## Features

### 🤖 AI Agent Hierarchy
- **AI Workforce Manager**: Central triage agent that analyzes requests and routes to specialists
- **12 Specialized Agents**: Each with specific expertise and detailed instructions
  - Web Scraper
  - Business Environment Analyst
  - Market Research Analyst
  - Data Analyst
  - Content Writer
  - Social Media Manager
  - Social Media Video Creator
  - Graphic Designer
  - Video Editor
  - PDF Producer
  - PowerPoint Producer
  - Pitch Deck Producer

### 🗄️ ChromaDB Vector Database Integration
- **ChromaDB**: High-performance vector database for storing conversation history with embeddings
- **Complete Context Awareness**: Every agent receives the entire chat history for full context
- **Automatic Embeddings**: Conversations are automatically embedded for semantic search
- **Persistent Storage**: All conversations stored permanently in ChromaDB
- **Continuity**: Agents maintain consistency and build upon previous conversations

### 🔍 Advanced Features
- **Similarity Search**: `search <query>` to find related past conversations using vector similarity
- **History Browsing**: `history` to view recent conversations
- **Database Statistics**: View total conversations and database info
- **Robust Error Handling**: Comprehensive error handling with detailed error messages
- **Context Injection**: All agents receive up to 50 recent conversations for context

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-workforce-manager
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Usage

### Basic Usage
```bash
python main.py
```

### Available Commands
- **Regular prompts**: Just type your request and the system will route it to the appropriate agent
- **Search**: `search web scraping` - Find similar conversations about web scraping using vector similarity
- **History**: `history` - View recent conversation history
- **Quit**: `quit` - Exit the application

### Example Interactions

```
User Prompt: Create a marketing report for my tech startup

AI Workforce Manager: Allocating task to Market Research Analyst...
Market Research Analyst: Based on our previous conversations about startups and market analysis, I'll create a comprehensive marketing report building upon the established framework...
```

```
User Prompt: Now create a social media strategy for the same startup

AI Workforce Manager: Allocating task to Social Media Manager...
Social Media Manager: Building upon the marketing report we just created, I'll develop a social media strategy that aligns with the identified target market and brand positioning...
```

## Architecture

### Agent Flow with Complete History
1. **User Input** → AI Workforce Manager (Triage Agent)
2. **History Retrieval** → System retrieves complete chat history from ChromaDB (last 50 conversations)
3. **Decision Making** → Analyzes request with full context and selects appropriate specialist
4. **Context Injection** → Chosen specialist receives complete chat history from ChromaDB
5. **Task Processing** → Specialist processes with full awareness of past conversations
6. **Response** → Contextually aware response that builds upon previous work
7. **Storage** → New conversation stored in ChromaDB with automatic embeddings

### Complete History Schema
Each agent receives:
```python
{
    "complete_chat_history": [
        {
            "timestamp": "2024-01-15T14:30:25",
            "user_prompt": "Original user request",
            "manager_response": "Complete manager response including agent output",
            "chosen_agent": "Agent Name"
        },
        # ... up to 50 recent conversations
    ]
}
```

## File Structure

```
├── main.py                    # Main application with complete history integration
├── chat_history_manager.py    # ChromaDB vector database integration
├── test_historical_context.py # Test script for complete history functionality
├── test_system.py             # System integration tests
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
└── chroma_db/                # ChromaDB database files (auto-created)
```

## Dependencies

- **openai-agents**: OpenAI Agents SDK for agent orchestration
- **chromadb**: Vector database for semantic search and history storage
- **python-dotenv**: Environment variable management
- **reportlab**: PDF generation capabilities
- **requests**: HTTP requests for web scraping
- **beautifulsoup4**: HTML parsing for web scraping
- **pydantic**: Data validation (specific version for compatibility)
- **numpy**: Numerical computing (specific version for compatibility)

## Configuration

### Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
OPENAI_MODEL=gpt-4
DEBUG=true
```

### Complete History Settings
- **History Limit for Agents**: 50 conversations (configurable in `delegate_task`)
- **History Limit for Decisions**: 20 conversations (configurable in `decide_agent`)
- **Database Path**: `./chroma_db` (auto-created)
- **Collection Name**: `chat_history`
- **Embedding Model**: Default ChromaDB embeddings
- **Persistence**: Automatic persistence to disk with DuckDB backend

## Error Handling

The system includes comprehensive error handling:

1. **API Key Validation**: Checks for OpenAI API key on startup
2. **ChromaDB Initialization**: Validates ChromaDB setup and configuration
3. **Agent Error Recovery**: Graceful handling of agent failures
4. **Network Resilience**: Handles network connectivity issues
5. **Context Overflow Protection**: Limits conversation length to prevent token overflow
6. **Database Error Handling**: Comprehensive error handling for all database operations

## Advanced Usage

### Programmatic Access
```python
from main import AIWorkforceManager

# Initialize with ChromaDB support
manager = AIWorkforceManager()

# Get complete chat history from ChromaDB
history = manager.history_manager.get_recent_history(limit=50)

# Format history for agent context
formatted_context = manager.format_historical_context(history, "Agent Name")

# Search for similar conversations
similar = manager.history_manager.search_similar_conversations("web scraping", n_results=5)
```

### Testing Complete History Integration
```bash
python test_historical_context.py
```

This will test:
- Complete history formatting
- Agent context injection
- Continuity between conversations
- ChromaDB integration

### System Tests
```bash
python test_system.py
```

This will test:
- Environment setup
- ChromaDB functionality
- Agent initialization

## Benefits of Complete History Integration

### 🔄 **Continuity**
- Agents remember all previous interactions
- Consistent responses across sessions
- Building upon previous work

### 🎯 **Context Awareness**
- Full understanding of project evolution
- Awareness of user preferences and patterns
- Consistent brand voice and methodology

### 📈 **Learning**
- Agents learn from past successes and failures
- Improved decision making over time
- Pattern recognition across conversations

### 🤝 **Collaboration**
- Agents can reference work done by other agents
- Seamless handoffs between different specialists
- Unified project understanding

## Troubleshooting

### Common Issues

1. **ChromaDB Installation Issues**
```bash
pip install chromadb==0.3.21
```

2. **OpenAI API Key Not Found**
- Ensure `.env` file exists with `OPENAI_API_KEY=your_key`
- Check that the key starts with `sk-`

3. **ChromaDB Database Permissions**
- Ensure write permissions in the project directory
- ChromaDB will create `./chroma_db/` automatically

4. **Context Too Large**
- System automatically limits conversation length
- Adjust limits in `delegate_task` method if needed

5. **NumPy Compatibility Issues**
```bash
pip install "numpy<2"
```

6. **Pydantic Version Issues**
```bash
pip install pydantic==1.10.12
```

### Debug Mode
Set `DEBUG=true` in your `.env` file for verbose logging including:
- Complete history retrieval details
- Context injection information
- Agent decision reasoning
- ChromaDB operation details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Run the test scripts: `python test_system.py` and `python test_historical_context.py`
3. Search existing issues
4. Create a new issue with detailed information

---

**Note**: This system requires an active OpenAI API key and internet connection for full functionality. ChromaDB operates locally and does not require external services. Each agent receives complete conversation history for maximum context awareness and continuity. ChromaDB is a required dependency - the system will not function without it. 