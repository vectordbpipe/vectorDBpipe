import pytest
from unittest.mock import MagicMock, patch
from vectorDBpipe.vectordb.store import get_vector_store

def test_chroma_insert_and_search(tmp_path):
    store = get_vector_store("chroma", {"persist_directory": str(tmp_path)})
    vectors = [[0.1, 0.2, 0.3]]
    metadata = [{"source": "test"}]
    store.insert_vectors(vectors, metadata)
    result = store.search_vectors([0.1, 0.2, 0.3], top_k=1)
    assert result is not None

def test_pinecone_init_v3():
    """Test compatibility with Pinecone v3 client instantiation."""
    import sys
    
    # Mock pinecone module before importing/using the store
    mock_pinecone = MagicMock()
    
    with patch.dict(sys.modules, {"pinecone": mock_pinecone}):
        # We must re-import inside the patch context so it sees the mocked module
        from vectorDBpipe.vectordb.store import PineconeVectorStore
        
        # Setup mock client return
        mock_client = MagicMock()
        mock_pinecone.Pinecone.return_value = mock_client
        
        # mimic list_indexes returning an object with .name attribute
        mock_index_obj = MagicMock()
        mock_index_obj.name = "existing-index"
        mock_client.list_indexes.return_value = [mock_index_obj]
        
        # Case 1: Index exists
        store = PineconeVectorStore(api_key="test-key", index_name="existing-index")
        mock_pinecone.Pinecone.assert_called_with(api_key="test-key")
        mock_client.create_index.assert_not_called()
        mock_client.Index.assert_called_with("existing-index")
        
        # Case 2: Index does not exist (should attempt create)
        # Reset mock for fresh call stats
        mock_client.reset_mock()
        mock_client.list_indexes.return_value = [mock_index_obj] 
        
        store = PineconeVectorStore(api_key="test-key", index_name="new-index")
        mock_client.create_index.assert_called()
