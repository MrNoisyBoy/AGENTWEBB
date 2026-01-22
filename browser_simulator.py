# main.py
import time
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import random


# Имитация браузерного управления
class BrowserAction(Enum):
    CLICK = "click"
    TYPE = "type"
    NAVIGATE = "navigate"
    SCROLL = "scroll"
    EXTRACT = "extract"
    WAIT = "wait"


@dataclass
class BrowserCommand:
    action: BrowserAction
    selector: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None


class BrowserSimulator:
    """Симулятор браузера для демонстрации"""

    def __init__(self):
        self.current_url = "about:blank"
        self.page_content = []
        self.history = []

    def navigate(self, url: str) -> List[Dict[str, str]]:
        """Переход по URL"""
        self.current_url = url
        self.history.append(f"Navigated to: {url}")

        # Имитация загрузки страницы
        if "mail" in url:
            self.page_content = [
                {"type": "link", "text": "Входящие", "selector": "#inbox"},
                {"type": "link", "text": "Спам", "selector": "#spam"},
                {"type": "email", "sender": "Amazon", "subject": "Ваш заказ отправлен", "selector": ".email-1"},
                {"type": "email", "sender": "Спам-рассылка", "subject": "Вы выиграли iPhone!", "selector": ".email-2"},
                {"type": "button", "text": "Удалить", "selector": ".delete-btn"},
                {"type": "button", "text": "Прочитано", "selector": ".read-btn"}
            ]
        elif "hh.ru" in url:
            self.page_content = [
                {"type": "input", "text": "Поиск вакансий", "selector": "#search"},
                {"type": "vacancy", "title": "AI-инженер", "company": "Yandex", "selector": ".vacancy-1"},
                {"type": "vacancy", "title": "ML Engineer", "company": "Sber", "selector": ".vacancy-2"},
                {"type": "button", "text": "Откликнуться", "selector": ".apply-btn"}
            ]

        return self.page_content

    def click(self, selector: str) -> str:
        """Клик по элементу"""
        for item in self.page_content:
            if item.get("selector") == selector:
                self.history.append(f"Clicked: {item.get('text', selector)}")
                return f"Clicked on {item.get('text', selector)}"
        return f"Element {selector} not found"

    def type_text(self, selector: str, text: str) -> str:
        """Ввод текста"""
        self.history.append(f"Typed '{text}' into {selector}")
        return f"Typed: {text}"

    def extract_text(self) -> List[Dict[str, str]]:
        """Извлечение текста со страницы"""
        return self.page_content

    def execute_command(self, command: BrowserCommand) -> Any:
        """Выполнение команды"""
        if command.action == BrowserAction.NAVIGATE:
            return self.navigate(command.url)
        elif command.action == BrowserAction.CLICK:
            return self.click(command.selector)
        elif command.action == BrowserAction.TYPE:
            return self.type_text(command.selector, command.text)
        elif command.action == BrowserAction.EXTRACT:
            return self.extract_text()
        elif command.action == BrowserAction.WAIT:
            time.sleep(1)
            return "Waited 1 second"


class LocalLLMSimulator:
    """Локальный симулятор LLM для демонстрации"""

    def analyze_task(self, task: str, context: List[Dict]) -> BrowserCommand:
        """Анализ задачи и генерация команды (имитация AI)"""

        task_lower = task.lower()

        if "почт" in task_lower or "mail" in task_lower:
            if "удалить" in task_lower and "спам" in task_lower:
                return BrowserCommand(
                    action=BrowserAction.NAVIGATE,
                    url="https://mail.example.com"
                )
            elif "прочита" in task_lower:
                return BrowserCommand(
                    action=BrowserAction.CLICK,
                    selector="#inbox"
                )

        elif "ваканс" in task_lower or "hh.ru" in task_lower:
            return BrowserCommand(
                action=BrowserAction.NAVIGATE,
                url="https://hh.ru/vacancies"
            )

        elif "заказ" in task_lower or "еда" in task_lower:
            return BrowserCommand(
                action=BrowserAction.NAVIGATE,
                url="https://delivery.example.com"
            )

        # По умолчанию - извлечь контент
        return BrowserCommand(action=BrowserAction.EXTRACT)


class AutonomousBrowserAgent:
    """Автономный AI-агент для управления браузером"""

    def __init__(self):
        self.browser = BrowserSimulator()
        self.llm = LocalLLMSimulator()
        self.task_history = []
        self.max_steps = 20

    def process_task(self, task: str) -> Dict[str, Any]:
        """Обработка задачи пользователя"""
        print(f"\n🔧 Новая задача: {task}")
        print("-" * 50)

        steps = []
        current_step = 1

        while current_step <= self.max_steps:
            print(f"\nШаг {current_step}:")

            # Извлекаем текущий контекст страницы
            context = self.browser.extract_text()

            # AI решает, что делать дальше
            command = self.llm.analyze_task(task, context)

            # Выполняем команду
            result = self.browser.execute_command(command)

            # Логируем шаг
            step_info = {
                "step": current_step,
                "command": asdict(command),
                "result": str(result)[:100] + "..." if len(str(result)) > 100 else str(result),
                "url": self.browser.current_url
            }
            steps.append(step_info)

            print(f"  Действие: {command.action.value}")
            if command.selector:
                print(f"  Селектор: {command.selector}")
            if command.text:
                print(f"  Текст: {command.text}")
            if command.url:
                print(f"  URL: {command.url}")
            print(f"  Результат: {step_info['result']}")

            # Проверяем завершение задачи
            if self._is_task_complete(task, context, current_step):
                print("\n✅ Задача выполнена!")
                break

            current_step += 1

            # Небольшая пауза между шагами для реалистичности
            time.sleep(0.5)

        return {
            "task": task,
            "steps": steps,
            "total_steps": current_step,
            "final_url": self.browser.current_url,
            "history": self.browser.history
        }

    def _is_task_complete(self, task: str, context: List[Dict], step: int) -> bool:
        """Определение, завершена ли задача (имитация AI-анализа)"""
        task_lower = task.lower()

        if "прочита" in task_lower and step >= 3:
            return True
        elif "удалить" in task_lower and step >= 5:
            return True
        elif "найди" in task_lower and step >= 4:
            return True
        elif step >= self.max_steps:
            return True

        return False


def main():
    """Главная функция для демонстрации работы агента"""
    print("🚀 Автономный AI-агент для управления браузером")
    print("=" * 50)

    agent = AutonomousBrowserAgent()

    # Примеры задач
    tasks = [
        "Прочитай последние 10 писем в моей почте и удали спам",
        "Найди 3 подходящие вакансии AI-инженера на hh.ru",
        "Закажи мне пиццу и колу на сайте доставки"
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n📋 Пример {i}: {task}")
        response = input("Запустить эту задачу? (y/n): ")

        if response.lower() == 'y':
            result = agent.process_task(task)

            print(f"\n📊 Отчет по задаче:")
            print(f"Всего шагов: {result['total_steps']}")
            print(f"Финальный URL: {result['final_url']}")
            print("\nИстория действий:")
            for action in result['history'][-5:]:
                print(f"  • {action}")


if __name__ == "__main__":
    main()