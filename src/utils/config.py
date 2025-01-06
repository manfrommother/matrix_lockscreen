import json
from pathlib import Path
from typing import Any, Optional


class Config:
    """Класс для работы с конфигурацией приложения"""
    
    def __init__(self) -> None:
        """Инициализация конфигурации"""
        self.config_dir = Path.home() / '.screen_locker'
        self.config_file = self.config_dir / 'config.json'
        self.create_config_dir()
        self.load_config()
        
    def create_config_dir(self) -> None:
        """Создание директории для конфигурации"""
        self.config_dir.mkdir(exist_ok=True)
        
    def load_config(self) -> None:
        """Загрузка конфигурации из файла"""
        if not self.config_file.exists():
            self.config = {
                'first_run': True,
                'pin_hash': None,
                'hotkey': None,
                'animation_type': 'matrix',  # По умолчанию матричная анимация
                'custom_animations': []
            }
            self.save_config()
        else:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                
    def save_config(self) -> None:
        """Сохранение конфигурации в файл"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)
            
    def get(self, key: str) -> Any:
        """
        Получение значения из конфигурации
        
        Args:
            key: Ключ конфигурации
            
        Returns:
            Any: Значение из конфигурации
        """
        return self.config.get(key)
        
    def set(self, key: str, value: Any) -> None:
        """
        Установка значения в конфигурацию
        
        Args:
            key: Ключ конфигурации
            value: Значение для установки
        """
        self.config[key] = value
        self.save_config()
        
    def is_first_run(self) -> bool:
        """
        Проверка первого запуска
        
        Returns:
            bool: True если это первый запуск, иначе False
        """
        return self.config.get('first_run', True)
        
    def set_first_run_completed(self) -> None:
        """Установка флага завершения первого запуска"""
        self.config['first_run'] = False
        self.save_config()
        
    def get_pin_hash(self) -> Optional[bytes]:
        """
        Получение хеша PIN-кода
        
        Returns:
            Optional[bytes]: Хеш PIN-кода или None
        """
        pin_hash = self.config.get('pin_hash')
        return bytes.fromhex(pin_hash) if pin_hash else None
        
    def set_pin_hash(self, pin_hash: bytes) -> None:
        """
        Установка хеша PIN-кода
        
        Args:
            pin_hash: Хеш PIN-кода
        """
        self.config['pin_hash'] = pin_hash.hex()
        self.save_config()