"""
Тесты для конфигурации системы
"""

import pytest
import os
from unittest.mock import patch
from src.config import Config, ModelConfig, RAGConfig


class TestConfig:
    """Тесты класса Config"""
    
    def test_config_initialization(self):
        """Тест инициализации конфигурации"""
        config = Config()
        
        assert config.model is not None
        assert config.database is not None
        assert config.rag is not None
        assert config.security is not None
    
    def test_model_config_defaults(self):
        """Тест значений по умолчанию для ModelConfig"""
        model_config = ModelConfig(huggingface_token="test_token")
        
        assert model_config.huggingface_model == "microsoft/Phi-4-mini-instruct"
        assert model_config.embedding_device == "cpu"
        assert model_config.huggingface_token == "test_token"
    
    def test_rag_config_validation(self):
        """Тест валидации RAG конфигурации"""
        rag_config = RAGConfig()
        
        assert rag_config.chunk_size > 0
        assert rag_config.chunk_overlap >= 0
        assert rag_config.top_k_retrieval > 0
        assert 0 <= rag_config.similarity_threshold <= 1
    
    @patch.dict(os.environ, {"CHUNK_SIZE": "1000", "TOP_K_RETRIEVAL": "3"})
    def test_config_from_environment(self):
        """Тест загрузки конфигурации из переменных окружения"""
        config = Config()
        
        assert config.rag.chunk_size == 1000
        assert config.rag.top_k_retrieval == 3
    
    def test_config_validation_error(self):
        """Тест ошибки валидации конфигурации"""
        with patch.dict(os.environ, {"HUGGINGFACE_TOKEN": ""}):
            with pytest.raises(ValueError, match="HUGGINGFACE_TOKEN обязателен"):
                Config()
    
    def test_directory_creation(self, tmp_path):
        """Тест создания необходимых директорий"""
        with patch.dict(os.environ, {
            "DATA_DIR": str(tmp_path / "data"),
            "MODELS_DIR": str(tmp_path / "models"),
            "LOGS_DIR": str(tmp_path / "logs"),
            "HUGGINGFACE_TOKEN": "test_token"
        }):
            config = Config()
            
            assert config.data_dir.exists()
            assert config.models_dir.exists()
            assert config.logs_dir.exists()
            assert (config.data_dir / "knowledge_base").exists()
    
    def test_config_to_dict(self):
        """Тест конвертации конфигурации в словарь"""
        with patch.dict(os.environ, {"HUGGINGFACE_TOKEN": "test_token"}):
            config = Config()
            config_dict = config.to_dict()
            
            assert "model" in config_dict
            assert "database" in config_dict
            assert "rag" in config_dict
            assert "security" in config_dict
            assert "paths" in config_dict
    
    def test_is_production(self):
        """Тест определения продакшн окружения"""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "production",
            "HUGGINGFACE_TOKEN": "test_token"
        }):
            config = Config()
            assert config.is_production() is True
        
        with patch.dict(os.environ, {
            "ENVIRONMENT": "development", 
            "HUGGINGFACE_TOKEN": "test_token"
        }):
            config = Config()
            assert config.is_production() is False