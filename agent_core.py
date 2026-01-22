# agent_core.py
import time
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Any, Optional
import random


class BrowserAction(Enum):
    CLICK = "click"
    TYPE = "type"
    NAVIGATE = "navigate"
    SCROLL = "scroll"
    EXTRACT = "extract"
    WAIT = "wait"
    SUBMIT = "submit"
    BACK = "back"
    REFRESH = "refresh"


@dataclass
class BrowserCommand:
    action: BrowserAction
    selector: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None
    coordinates: Optional[tuple] = None
    description: Optional[str] = None


class BrowserSimulator:
    """Улучшенный симулятор браузера"""

    def __init__(self):
        self.current_url = "about:blank"
        self.page_content = []
        self.history = []
        self.window_size = (1920, 1080)
        self.cookies = {}
        self.session_data = {}

    def navigate(self, url: str) -> List[Dict[str, Any]]:
        """Переход по URL с имитацией разных сайтов"""
        self.current_url = url
        self.history.append({"action": "navigate", "url": url, "timestamp": time.time()})

        # Имитация контента для разных сайтов
        if "mail" in url or "почт" in url:
            self.page_content = self._generate_email_content()
        elif "hh.ru" in url or "ваканс" in url:
            self.page_content = self._generate_job_content()
        elif "доставк" in url or "еда" in url or "food" in url:
            self.page_content = self._generate_food_content()
        elif "google" in url or "поиск" in url:
            self.page_content = self._generate_search_content()
        else:
            self.page_content = self._generate_generic_content()

        return self.page_content

    def _generate_email_content(self):
        """Генерация контента почтового сервиса"""
        emails = [
            {"type": "email", "sender": "Amazon", "subject": "Ваш заказ #12345 отправлен",
             "preview": "Товар будет доставлен 15 декабря", "selector": ".email-amazon",
             "category": "покупки", "unread": False},
            {"type": "email", "sender": "Спам-рассылка", "subject": "Вы выиграли iPhone 15!",
             "preview": "Для получения приза перейдите по ссылке...", "selector": ".email-spam",
             "category": "спам", "unread": True},
            {"type": "email", "sender": "ГитХаб", "subject": "Новые коммиты в репозитории",
             "preview": "В ваших репозиториях есть новые изменения", "selector": ".email-github",
             "category": "уведомления", "unread": True},
            {"type": "email", "sender": "Коллега", "subject": "Встреча в 15:00",
             "preview": "Не забудьте про совещание по проекту", "selector": ".email-work",
             "category": "работа", "unread": False},
        ]

        controls = [
            {"type": "button", "text": "Написать письмо", "selector": ".btn-compose", "action": "compose"},
            {"type": "button", "text": "Удалить", "selector": ".btn-delete", "action": "delete"},
            {"type": "button", "text": "Пометить как прочитанное", "selector": ".btn-mark-read", "action": "mark_read"},
            {"type": "button", "text": "В спам", "selector": ".btn-spam", "action": "mark_spam"},
            {"type": "tab", "text": "Входящие (15)", "selector": ".tab-inbox", "count": 15},
            {"type": "tab", "text": "Спам (3)", "selector": ".tab-spam", "count": 3},
            {"type": "tab", "text": "Отправленные", "selector": ".tab-sent", "count": 8},
        ]

        return emails + controls

    def _generate_job_content(self):
        """Генерация контента сайта вакансий"""
        vacancies = [
            {"type": "vacancy", "title": "AI-инженер", "company": "Яндекс",
             "salary": "от 300 000 ₽", "experience": "3+ года",
             "description": "Разработка ML-моделей для поиска", "selector": ".vacancy-1"},
            {"type": "vacancy", "title": "ML Researcher", "company": "Сбер",
             "salary": "от 350 000 ₽", "experience": "5+ лет",
             "description": "Исследования в области компьютерного зрения", "selector": ".vacancy-2"},
            {"type": "vacancy", "title": "Data Scientist", "company": "Тинькофф",
             "salary": "от 280 000 ₽", "experience": "2+ года",
             "description": "Анализ данных для финтех продуктов", "selector": ".vacancy-3"},
        ]

        controls = [
            {"type": "input", "text": "Должность, компания или ключевые слова", "selector": ".input-search",
             "placeholder": "Поиск вакансий"},
            {"type": "button", "text": "Найти", "selector": ".btn-search", "action": "search"},
            {"type": "button", "text": "Откликнуться", "selector": ".btn-apply", "action": "apply"},
            {"type": "filter", "text": "Опыт работы", "selector": ".filter-exp",
             "options": ["Нет опыта", "1-3 года", "3-6 лет"]},
            {"type": "filter", "text": "Зарплата", "selector": ".filter-salary",
             "options": ["до 100k", "100-200k", "200k+"]},
        ]

        return vacancies + controls

    def _generate_food_content(self):
        """Генерация контента сайта доставки еды"""
        restaurants = [
            {"type": "restaurant", "name": "Додо Пицца", "cuisine": "Пицца",
             "rating": "4.7 ★", "delivery_time": "30-40 мин",
             "min_order": "499 ₽", "selector": ".restaurant-1"},
            {"type": "restaurant", "name": "Burger King", "cuisine": "Бургеры",
             "rating": "4.5 ★", "delivery_time": "25-35 мин",
             "min_order": "299 ₽", "selector": ".restaurant-2"},
            {"type": "restaurant", "name": "Суши Весла", "cuisine": "Суши",
             "rating": "4.8 ★", "delivery_time": "40-50 мин",
             "min_order": "799 ₽", "selector": ".restaurant-3"},
        ]

        menu_items = [
            {"type": "menu_item", "name": "Пицца Пепперони", "price": "549 ₽",
             "description": "Острая салями, сыр моцарелла", "selector": ".item-1"},
            {"type": "menu_item", "name": "Чизбургер", "price": "199 ₽",
             "description": "Говяжья котлета, сыр, соус", "selector": ".item-2"},
            {"type": "menu_item", "name": "Кола", "price": "99 ₽",
             "description": "0.5 л", "selector": ".item-3"},
        ]

        controls = [
            {"type": "button", "text": "Добавить в корзину", "selector": ".btn-add-to-cart", "action": "add_to_cart"},
            {"type": "button", "text": "Оформить заказ", "selector": ".btn-checkout", "action": "checkout"},
            {"type": "input", "text": "Адрес доставки", "selector": ".input-address", "placeholder": "Введите адрес"},
        ]

        return restaurants + menu_items + controls

    def _generate_search_content(self):
        """Генерация контента поисковой системы"""
        results = [
            {"type": "search_result", "title": "Искусственный интеллект — Википедия",
             "url": "https://ru.wikipedia.org",
             "snippet": "Иску́сственный интелле́кт — свойство искусственных систем...",
             "selector": ".result-1"},
            {"type": "search_result", "title": "Новости AI на Хабре",
             "url": "https://habr.com", "snippet": "Последние статьи про машинное обучение и нейросети...",
             "selector": ".result-2"},
            {"type": "search_result", "title": "Курсы по Machine Learning",
             "url": "https://coursera.org", "snippet": "Бесплатные курсы от ведущих университетов...",
             "selector": ".result-3"},
        ]

        controls = [
            {"type": "input", "text": "Поиск в Google", "selector": ".input-google-search", "value": ""},
            {"type": "button", "text": "Поиск в Google", "selector": ".btn-google-search", "action": "search"},
            {"type": "button", "text": "Мне повезёт!", "selector": ".btn-lucky", "action": "lucky"},
        ]

        return results + controls

    def _generate_generic_content(self):
        """Генерация общего контента"""
        return [
            {"type": "heading", "text": "Добро пожаловать", "selector": ".heading-welcome"},
            {"type": "paragraph",
             "text": "Это демонстрационная страница. В реальной версии здесь будет контент с сайта.",
             "selector": ".para-1"},
            {"type": "link", "text": "Главная", "selector": ".link-home"},
            {"type": "link", "text": "О нас", "selector": ".link-about"},
            {"type": "link", "text": "Контакты", "selector": ".link-contact"},
            {"type": "button", "text": "Продолжить", "selector": ".btn-continue"},
        ]

    def click(self, selector: str) -> Dict[str, Any]:
        """Клик по элементу с имитацией реакции"""
        for item in self.page_content:
            if item.get("selector") == selector:
                action_result = {
                    "success": True,
                    "element": item.get('text', selector),
                    "action": item.get('action', 'click'),
                    "message": f"Выполнено: {item.get('text', 'действие')}"
                }

                # Имитация изменений после клика
                if item.get('action') == 'delete':
                    action_result['message'] = "Письмо удалено"
                elif item.get('action') == 'apply':
                    action_result['message'] = "Отклик отправлен"
                elif item.get('action') == 'add_to_cart':
                    action_result['message'] = "Товар добавлен в корзину"

                self.history.append({
                    "action": "click",
                    "selector": selector,
                    "result": action_result,
                    "timestamp": time.time()
                })

                return action_result

        return {"success": False, "message": f"Элемент {selector} не найден"}

    def type_text(self, selector: str, text: str) -> Dict[str, Any]:
        """Ввод текста"""
        result = {
            "success": True,
            "selector": selector,
            "text": text,
            "message": f"Введен текст: {text}"
        }

        self.history.append({
            "action": "type",
            "selector": selector,
            "text": text,
            "timestamp": time.time()
        })

        return result

    def extract_text(self) -> List[Dict[str, Any]]:
        """Извлечение текста со страницы"""
        return self.page_content

    def execute_command(self, command: BrowserCommand) -> Dict[str, Any]:
        """Выполнение команды"""
        if command.action == BrowserAction.NAVIGATE:
            return {"result": self.navigate(command.url)}
        elif command.action == BrowserAction.CLICK:
            return {"result": self.click(command.selector)}
        elif command.action == BrowserAction.TYPE:
            return {"result": self.type_text(command.selector, command.text)}
        elif command.action == BrowserAction.EXTRACT:
            return {"result": self.extract_text()}
        elif command.action == BrowserAction.WAIT:
            time.sleep(1)
            return {"result": "Ожидание 1 секунда"}
        elif command.action == BrowserAction.BACK:
            if len(self.history) > 1:
                self.history.pop()
                prev_action = self.history[-1] if self.history else None
                if prev_action and prev_action.get('action') == 'navigate':
                    self.current_url = prev_action.get('url', 'about:blank')
            return {"result": "Назад в истории"}

        return {"result": f"Неизвестное действие: {command.action}"}


class LocalLLMSimulator:
    """Имитация AI-модели для принятия решений"""

    def __init__(self):
        self.context_memory = []
        self.max_context_size = 10

    def analyze_task(self, task: str, page_context: List[Dict]) -> BrowserCommand:
        """Анализ задачи и генерация следующей команды"""

        task_lower = task.lower()
        page_elements_by_type = {}

        for elem in page_context:
            elem_type = elem.get('type', 'unknown')
            if elem_type not in page_elements_by_type:
                page_elements_by_type[elem_type] = []
            page_elements_by_type[elem_type].append(elem)

        # Стратегия для почты
        if any(word in task_lower for word in ['почт', 'mail', 'письм']):
            if 'удал' in task_lower and 'спам' in task_lower:
                # Ищем спам-письма
                spam_emails = [e for e in page_elements_by_type.get('email', [])
                               if 'спам' in str(e).lower() or e.get('category') == 'спам']
                if spam_emails:
                    return BrowserCommand(
                        action=BrowserAction.CLICK,
                        selector=spam_emails[0].get('selector'),
                        description="Клик по спам-письму для удаления"
                    )

                # Ищем кнопку удаления
                delete_buttons = [e for e in page_elements_by_type.get('button', [])
                                  if 'удал' in e.get('text', '').lower()]
                if delete_buttons:
                    return BrowserCommand(
                        action=BrowserAction.CLICK,
                        selector=delete_buttons[0].get('selector'),
                        description="Нажатие кнопки удаления"
                    )

                # Если еще не на почте - переходим
                return BrowserCommand(
                    action=BrowserAction.NAVIGATE,
                    url="https://mail.google.com",
                    description="Переход в почтовый сервис"
                )

            elif 'прочит' in task_lower or 'последн' in task_lower:
                # Ищем входящие
                inbox_tabs = [e for e in page_context if 'входящ' in e.get('text', '').lower()]
                if inbox_tabs:
                    return BrowserCommand(
                        action=BrowserAction.CLICK,
                        selector=inbox_tabs[0].get('selector'),
                        description="Открытие входящих писем"
                    )

                return BrowserCommand(
                    action=BrowserAction.EXTRACT,
                    description="Сбор информации о письмах"
                )

        # Стратегия для вакансий
        elif any(word in task_lower for word in ['ваканс', 'hh.ru', 'работ', 'job']):
            if 'ai' in task_lower or 'инженер' in task_lower:
                # Ищем поле поиска
                search_inputs = [e for e in page_elements_by_type.get('input', [])
                                 if any(word in e.get('text', '').lower() for word in ['поиск', 'search'])]

                if search_inputs:
                    return BrowserCommand(
                        action=BrowserAction.TYPE,
                        selector=search_inputs[0].get('selector'),
                        text="AI инженер",
                        description="Ввод поискового запроса"
                    )

                return BrowserCommand(
                    action=BrowserAction.NAVIGATE,
                    url="https://hh.ru/vacancies",
                    description="Переход на сайт вакансий"
                )

            elif 'отклик' in task_lower:
                apply_buttons = [e for e in page_elements_by_type.get('button', [])
                                 if 'отклик' in e.get('text', '').lower()]
                if apply_buttons:
                    return BrowserCommand(
                        action=BrowserAction.CLICK,
                        selector=apply_buttons[0].get('selector'),
                        description="Отклик на вакансию"
                    )

        # Стратегия для заказа еды
        elif any(word in task_lower for word in ['заказ', 'еда', 'пицц', 'бургер', 'доставк']):
            if 'пицц' in task_lower:
                pizza_items = [e for e in page_context if 'пицц' in e.get('name', '').lower()]
                if pizza_items:
                    return BrowserCommand(
                        action=BrowserAction.CLICK,
                        selector=pizza_items[0].get('selector'),
                        description="Выбор пиццы"
                    )

            add_buttons = [e for e in page_elements_by_type.get('button', [])
                           if 'добав' in e.get('text', '').lower() or 'корзин' in e.get('text', '').lower()]
            if add_buttons:
                return BrowserCommand(
                    action=BrowserAction.CLICK,
                    selector=add_buttons[0].get('selector'),
                    description="Добавление в корзину"
                )

            return BrowserCommand(
                action=BrowserAction.NAVIGATE,
                url="https://dostavka.ru",
                description="Переход на сайт доставки еды"
            )

        # Стратегия по умолчанию
        if not page_context or len(page_context) < 5:
            # Если страница пустая или почти пустая
            if 'google' in task_lower or 'поиск' in task_lower:
                return BrowserCommand(
                    action=BrowserAction.NAVIGATE,
                    url="https://google.com",
                    description="Переход в поисковую систему"
                )
            else:
                return BrowserCommand(
                    action=BrowserAction.EXTRACT,
                    description="Исследование текущей страницы"
                )

        # Пытаемся найти что-то полезное на странице
        interactive_elements = [e for e in page_context if e.get('type') in ['button', 'link', 'input']]
        if interactive_elements:
            return BrowserCommand(
                action=BrowserAction.CLICK if interactive_elements[0].get('type') != 'input' else BrowserAction.TYPE,
                selector=interactive_elements[0].get('selector'),
                text="тест" if interactive_elements[0].get('type') == 'input' else None,
                description=f"Взаимодействие с {interactive_elements[0].get('type')}"
            )

        return BrowserCommand(
            action=BrowserAction.EXTRACT,
            description="Сбор дополнительной информации"
        )


class AutonomousBrowserAgent:
    """Автономный AI-агент с улучшенной логикой"""

    def __init__(self):
        self.browser = BrowserSimulator()
        self.llm = LocalLLMSimulator()
        self.task_state = {
            "current_task": None,
            "step_count": 0,
            "completed_steps": [],
            "status": "idle",
            "start_time": None,
            "error_count": 0
        }
        self.max_steps = 30
        self.learned_patterns = []

    def process_task(self, task: str) -> Dict[str, Any]:
        """Основной метод обработки задачи"""
        self.task_state = {
            "current_task": task,
            "step_count": 0,
            "completed_steps": [],
            "status": "running",
            "start_time": time.time(),
            "error_count": 0
        }

        steps = []

        while self.task_state["step_count"] < self.max_steps:
            current_step = self.task_state["step_count"] + 1

            # Получаем текущий контекст
            context = self.browser.extract_text()

            # AI принимает решение
            command = self.llm.analyze_task(task, context)

            # Выполняем команду
            try:
                result = self.browser.execute_command(command)

                # Записываем шаг
                step_info = {
                    "step": current_step,
                    "command": asdict(command),
                    "result": result,
                    "context_preview": [{"type": e.get('type'), "text": e.get('text', e.get('name', ''))[:50]}
                                        for e in context[:3]],
                    "timestamp": time.time() - self.task_state["start_time"]
                }

                steps.append(step_info)
                self.task_state["completed_steps"].append(step_info)

                # Проверяем завершение
                if self._is_task_completed(task, context, current_step):
                    self.task_state["status"] = "completed"
                    break

            except Exception as e:
                self.task_state["error_count"] += 1
                steps.append({
                    "step": current_step,
                    "error": str(e),
                    "command": asdict(command),
                    "timestamp": time.time() - self.task_state["start_time"]
                })

                if self.task_state["error_count"] > 5:
                    self.task_state["status"] = "error"
                    break

            self.task_state["step_count"] = current_step

        # Формируем итоговый отчет
        return {
            "task": task,
            "steps": steps,
            "summary": {
                "total_steps": self.task_state["step_count"],
                "successful_steps": len([s for s in steps if 'error' not in s]),
                "error_steps": len([s for s in steps if 'error' in s]),
                "execution_time": time.time() - self.task_state["start_time"],
                "final_status": self.task_state["status"],
                "final_url": self.browser.current_url,
                "elements_found": len(context)
            },
            "browser_history": self.browser.history[-10:] if self.browser.history else []
        }

    def _is_task_completed(self, task: str, context: List[Dict], step: int) -> bool:
        """Определение, завершена ли задача"""
        task_lower = task.lower()

        # Простая эвристика завершения
        if "удал" in task_lower and step > 3:
            # Проверяем, есть ли сообщения об удалении
            recent_actions = self.browser.history[-3:]
            for action in recent_actions:
                if isinstance(action, dict) and 'удален' in str(action.get('result', '')).lower():
                    return True

        if "прочит" in task_lower and step > 2:
            return True

        if "найди" in task_lower and step > 4:
            # Проверяем, найдены ли результаты
            search_results = [e for e in context if e.get('type') in ['search_result', 'vacancy', 'restaurant']]
            if len(search_results) >= 3:
                return True

        if step >= self.max_steps:
            return True

        return False