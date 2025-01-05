import sys 
import winreg
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.utils.config import Config


class ScreenLocker:
    '''Основной класс приложения'''

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.config = Config()
        self.main_window: Optional[MainWindow] = None

    def setup_aoutostart(self) -> None:
        '''Настройка автозапуска приложения'''
        key_path = r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        app_path = str(Path(sys.executable).resolve())

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0,
                                winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, 'ScreenLocker', 0, winreg.REG_SZ, app_path)
        except WindowsError as e:
            print(f'Ошибка при настройке автозапуска: {e}')

    def run(self) -> None:
        '''Запуск приложения'''
        if self.config.is_first_run():
            self.setup_autostart()
            self.config.set_first_run_completed()
            
        self.main_window = MainWindow(self.config)
        self.main_window.show()
        
        sys.exit(self.app.exec())


if __name__ == '__main__':
    app = ScreenLocker()
    app.run()