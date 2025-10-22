"""
AI Legal Advisor - Конфигурация и настройки

Центральный модуль для управления конфигурацией приложения
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

@dataclass
class ModelConfig:
    """Конфигурация моделей"""
    huggingface_token: str
    huggingface_model: str = "microsoft/Phi-4-mini-instruct"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    moderation_model: str = "IlyaGusev/saiga_yandexgpt_8b_gguf"
    moderation_filename: str = "saiga_yandexgpt_8b.Q3_K_M.gguf"
    embedding_device: str = "cpu"

@dataclass
class DatabaseConfig:
    """Конфигурация базы данных"""
    chroma_persist_directory: str = "./data/chroma_db"
    chroma_collection_name: str = "legal_documents"
    
@dataclass
class APIConfig:
    """Конфигурация API"""
    host: str = "0.0.0.0"
    port: int = 8000
    streamlit_port: int = 8501
    max_workers: int = 4

@dataclass
class RAGConfig:
    """Конфигурация RAG системы"""
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_retrieval: int = 5
    similarity_threshold: float = 0.7
    bm25_k1: float = 1.2
    bm25_b: float = 0.75

@dataclass
class SecurityConfig:
    """Конфигурация безопасности"""
    enable_content_filter: bool = True
    max_query_length: int = 1000
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600
    enable_cors: bool = True
    allowed_origins: list = None

@dataclass
class CacheConfig:
    """Конфигурация кэширования"""
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    cache_ttl: int = 3600

@dataclass
class MonitoringConfig:
    """Конфигурация мониторинга"""
    enable_monitoring: bool = True
    log_level: str = "INFO"
    metrics_port: int = 8502
    phoenix_endpoint: Optional[str] = None

class Config:
    """Главный класс конфигурации"""
    
    def __init__(self):
        self.model = ModelConfig(
            huggingface_token=os.getenv("HUGGINGFACE_TOKEN", ""),
            huggingface_model=os.getenv("HUGGINGFACE_MODEL", "microsoft/Phi-4-mini-instruct"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"),
            moderation_model=os.getenv("MODERATION_MODEL", "IlyaGusev/saiga_yandexgpt_8b_gguf"),
            moderation_filename=os.getenv("MODERATION_FILENAME", "saiga_yandexgpt_8b.Q3_K_M.gguf"),
            embedding_device=os.getenv("EMBEDDING_DEVICE", "cpu")
        )
        
        self.database = DatabaseConfig(
            chroma_persist_directory=os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db"),
            chroma_collection_name=os.getenv("CHROMA_COLLECTION_NAME", "legal_documents")
        )
        
        self.api = APIConfig(
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", "8000")),
            streamlit_port=int(os.getenv("STREAMLIT_PORT", "8501")),
            max_workers=int(os.getenv("MAX_WORKERS", "4"))
        )
        
        self.rag = RAGConfig(
            chunk_size=int(os.getenv("CHUNK_SIZE", "500")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "50")),
            top_k_retrieval=int(os.getenv("TOP_K_RETRIEVAL", "5")),
            similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", "0.7")),
            bm25_k1=float(os.getenv("BM25_K1", "1.2")),
            bm25_b=float(os.getenv("BM25_B", "0.75"))
        )
        
        self.security = SecurityConfig(
            enable_content_filter=os.getenv("ENABLE_CONTENT_FILTER", "true").lower() == "true",
            max_query_length=int(os.getenv("MAX_QUERY_LENGTH", "1000")),
            rate_limit_requests=int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
            rate_limit_window=int(os.getenv("RATE_LIMIT_WINDOW", "3600")),
            enable_cors=os.getenv("ENABLE_CORS", "true").lower() == "true",
            allowed_origins=os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
        )
        
        self.cache = CacheConfig(
            redis_host=os.getenv("REDIS_HOST", "localhost"),
            redis_port=int(os.getenv("REDIS_PORT", "6379")),
            redis_db=int(os.getenv("REDIS_DB", "0")),
            cache_ttl=int(os.getenv("CACHE_TTL", "3600"))
        )
        
        self.monitoring = MonitoringConfig(
            enable_monitoring=os.getenv("ENABLE_MONITORING", "true").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            metrics_port=int(os.getenv("METRICS_PORT", "8502")),
            phoenix_endpoint=os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
        )
        
        # Пути к директориям
        self.data_dir = Path(os.getenv("DATA_DIR", "./data"))
        self.models_dir = Path(os.getenv("MODELS_DIR", "./models"))
        self.logs_dir = Path(os.getenv("LOGS_DIR", "./logs"))
        
        # Настройки окружения
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "true").lower() == "true"
        
        # Создаем необходимые директории
        self._create_directories()
        
        # Валидация конфигурации
        self._validate_config()
    
    def _create_directories(self):
        """Создание необходимых директорий"""
        directories = [
            self.data_dir,
            self.models_dir,
            self.logs_dir,
            self.data_dir / "knowledge_base",
            self.data_dir / "chroma_db",
            self.data_dir / "sample_docs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _validate_config(self):
        """Валидация конфигурации"""
        if not self.model.huggingface_token:
            raise ValueError("HUGGINGFACE_TOKEN обязателен для работы системы")
        
        if self.rag.chunk_size <= 0:
            raise ValueError("CHUNK_SIZE должен быть положительным числом")
        
        if self.rag.similarity_threshold < 0 or self.rag.similarity_threshold > 1:
            raise ValueError("SIMILARITY_THRESHOLD должен быть между 0 и 1")
    
    def get_model_cache_dir(self) -> Path:
        """Получить путь к директории кэша моделей"""
        return self.models_dir / "cache"
    
    def get_data_path(self, filename: str) -> Path:
        """Получить полный путь к файлу данных"""
        return self.data_dir / filename
    
    def is_production(self) -> bool:
        """Проверка, работает ли система в продакшене"""
        return self.environment.lower() == "production"
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертация конфигурации в словарь"""
        return {
            "model": self.model.__dict__,
            "database": self.database.__dict__,
            "api": self.api.__dict__,
            "rag": self.rag.__dict__,
            "security": self.security.__dict__,
            "cache": self.cache.__dict__,
            "monitoring": self.monitoring.__dict__,
            "paths": {
                "data_dir": str(self.data_dir),
                "models_dir": str(self.models_dir),
                "logs_dir": str(self.logs_dir)
            },
            "environment": self.environment,
            "debug": self.debug
        }

# Глобальный экземпляр конфигурации
config = Config()