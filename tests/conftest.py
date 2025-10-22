"""
Конфигурация для тестов pytest
"""

import pytest
import sys
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

@pytest.fixture
def sample_legal_query():
    """Фикстура с примером юридического запроса"""
    return "Какие документы нужны для регистрации ООО?"

@pytest.fixture 
def sample_response():
    """Фикстура с примером ответа системы"""
    return {
        "answer": "Для регистрации ООО необходимы следующие документы...",
        "sources": [
            "ФЗ от 08.02.1998 N 14-ФЗ",
            "ФЗ от 08.08.2001 N 129-ФЗ"
        ],
        "confidence": 0.94,
        "security_status": "✅ Безопасно",
        "response_time": 2.3
    }

@pytest.fixture
def config():
    """Фикстура с тестовой конфигурацией"""
    from src.config import Config
    return Config()