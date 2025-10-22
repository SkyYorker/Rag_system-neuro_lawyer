"""
AI Юридический Консультант - Главное приложение Streamlit

Интерактивный веб-интерфейс для RAG-системы юридических консультаций
с демонстрацией всех ключевых возможностей.
"""

import streamlit as st
import time
import os
from datetime import datetime
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Конфигурация страницы
st.set_page_config(
    page_title="AI Юридический Консультант",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS стили
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .security-badge {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    .warning-badge {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Инициализация состояния сессии"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'query_count' not in st.session_state:
        st.session_state.query_count = 0
    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = {
            'response_times': [],
            'confidence_scores': [],
            'security_checks': [],
            'queries': []
        }

def mock_rag_response(query: str) -> Dict:
    """
    Имитация ответа RAG системы для демонстрации
    В реальной реализации здесь будет вызов вашей RAG системы
    """
    time.sleep(2)  # Имитация времени обработки
    
    responses = {
        "ооо": {
            "answer": """Для регистрации ООО (Общества с ограниченной ответственностью) в России необходимы следующие документы:

**Основные документы:**
1. **Устав ООО** - основной учредительный документ
2. **Решение единственного учредителя** или **Протокол общего собрания учредителей**
3. **Заявление по форме Р11001** - заявление о государственной регистрации
4. **Документ об уплате государственной пошлины** (4000 рублей)

**Дополнительные документы:**
- Копии паспортов всех учредителей
- Документы на юридический адрес (договор аренды или гарантийное письмо)
- Если учредители - иностранные граждане: переводы документов и справки о несудимости

**Особенности:**
- Минимальный уставный капитал: 10 000 рублей
- Срок регистрации: 3 рабочих дня
- Возможна электронная подача документов через сайт ФНС""",
            "sources": [
                "Федеральный закон от 08.02.1998 N 14-ФЗ 'Об обществах с ограниченной ответственностью'",
                "Федеральный закон от 08.08.2001 N 129-ФЗ 'О государственной регистрации юридических лиц'"
            ],
            "confidence": 0.94,
            "security_status": "✅ Безопасно",
            "response_time": 2.3
        },
        "трудовой": {
            "answer": """Трудовой договор должен содержать следующие обязательные условия согласно ТК РФ:

**Обязательные условия (ст. 57 ТК РФ):**
1. **Место работы** (с указанием структурного подразделения)
2. **Трудовая функция** (должность, специальность, квалификация)
3. **Дата начала работы** (и срок действия для срочного договора)
4. **Условия оплаты труда** (размер тарифной ставки, оклада, доплат)
5. **Режим рабочего времени и времени отдыха**
6. **Гарантии и компенсации** за вредные условия труда
7. **Условия труда на рабочем месте**
8. **Условия об обязательном социальном страховании**

**Дополнительные условия:**
- Испытательный срок (не более 3 месяцев)
- Неразглашение служебной тайны
- Обязанность отработать определенный срок после обучения
- Дополнительное страхование

**Важно:** Договор составляется в двух экземплярах и подписывается обеими сторонами.""",
            "sources": [
                "Трудовой кодекс РФ, статья 57",
                "Трудовой кодекс РФ, статья 67"
            ],
            "confidence": 0.91,
            "security_status": "✅ Безопасно", 
            "response_time": 2.1
        }
    }
    
    # Поиск наиболее подходящего ответа
    query_lower = query.lower()
    for key, response in responses.items():
        if key in query_lower:
            return response
    
    # Общий ответ по умолчанию
    return {
        "answer": """Спасибо за ваш вопрос! Для получения точного юридического совета по вашему запросу рекомендую:

1. **Уточнить детали** - предоставьте больше информации о вашей ситуации
2. **Обратиться к специалисту** - консультация с квалифицированным юристом
3. **Изучить актуальное законодательство** - законы могут изменяться

*Данная система предоставляет общую информацию и не заменяет профессиональную юридическую консультацию.*""",
        "sources": ["Общие рекомендации"],
        "confidence": 0.75,
        "security_status": "✅ Безопасно",
        "response_time": 1.8
    }

def render_sidebar():
    """Боковая панель с информацией и настройками"""
    with st.sidebar:
        st.markdown("### 🛠️ Настройки системы")
        
        # Переключатели функций
        enable_security = st.checkbox("🛡️ Фильтр безопасности", value=True)
        enable_hallucination = st.checkbox("🧠 Детекция галлюцинаций", value=True)
        confidence_threshold = st.slider("🎯 Порог уверенности", 0.0, 1.0, 0.8, 0.05)
        
        st.markdown("---")
        st.markdown("### 📊 Статистика сессии")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Запросов", st.session_state.query_count)
        with col2:
            avg_time = 0
            if st.session_state.performance_metrics['response_times']:
                avg_time = sum(st.session_state.performance_metrics['response_times']) / len(st.session_state.performance_metrics['response_times'])
            st.metric("Ср. время", f"{avg_time:.1f}с")
        
        st.markdown("---")
        st.markdown("### 🔧 Технологии")
        
        tech_stack = {
            "🦜 LangChain": "RAG пайплайн",
            "🤗 HuggingFace": "LLM Phi-4-mini",
            "📊 ChromaDB": "Векторная БД",
            "🔍 BM25": "Ключевой поиск",
            "🛡️ HybridGuard": "Безопасность"
        }
        
        for tech, desc in tech_stack.items():
            st.markdown(f"**{tech}**: {desc}")

def render_performance_dashboard():
    """Дашборд производительности"""
    st.markdown("### 📈 Аналитика производительности")
    
    if not st.session_state.performance_metrics['response_times']:
        st.info("Выполните несколько запросов для отображения аналитики")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = st.session_state.performance_metrics
    
    with col1:
        avg_response_time = sum(metrics['response_times']) / len(metrics['response_times'])
        st.metric("Среднее время ответа", f"{avg_response_time:.2f}с")
    
    with col2:
        avg_confidence = sum(metrics['confidence_scores']) / len(metrics['confidence_scores'])
        st.metric("Средняя уверенность", f"{avg_confidence:.2%}")
    
    with col3:
        security_passed = sum(1 for status in metrics['security_checks'] if "✅" in status)
        security_rate = security_passed / len(metrics['security_checks']) if metrics['security_checks'] else 0
        st.metric("Безопасность", f"{security_rate:.1%}")
    
    with col4:
        st.metric("Всего запросов", len(metrics['queries']))
    
    # Графики производительности
    col1, col2 = st.columns(2)
    
    with col1:
        # График времени ответа
        fig_time = px.line(
            x=list(range(1, len(metrics['response_times']) + 1)),
            y=metrics['response_times'],
            title="Время ответа по запросам",
            labels={'x': 'Номер запроса', 'y': 'Время (сек)'}
        )
        fig_time.update_layout(height=300)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        # График уверенности
        fig_conf = px.bar(
            x=list(range(1, len(metrics['confidence_scores']) + 1)),
            y=metrics['confidence_scores'],
            title="Уверенность в ответах",
            labels={'x': 'Номер запроса', 'y': 'Уверенность'}
        )
        fig_conf.update_layout(height=300)
        st.plotly_chart(fig_conf, use_container_width=True)

def main():
    """Основная функция приложения"""
    initialize_session_state()
    
    # Заголовок
    st.markdown('<h1 class="main-header">⚖️ AI Юридический Консультант</h1>', unsafe_allow_html=True)
    
    # Описание системы
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🧠 Умная RAG-система</h4>
            <p>Гибридный поиск: векторный + BM25 для максимальной точности</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🛡️ Безопасность</h4>
            <p>Многоуровневая фильтрация и защита от галлюцинаций</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Мониторинг</h4>
            <p>Отслеживание производительности и качества в реальном времени</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Боковая панель
    render_sidebar()
    
    # Основной интерфейс чата
    st.markdown("### 💬 Задайте ваш юридический вопрос")
    
    # Примеры вопросов
    with st.expander("💡 Примеры вопросов"):
        example_questions = [
            "Какие документы нужны для регистрации ООО?",
            "Как правильно оформить трудовой договор?",
            "Каковы сроки исковой давности по договорам?",
            "Какая ответственность за нарушение авторских прав?",
            "Как расторгнуть договор аренды досрочно?"
        ]
        
        for i, question in enumerate(example_questions, 1):
            st.markdown(f"{i}. {question}")
    
    # Поле ввода вопроса
    user_query = st.text_area(
        "Ваш вопрос:",
        height=100,
        placeholder="Например: Какие документы нужны для регистрации ООО?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        submit_button = st.button("🚀 Отправить", type="primary")
    
    with col2:
        clear_button = st.button("🗑️ Очистить")
    
    if clear_button:
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.session_state.performance_metrics = {
            'response_times': [],
            'confidence_scores': [],
            'security_checks': [],
            'queries': []
        }
        st.rerun()
    
    # Обработка запроса
    if submit_button and user_query.strip():
        with st.spinner("🤔 Анализирую ваш вопрос..."):
            # Добавляем вопрос пользователя
            st.session_state.messages.append({
                "role": "user",
                "content": user_query,
                "timestamp": datetime.now()
            })
            
            # Получаем ответ от системы
            response = mock_rag_response(user_query)
            
            # Добавляем ответ системы
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now()
            })
            
            # Обновляем метрики
            st.session_state.query_count += 1
            st.session_state.performance_metrics['response_times'].append(response['response_time'])
            st.session_state.performance_metrics['confidence_scores'].append(response['confidence'])
            st.session_state.performance_metrics['security_checks'].append(response['security_status'])
            st.session_state.performance_metrics['queries'].append(user_query)
    
    # Отображение истории чата
    if st.session_state.messages:
        st.markdown("### 💬 История диалога")
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(f"**Вопрос:** {message['content']}")
                    st.caption(f"⏰ {message['timestamp'].strftime('%H:%M:%S')}")
            else:
                with st.chat_message("assistant"):
                    response_data = message['content']
                    
                    # Основной ответ
                    st.write("**Ответ:**")
                    st.write(response_data['answer'])
                    
                    # Метрики ответа
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("🎯 Уверенность", f"{response_data['confidence']:.1%}")
                    
                    with col2:
                        st.metric("⏱️ Время", f"{response_data['response_time']}с")
                    
                    with col3:
                        status_color = "green" if "✅" in response_data['security_status'] else "orange"
                        st.markdown(f"<span style='color: {status_color}'>{response_data['security_status']}</span>", 
                                  unsafe_allow_html=True)
                    
                    with col4:
                        st.metric("📚 Источники", len(response_data['sources']))
                    
                    # Источники
                    with st.expander("📖 Источники информации"):
                        for i, source in enumerate(response_data['sources'], 1):
                            st.write(f"{i}. {source}")
                    
                    st.caption(f"⏰ {message['timestamp'].strftime('%H:%M:%S')}")
    
    # Дашборд производительности
    if st.session_state.query_count > 0:
        st.markdown("---")
        render_performance_dashboard()
    
    # Футер
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 AI Юридический Консультант | Построен на LangChain + HuggingFace | 
        <a href='https://github.com/yourusername/ai-legal-advisor'>GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()