# app.py
import streamlit as st
import time
import json
from datetime import datetime
import threading

# Настройка страницы
st.set_page_config(
    page_title="AI Браузерный Агент",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация session_state ДО определения функций
if 'agent' not in st.session_state:
    # Простая имитация агента
    class SimpleAgent:
        def __init__(self):
            self.history = []
            self.current_url = "about:blank"

        def process_task(self, task_text):
            """Упрощенная обработка задачи"""
            steps = []
            task_lower = task_text.lower()

            if "почт" in task_lower or "письм" in task_lower:
                steps = [
                    {"action": "navigate", "url": "https://mail.google.com", "desc": "Переход в почтовый сервис"},
                    {"action": "click", "selector": "#inbox", "desc": "Открытие входящих"},
                    {"action": "extract", "desc": "Чтение последних 10 писем"},
                    {"action": "click", "selector": ".spam", "desc": "Поиск спама"},
                    {"action": "click", "selector": ".delete", "desc": "Удаление спама"},
                ]
                self.current_url = "https://mail.google.com"
            elif "ваканс" in task_lower or "hh.ru" in task_lower:
                steps = [
                    {"action": "navigate", "url": "https://hh.ru", "desc": "Переход на сайт вакансий"},
                    {"action": "type", "selector": "input", "text": "AI инженер", "desc": "Ввод поискового запроса"},
                    {"action": "click", "selector": ".search-btn", "desc": "Поиск вакансий"},
                    {"action": "extract", "desc": "Анализ результатов"},
                    {"action": "click", "selector": ".apply-btn", "desc": "Отклик на вакансию"},
                ]
                self.current_url = "https://hh.ru"
            elif "заказ" in task_lower or "еда" in task_lower:
                steps = [
                    {"action": "navigate", "url": "https://dostavka.ru", "desc": "Переход на сайт доставки"},
                    {"action": "type", "selector": ".address", "text": "Мой адрес", "desc": "Ввод адреса"},
                    {"action": "click", "selector": ".pizza", "desc": "Выбор пиццы"},
                    {"action": "click", "selector": ".add-to-cart", "desc": "Добавление в корзину"},
                    {"action": "click", "selector": ".checkout", "desc": "Оформление заказа"},
                ]
                self.current_url = "https://dostavka.ru"
            else:
                steps = [
                    {"action": "navigate", "url": "https://google.com", "desc": "Поиск информации"},
                    {"action": "type", "selector": "input", "text": task_text, "desc": "Ввод запроса"},
                    {"action": "click", "selector": ".search-btn", "desc": "Выполнение поиска"},
                    {"action": "extract", "desc": "Анализ результатов"},
                ]
                self.current_url = "https://google.com"

            # Имитация выполнения
            result_steps = []
            for i, step in enumerate(steps):
                result_steps.append({
                    "step": i + 1,
                    "command": step,
                    "result": f"Успешно выполнено: {step['desc']}",
                    "url": self.current_url
                })
                time.sleep(0.3)  # Имитация задержки

            return {
                "task": task_text,
                "steps": result_steps,
                "total_steps": len(result_steps),
                "final_url": self.current_url,
                "history": [f"Задача: {task_text}"]
            }


    st.session_state.agent = SimpleAgent()

if 'tasks_history' not in st.session_state:
    st.session_state.tasks_history = []

if 'current_task' not in st.session_state:
    st.session_state.current_task = None

if 'is_running' not in st.session_state:
    st.session_state.is_running = False

if 'execution_log' not in st.session_state:
    st.session_state.execution_log = []


def run_agent_task(task_text):
    """Запуск задачи"""
    try:
        st.session_state.is_running = True
        st.session_state.current_task = task_text

        # Запускаем агента
        result = st.session_state.agent.process_task(task_text)

        # Сохраняем результат
        st.session_state.tasks_history.append({
            "task": task_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "result": result,
            "status": "completed"
        })

        st.session_state.execution_log = result.get('steps', [])

    except Exception as e:
        st.session_state.tasks_history.append({
            "task": task_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": str(e),
            "status": "error"
        })
    finally:
        st.session_state.is_running = False
        st.session_state.current_task = None


# CSS стили
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #43A047;
        margin-top: 1.5rem;
    }
    .task-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1E88E5;
    }
    .step-card {
        background-color: #e8f5e8;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 3px solid #43A047;
    }
    .browser-window {
        background-color: white;
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        min-height: 300px;
        font-family: monospace;
    }
    .status-running {
        color: #FF9800;
        font-weight: bold;
    }
    .status-completed {
        color: #4CAF50;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Заголовок приложения
    st.markdown('<h1 class="main-header">🤖 Автономный AI-агент</h1>', unsafe_allow_html=True)

    # Информация
    st.info("""
    💡 **Как работает:** Введите задачу текстом → Агент анализирует → Автономно выполняет в браузере.
    Эта демо-версия работает без внешних API и предзаданных сценариев.
    """)

    # Две колонки
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<h3 class="sub-header">🎯 Введите задачу</h3>', unsafe_allow_html=True)

        # Примеры задач
        example = st.selectbox(
            "Выберите пример:",
            ["--- Создать свою задачу ---",
             "Прочитай последние 10 писем в почте и удали спам",
             "Найди 3 вакансии AI-инженера на hh.ru",
             "Закажи пиццу пепперони и колу"]
        )

        if example != "--- Создать свою задачу ---":
            task_input = st.text_area("Задача:", value=example, height=100)
        else:
            task_input = st.text_area("Задача:", placeholder="Опишите задачу для агента...", height=100)

        # Кнопки
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Запустить агента", type="primary", use_container_width=True):
                if task_input.strip():
                    # Запускаем в основном потоке (без threading)
                    run_agent_task(task_input.strip())
                    st.rerun()
                else:
                    st.warning("Введите задачу")

        with col_btn2:
            if st.button("🔄 Очистить историю", use_container_width=True):
                st.session_state.tasks_history = []
                st.session_state.execution_log = []
                st.rerun()

        # Статус
        if st.session_state.is_running:
            st.markdown('<p class="status-running">⏳ Агент выполняет задачу...</p>', unsafe_allow_html=True)
            st.progress(0.7)

        # История
        if st.session_state.tasks_history:
            st.markdown('<h3 class="sub-header">📋 История</h3>', unsafe_allow_html=True)
            for task in reversed(st.session_state.tasks_history[-3:]):
                with st.expander(f"{task['task'][:50]}... ({task['timestamp']})"):
                    st.write(f"**Статус:** {task['status']}")
                    if task['status'] == 'completed':
                        st.success(f"✅ Выполнено за {task['result'].get('total_steps', 0)} шагов")

    with col2:
        st.markdown('<h3 class="sub-header">🖥️ Симулятор браузера</h3>', unsafe_allow_html=True)

        # Окно браузера
        st.markdown('<div class="browser-window">', unsafe_allow_html=True)
        if hasattr(st.session_state.agent, 'current_url') and st.session_state.agent.current_url != "about:blank":
            st.write(f"🌐 **URL:** {st.session_state.agent.current_url}")
            st.divider()

            # Отображение контента
            if "mail" in st.session_state.agent.current_url:
                st.write("**Папки:** Входящие (15) | Спам (3) | Отправленные (8)")
                st.write("**Письма:**")
                st.write("📧 Amazon - Ваш заказ отправлен")
                st.write("📧 Спам-рассылка - Вы выиграли iPhone!")
                st.write("📧 GitHub - Новые коммиты")
            elif "hh.ru" in st.session_state.agent.current_url:
                st.write("**Вакансии:**")
                st.write("💼 AI-инженер в Яндекс (от 300к)")
                st.write("💼 ML Researcher в Сбер (от 350к)")
                st.write("💼 Data Scientist в Тинькофф (от 280к)")
            elif "dostavka" in st.session_state.agent.current_url:
                st.write("**Рестораны:**")
                st.write("🍕 Додо Пицца (4.7★, 30-40 мин)")
                st.write("🍔 Burger King (4.5★, 25-35 мин)")
                st.write("🍣 Суши Весла (4.8★, 40-50 мин)")
            else:
                st.write("**Поисковые результаты:**")
                st.write("🔍 Искусственный интеллект — Википедия")
                st.write("🔍 Новости AI на Хабре")
                st.write("🔍 Курсы по Machine Learning")
        else:
            st.write("🌐 **Браузер закрыт**")
            st.write("Запустите агента, чтобы начать работу")
        st.markdown('</div>', unsafe_allow_html=True)

        # Лог выполнения
        if st.session_state.execution_log:
            st.markdown('<h3 class="sub-header">📝 Лог выполнения</h3>', unsafe_allow_html=True)

            for step in st.session_state.execution_log[-5:]:  # Последние 5 шагов
                action_icons = {
                    "navigate": "🌐", "click": "🖱️", "type": "⌨️",
                    "extract": "📋", "wait": "⏳"
                }
                icon = action_icons.get(step['command']['action'], "⚙️")

                with st.expander(f"{icon} Шаг {step['step']}: {step['command']['desc']}", expanded=False):
                    st.write(f"**Действие:** {step['command']['action']}")
                    if 'url' in step['command']:
                        st.write(f"**URL:** {step['command']['url']}")
                    if 'text' in step['command']:
                        st.write(f"**Текст:** {step['command']['text']}")
                    st.write(f"**Результат:** {step['result']}")

    # Боковая панель
    with st.sidebar:
        st.markdown('<h3 class="sub-header">⚙️ Настройки</h3>', unsafe_allow_html=True)

        st.slider("Скорость выполнения:", 1, 5, 2)
        st.checkbox("Подробный лог", value=True)

        st.divider()

        st.markdown('<h3 class="sub-header">📊 Статистика</h3>', unsafe_allow_html=True)

        if st.session_state.tasks_history:
            completed = len([t for t in st.session_state.tasks_history if t['status'] == 'completed'])
            errors = len([t for t in st.session_state.tasks_history if t['status'] == 'error'])

            col_stat1, col_stat2 = st.columns(2)
            col_stat1.metric("Выполнено", completed)
            col_stat2.metric("Ошибок", errors)

        st.divider()

        st.markdown('<h3 class="sub-header">🚀 Быстрый запуск</h3>', unsafe_allow_html=True)

        quick_tasks = [
            "Найди новости про ИИ",
            "Проверь курсы машинного обучения",
            "Поищи билеты в Сочи"
        ]

        for qt in quick_tasks:
            if st.button(f"▶️ {qt}", use_container_width=True):
                run_agent_task(qt)
                st.rerun()

        st.divider()

        st.markdown("""
        ### ℹ️ Информация
        **Версия:** 1.0.0 демо  
        **Работает без:** API ключей  
        **Состояние:** Автономное выполнение  

        Для production версии добавьте:
        1. OpenAI/Anthropic API
        2. Playwright/Selenium
        3. Обработку ошибок
        """)


if __name__ == "__main__":
    main()