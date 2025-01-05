import re
import bcrypt
from typing import Optional
from datetime import datetime, timedelta


class SecurityManager:
    '''Менеджер безопасности приложения'''

    def __init__(self):
        self.failed_attempts = 0
        self.blocked_untils: Optional[datetime] = None

    @staticmethod
    def validate_pin(pin: str) -> bool:
        '''
        Проверка корректности PIN-кода
        
        Args:
            pin: PIN-код для проверки
            
        Returns:
            bool: True если PIN-код корректный, иначе False
        '''
        #PIN должен содержать ровно 4 цифры
        return bool(re.match(r'^\d{4}$', pin))
    
    @staticmethod
    def hash_pin(pin:str) -> bytes:
        '''
        Хеширование PIN-кода
        
        Args:
            pin: PIN-код для хеширования
            
        Returns:
            bytes: Хеш PIN-кода
        '''
        return bcrypt.hashpw(pin.encode(), bcrypt.gensalt())
    
    @staticmethod
    def verify_pin(pin: str, hashed_pin: bytes) -> bool:
        '''
        Проверка PIN-кода
        Args:
            pin: PIN-код для проверки
            hashed_pin: Хешированный PIN-код
            
        Returns:
            bool: True если PIN-код верный, иначе False
        '''
        return bcrypt.checkpw(pin.encode(), hashed_pin)
    
    def check_block_status(self) -> tuple[bool, Optional[timedelta]]:
        """
        Проверка статуса блокировки
        
        Returns:
            tuple: (заблокировано ли, оставшееся время блокировки)
        """
        if not self.blocked_untils:
            return False, None
        
        now = datetime.now()
        if now < self.blocked_untils:
            return True, self.blocked_untils - now
        
        return False, None
    
    def update_failed_attempts(self) -> Optional[timedelta]:
        """
        Обновление счетчика неудачных попыток
        
        Returns:
            Optional[timedelta]: Время блокировки, если оно установлено
        """
        self.failed_attempts += 1
        
        #определяет время блокировки в зависимости от количества попыток
        block_time = None
        if self.failed_attempts == 3:
            block_time = timedelta(minutes=1)
        elif self.failed_attempts == 6:
            block_time = timedelta(minutes=2)
        elif self.failed_attempts == 9:
            block_time = timedelta(minutes=5)
        elif self.failed_attempts == 12:
            block_time = timedelta(minutes=10)

        if block_time:
            self.blocked_untils = datetime.now() + block_time
        
        return block_time
    
    def reset_failed_attempts(self) -> None:
        '''Сбрасывает счетчик неудачных попыток'''
        self.failed_attempts = 0
        self.blocked_untils = None