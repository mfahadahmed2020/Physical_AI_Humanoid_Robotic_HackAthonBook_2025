from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from uuid import uuid4
import logging
from ..database.config import settings


logger = logging.getLogger(__name__)


class QdrantService:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=False  # Set to True in production for better performance
        )
        
        # Collection name for textbook content
        self.collection_name = settings.VECTOR_STORE_COLLECTION_NAME or "robotics_textbook"
        
        # Initialize the collection if it doesn't exist
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize the Qdrant collection with appropriate vector configuration"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name not in collection_names:
                # Create a new collection
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # Default size for OpenAI embeddings
                        distance=models.Distance.COSINE
                    )
                )
                
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection already exists: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {e}")
            raise
    
    def store_embedding(self, 
                      content_id: str, 
                      text_content: str, 
                      embedding: List[float], 
                      metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Store a text content with its embedding in Qdrant"""
        try:
            # Prepare the point to be stored
            points = [
                models.PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload={
                        "content_id": content_id,
                        "text_content": text_content,
                        "metadata": metadata or {}
                    }
                )
            ]
            
            # Upsert the point
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Stored embedding for content: {content_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing embedding for content {content_id}: {e}")
            return False
    
    def search_similar(self, 
                     query_embedding: List[float], 
                     limit: int = 5, 
                     filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar content based on embedding"""
        try:
            # Prepare filters if provided
            qdrant_filters = None
            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    filter_conditions.append(
                        models.FieldCondition(
                            key=f"metadata.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )
                
                if filter_conditions:
                    qdrant_filters = models.Filter(
                        must=filter_conditions
                    )
            
            # Perform the search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=qdrant_filters
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content_id": result.payload.get("content_id"),
                    "text_content": result.payload.get("text_content"),
                    "metadata": result.payload.get("metadata", {}),
                    "score": result.score
                })
            
            logger.info(f"Found {len(formatted_results)} similar results")
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching for similar content: {e}")
            return []
    
    def delete_content(self, content_id: str) -> bool:
        """Delete a content from the vector store"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[content_id]
                )
            )
            
            logger.info(f"Deleted content from vector store: {content_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting content {content_id}: {e}")
            return False
    
    def get_content(self, content_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific content by ID"""
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[content_id]
            )
            
            if points:
                point = points[0]
                return {
                    "content_id": point.payload.get("content_id"),
                    "text_content": point.payload.get("text_content"),
                    "metadata": point.payload.get("metadata", {}),
                }
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving content {content_id}: {e}")
            return None