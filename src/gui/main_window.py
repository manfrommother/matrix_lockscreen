from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from src.utils.config import Config
from src.core.security import SecurityManager
from typing import Optional


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self, config: Config) -> None:
        """
        Инициализация главного окна
        
        Args:
            config: Объект конфигурации
        """
        super().__init__()
        
        self.config = config
        self.security = SecurityManager()
        
        self.setWindowTitle("Screen Locker")
        self.setGeometry(100, 100, 400, 300)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создаем layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Добавляем кнопки
        self.setup_buttons(layout)
        
        # Проверяем первый запуск
        if self.config.is_first_run():
            self.show_first_run_dialog()
            
    def setup_buttons(self, layout: QVBoxLayout) -> None:
        """
        Настройка кнопок интерфейса
        
        Args:
            layout: Layout для размещения кнопок
        """
        # Кнопка настроек
        settings_btn = QPushButton("Настройки")
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn)
        
        # Кнопка блокировки (временно, потом будет по горячей клавише)
        lock_btn = QPushButton("Заблокировать экран")
        lock_btn.clicked.connect(self.lock_screen)
        layout.addWidget(lock_btn)
        
    def show_first_run_dialog(self) -> None:
        """Показ диалога первого запуска"""
        QMessageBox.information(
            self,
            "Добро пожаловать",
            "Добро пожаловать в Screen Locker!\n"
            "Пожалуйста, настройте PIN-код и горячие клавиши в настройках."
        )
        
    def show_settings(self) -> None:
        """Показ окна настроек"""
        # TODO: Реализовать окно настроек
        pass
        
    def lock_screen(self) -> None:
        """Блокировка экрана"""
        # TODO: Реализовать блокировку экрана
        pass

    def closeEvent(self, event) -> None:
        """
        Обработка закрытия окна
        
        Args:
            event: Событие закрытия
        """
        # Скрываем окно вместо закрытия
        event.ignore()
        self.hide()