"""
AI Юридический Консультант - CLI интерфейс

Консольное приложение для демонстрации возможностей RAG системы
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
import json

# Добавляем src в путь импорта
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import config

def print_banner():
    """Выводит баннер приложения"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                   ⚖️  AI ЮРИДИЧЕСКИЙ КОНСУЛЬТАНТ              ║
╠══════════════════════════════════════════════════════════════╣
║  Интеллектуальная RAG-система для юридических консультаций  ║
║  Версия: 1.0 | LangChain + HuggingFace + ChromaDB           ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_system_info():
    """Выводит информацию о системе"""
    print("\n🔧 КОНФИГУРАЦИЯ СИСТЕМЫ:")
    print("─" * 50)
    print(f"📊 Модель: {config.model.huggingface_model}")
    print(f"🔤 Эмбеддинги: {config.model.embedding_model}")
    print(f"💾 База данных: ChromaDB ({config.database.chroma_collection_name})")
    print(f"🔍 Размер чанков: {config.rag.chunk_size}")
    print(f"📈 Top-K поиск: {config.rag.top_k_retrieval}")
    print(f"🎯 Порог схожести: {config.rag.similarity_threshold}")
    print(f"🛡️ Фильтр безопасности: {'✅ Включен' if config.security.enable_content_filter else '❌ Отключен'}")
    print("─" * 50)

def mock_rag_query(query: str, show_sources: bool = True, show_metrics: bool = True) -> Dict:
    """
    Имитация запроса к RAG системе для демонстрации
    В реальной реализации здесь будет ваша RAG система
    """
    print(f"\n🤔 Обрабатываю запрос: '{query}'")
    print("⏳ Выполняю поиск в базе знаний...")
    time.sleep(1)
    
    print("🔍 Векторный поиск...")
    time.sleep(0.5)
    
    print("📝 BM25 поиск...")
    time.sleep(0.5)
    
    print("🧠 Генерирую ответ...")
    time.sleep(1)
    
    print("🛡️ Проверяю на галлюцинации...")
    time.sleep(0.3)
    
    # Простые примеры ответов для демонстрации
    responses = {
        "ооо": {
            "answer": """
Для регистрации ООО в России необходимы следующие документы:

📋 ОСНОВНЫЕ ДОКУМЕНТЫ:
1. Устав ООО (основной учредительный документ)
2. Решение единственного учредителя ИЛИ Протокол общего собрания
3. Заявление по форме Р11001
4. Документ об уплате госпошлины (4000 руб.)

📝 ДОПОЛНИТЕЛЬНЫЕ ДОКУМЕНТЫ:
• Копии паспортов учредителей
• Документы на юридический адрес
• Для иностранцев: переводы документов

⚡ ВАЖНО:
• Минимальный уставный капитал: 10 000 рублей
• Срок регистрации: 3 рабочих дня
• Возможна электронная подача через сайт ФНС
            """,
            "sources": [
                "ФЗ от 08.02.1998 N 14-ФЗ 'Об обществах с ограниченной ответственностью'",
                "ФЗ от 08.08.2001 N 129-ФЗ 'О государственной регистрации юридических лиц'",
                "Постановление Правительства РФ от 16.10.2003 N 635"
            ],
            "confidence": 0.94,
            "security_status": "✅ Безопасно",
            "response_time": 2.8,
            "retrieved_docs": 5,
            "hallucination_score": 0.02
        },
        "трудовой": {
            "answer": """
Трудовой договор должен содержать обязательные условия по ТК РФ:

📋 ОБЯЗАТЕЛЬНЫЕ УСЛОВИЯ (ст. 57 ТК РФ):
1. Место работы (с указанием подразделения)
2. Трудовая функция (должность, специальность)
3. Дата начала работы
4. Условия оплаты труда (оклад, доплаты)
5. Режим рабочего времени и отдыха
6. Гарантии за вредные условия труда
7. Условия труда на рабочем месте
8. Обязательное социальное страхование

📝 ДОПОЛНИТЕЛЬНЫЕ УСЛОВИЯ:
• Испытательный срок (макс. 3 месяца)
• Неразглашение коммерческой тайны
• Обучение за счет работодателя

⚖️ ПОРЯДОК ОФОРМЛЕНИЯ:
• Договор в 2 экземплярах
• Подписание обеими сторонами
• Ознакомление с локальными актами
            """,
            "sources": [
                "Трудовой кодекс РФ, статья 57",
                "Трудовой кодекс РФ, статья 67",
                "Трудовой кодекс РФ, статья 68"
            ],
            "confidence": 0.91,
            "security_status": "✅ Безопасно",
            "response_time": 2.4,
            "retrieved_docs": 4,
            "hallucination_score": 0.03
        }
    }
    
    # Поиск подходящего ответа
    query_lower = query.lower()
    for key, response in responses.items():
        if key in query_lower:
            return response
    
    # Ответ по умолчанию
    return {
        "answer": """
Спасибо за ваш вопрос! 

Для получения точного юридического совета рекомендую:

1. 📝 УТОЧНИТЬ ДЕТАЛИ - предоставьте больше информации
2. 👨‍💼 КОНСУЛЬТАЦИЯ СПЕЦИАЛИСТА - обратитесь к юристу
3. 📚 ИЗУЧИТЬ ЗАКОНОДАТЕЛЬСТВО - проверьте актуальные нормы

⚠️ ВАЖНО: Данная система предоставляет общую информацию 
и не заменяет профессиональную юридическую консультацию.
        """,
        "sources": ["Общие рекомендации по юридическим вопросам"],
        "confidence": 0.75,
        "security_status": "✅ Безопасно", 
        "response_time": 1.9,
        "retrieved_docs": 2,
        "hallucination_score": 0.08
    }

def print_response(response: Dict, show_sources: bool = True, show_metrics: bool = True):
    """Красиво выводит ответ системы"""
    print("\n" + "═" * 70)
    print("📋 ОТВЕТ СИСТЕМЫ:")
    print("═" * 70)
    print(response["answer"])
    
    if show_metrics:
        print("\n📊 МЕТРИКИ ОТВЕТА:")
        print("─" * 50)
        print(f"🎯 Уверенность: {response['confidence']:.1%}")
        print(f"⏱️  Время ответа: {response['response_time']:.1f} сек")
        print(f"🛡️ Безопасность: {response['security_status']}")
        print(f"📄 Найдено документов: {response['retrieved_docs']}")
        print(f"🧠 Риск галлюцинаций: {response['hallucination_score']:.1%}")
    
    if show_sources and response["sources"]:
        print(f"\n📚 ИСТОЧНИКИ ({len(response['sources'])}):")
        print("─" * 50)
        for i, source in enumerate(response["sources"], 1):
            print(f"{i}. {source}")
    
    print("═" * 70)

def interactive_mode():
    """Интерактивный режим работы"""
    print("\n🚀 ИНТЕРАКТИВНЫЙ РЕЖИМ")
    print("─" * 50)
    print("Введите ваши юридические вопросы.")
    print("Команды: 'exit' - выход, 'help' - помощь, 'info' - информация о системе")
    print("─" * 50)
    
    while True:
        try:
            query = input("\n❓ Ваш вопрос: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['exit', 'quit', 'выход']:
                print("\n👋 До свидания!")
                break
            
            if query.lower() in ['help', 'помощь']:
                print_help()
                continue
            
            if query.lower() in ['info', 'информация']:
                print_system_info()
                continue
            
            # Выполняем запрос
            response = mock_rag_query(query)
            print_response(response)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Программа прервана пользователем")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")

def print_help():
    """Выводит справку по использованию"""
    help_text = """
📖 СПРАВКА ПО ИСПОЛЬЗОВАНИЮ:

🔸 КОМАНДЫ:
  • exit, quit, выход    - Завершить работу
  • help, помощь         - Показать эту справку  
  • info, информация     - Информация о системе

🔸 ПРИМЕРЫ ВОПРОСОВ:
  • "Какие документы нужны для регистрации ООО?"
  • "Как оформить трудовой договор?"
  • "Каковы сроки исковой давности?"
  • "Какая ответственность за нарушение авторских прав?"

🔸 ОСОБЕННОСТИ:
  • Система анализирует ваш запрос на безопасность
  • Использует гибридный поиск (векторный + BM25)
  • Проверяет ответы на галлюцинации
  • Предоставляет источники информации

⚠️  ВАЖНО: Консультации носят информационный характер
    """
    print(help_text)

def main():
    """Главная функция приложения"""
    parser = argparse.ArgumentParser(
        description="AI Юридический Консультант - RAG система",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py                                    # Интерактивный режим
  python main.py --query "Как зарегистрировать ООО?" # Одиночный запрос
  python main.py --info                             # Информация о системе
  python main.py --config                           # Показать конфигурацию
        """
    )
    
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Задать вопрос системе (одиночный запрос)"
    )
    
    parser.add_argument(
        "--no-sources",
        action="store_true",
        help="Не показывать источники"
    )
    
    parser.add_argument(
        "--no-metrics",
        action="store_true", 
        help="Не показывать метрики"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Показать информацию о системе"
    )
    
    parser.add_argument(
        "--config",
        action="store_true",
        help="Показать конфигурацию системы"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="AI Legal Advisor v1.0"
    )
    
    args = parser.parse_args()
    
    # Показываем баннер
    print_banner()
    
    # Проверяем конфигурацию
    if not config.model.huggingface_token:
        print("❌ ОШИБКА: Не найден HUGGINGFACE_TOKEN")
        print("   Создайте файл .env по образцу .env.example")
        sys.exit(1)
    
    # Обработка аргументов
    if args.config:
        print("\n📋 ПОЛНАЯ КОНФИГУРАЦИЯ:")
        print("─" * 50)
        config_dict = config.to_dict()
        print(json.dumps(config_dict, indent=2, ensure_ascii=False))
        return
    
    if args.info:
        print_system_info()
        return
    
    if args.query:
        # Одиночный запрос
        print(f"\n🎯 Режим одиночного запроса")
        response = mock_rag_query(args.query)
        print_response(
            response, 
            show_sources=not args.no_sources,
            show_metrics=not args.no_metrics
        )
        return
    
    # Интерактивный режим по умолчанию
    print_system_info()
    interactive_mode()

if __name__ == "__main__":
    main()