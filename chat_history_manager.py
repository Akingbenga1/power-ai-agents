import os
import json
import uuid
import pickle
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional

# Import required dependencies for simple vector search
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError:
    raise ImportError("Required packages missing. Please install them with: pip install sentence-transformers scikit-learn numpy")

class ChatHistoryManager:
    def __init__(self, db_path="./vector_db", collection_name="chat_history"):
        """
        Initialize the ChatHistoryManager with simple vector database using sentence-transformers.
        
        Args:
            db_path: Path to store the database files
            collection_name: Name of the collection to store chat history
        """
        self.db_path = db_path
        self.collection_name = collection_name
        self.metadata_file = os.path.join(db_path, f"{collection_name}_metadata.json")
        self.embeddings_file = os.path.join(db_path, f"{collection_name}_embeddings.pkl")
        
        # Create directory if it doesn't exist
        os.makedirs(db_path, exist_ok=True)
        
        try:
            # Initialize sentence transformer for embeddings
            print("🔄 Loading sentence transformer model...")
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model
            self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
            
            # Initialize or load data
            self._load_or_create_data()
            
            print(f"✅ Vector database initialized: {collection_name}")
            print(f"📊 Total conversations: {len(self.metadata)}")
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize vector database: {e}")

    def _load_or_create_data(self):
        """Load existing data or create new storage."""
        if os.path.exists(self.metadata_file) and os.path.exists(self.embeddings_file):
            # Load existing data
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
            with open(self.embeddings_file, 'rb') as f:
                self.embeddings = pickle.load(f)
            print(f"✅ Loaded existing data with {len(self.metadata)} conversations")
        else:
            # Create new storage
            self.metadata = []
            self.embeddings = []
            print(f"✅ Created new vector database")

    def _save_data(self):
        """Save data to disk."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(self.embeddings, f)
        except Exception as e:
            print(f"⚠️ Warning: Failed to save data: {e}")

    def add_entry(self, user_prompt: str, manager_response: str, chosen_agent: str = None, agent_suggestion: str = None):
        """
        Adds an entry to the chat history with vector embeddings.
        
        Args:
            user_prompt: The user's input prompt
            manager_response: The AI Workforce Manager's response
            chosen_agent: The agent that was chosen (if any)
            agent_suggestion: Any agent suggestion made (if any)
        """
        try:
            # Create unique ID for this entry
            entry_id = str(uuid.uuid4())
            
            # Prepare metadata
            metadata = {
                "id": entry_id,
                "timestamp": datetime.now().isoformat(),
                "user_prompt": user_prompt,
                "manager_response": manager_response,
                "chosen_agent": chosen_agent or "None",
                "agent_suggestion": agent_suggestion or "None",
                "user_prompt_length": len(user_prompt),
                "manager_response_length": len(manager_response)
            }
            
            # Combine user prompt and manager response for embedding
            combined_text = f"User: {user_prompt}\nManager: {manager_response}"
            
            # Generate embedding
            embedding = self.encoder.encode(combined_text)
            
            # Add to storage
            self.metadata.append(metadata)
            self.embeddings.append(embedding)
            
            # Save to disk
            self._save_data()
            
            print(f"💾 Chat history saved to vector database (ID: {entry_id[:8]}...)")
            
        except Exception as e:
            raise RuntimeError(f"Failed to save chat history to vector database: {e}")

    def search_similar_conversations(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search for similar conversations using semantic similarity.
        
        Args:
            query: The search query
            n_results: Number of similar results to return
            
        Returns:
            List of similar conversation entries with metadata
        """
        try:
            if len(self.metadata) == 0:
                return []
            
            # Generate embedding for query
            query_embedding = self.encoder.encode(query)
            
            # Calculate cosine similarities
            embeddings_matrix = np.array(self.embeddings)
            similarities = cosine_similarity([query_embedding], embeddings_matrix)[0]
            
            # Get top n_results
            n_results = min(n_results, len(self.metadata))
            top_indices = np.argsort(similarities)[::-1][:n_results]
            
            similar_conversations = []
            for idx in top_indices:
                metadata = self.metadata[idx]
                similar_conversations.append({
                    "similarity_score": float(similarities[idx]),
                    "user_prompt": metadata["user_prompt"],
                    "manager_response": metadata["manager_response"],
                    "metadata": metadata
                })
            
            return similar_conversations
            
        except Exception as e:
            raise RuntimeError(f"Failed to search vector database: {e}")

    def get_recent_history(self, limit: int = 1000) -> List[Dict]:
        """
        Get recent chat history entries.
        
        Args:
            limit: Maximum number of recent entries to return
            
        Returns:
            List of recent conversation entries
        """
        try:
            if not self.metadata:
                return []
            
            # Sort by timestamp (most recent first)
            sorted_metadata = sorted(self.metadata, key=lambda x: x["timestamp"], reverse=True)
            
            # Return limited results
            recent_entries = []
            for entry in sorted_metadata[:limit]:
                recent_entries.append({
                    "timestamp": entry["timestamp"],
                    "user_prompt": entry["user_prompt"],
                    "manager_response": entry["manager_response"],
                    "chosen_agent": entry["chosen_agent"],
                    "agent_suggestion": entry["agent_suggestion"]
                })
            
            return recent_entries
            
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve recent history from vector database: {e}")

    def get_history(self) -> List[Dict]:
        """
        Retrieves all chat history (for backward compatibility).
        
        Returns:
            List of all conversation entries
        """
        return self.get_recent_history(limit=1000)  # Get up to 1000 recent entries

    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the chat history collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            return {
                "total_conversations": len(self.metadata),
                "collection_name": self.collection_name,
                "database_path": self.db_path,
                "embedding_dimension": self.embedding_dim
            }
        except Exception as e:
            raise RuntimeError(f"Failed to get collection stats: {e}")

    def clear_history(self):
        """
        Clear all chat history (use with caution).
        """
        try:
            # Clear data
            self.metadata = []
            self.embeddings = []
            
            # Remove files
            for file_path in [self.metadata_file, self.embeddings_file]:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            print(f"🗑️ Chat history cleared successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to clear history: {e}")

# Example Usage and Testing
if __name__ == "__main__":
    # Test the ChatHistoryManager
    history_manager = ChatHistoryManager()
    
    # Add some test entries
    history_manager.add_entry(
        "What's the weather like?", 
        "I'm not a weather bot, but I can help with other tasks.", 
        chosen_agent="None"
    )
    
    history_manager.add_entry(
        "Scrape website X for data.", 
        "Allocating to Web Scraper.", 
        chosen_agent="Web Scraper"
    )
    
    history_manager.add_entry(
        "Create a marketing report for my startup",
        "I'll assign this to the Market Research Analyst to gather comprehensive market data.",
        chosen_agent="Market Research Analyst"
    )
    
    # Test similarity search
    print("\n🔍 Testing similarity search for 'weather information':")
    similar = history_manager.search_similar_conversations("weather information", n_results=3)
    for i, conv in enumerate(similar, 1):
        print(f"{i}. Similarity: {conv['similarity_score']:.3f}")
        print(f"   User: {conv['user_prompt'][:50]}...")
        print(f"   Agent: {conv['metadata']['chosen_agent']}")
    
    # Test recent history
    print(f"\n📚 Recent history:")
    recent = history_manager.get_recent_history(limit=3)
    for entry in recent:
        print(f"- {entry['timestamp']}: {entry['user_prompt'][:30]}... -> {entry['chosen_agent']}")
    
    # Get stats
    print(f"\n📊 Collection stats:")
    stats = history_manager.get_collection_stats()
    print(f"Total conversations: {stats.get('total_conversations', 'Unknown')}")
    print(f"Embedding dimension: {stats.get('embedding_dimension', 'Unknown')}") 