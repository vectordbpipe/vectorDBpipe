
import os
import pytest
from vectorDBpipe.vectordb.store import FaissVectorStore

def test_faiss_persistence(tmp_path):
    index_path = str(tmp_path / "faiss_test.index")
    # Clean up if exists (tmp_path is unique per test but good practice)
    if os.path.exists(index_path):
        os.remove(index_path)

    store = FaissVectorStore(index_path=index_path)

    vectors = [[0.1, 0.2, 0.3]]
    metadata = [{"source": "test"}]

    # Insert vectors - should NOT save to disk yet
    store.insert_vectors(vectors, metadata)
    assert not os.path.exists(index_path), "FAISS index should not be on disk before persist()"

    # Persist - should save to disk
    store.persist()
    assert os.path.exists(index_path), "FAISS index should be on disk after persist()"
    assert os.path.exists(index_path + "_metadata.pkl"), "Metadata should be on disk after persist()"

    # Verify search (in-memory search should work regardless of persist, but good to check)
    results = store.search_vectors([0.1, 0.2, 0.3], top_k=1)
    assert len(results) == 1
    assert results[0]["id"] == "id_0"

def test_faiss_search_without_persist(tmp_path):
    # Verify that search works even if we haven't persisted yet (in-memory)
    index_path = str(tmp_path / "faiss_mem.index")
    store = FaissVectorStore(index_path=index_path)

    vectors = [[0.5, 0.5]]
    metadata = [{"id": "mem_vec"}]
    store.insert_vectors(vectors, metadata)

    # Search immediately
    results = store.search_vectors([0.5, 0.5], top_k=1)
    assert len(results) == 1
    assert results[0]["id"] == "mem_vec"

    # Still not on disk
    assert not os.path.exists(index_path)
