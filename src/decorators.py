import functools
from datetime import datetime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала и конца выполнения функции.

    Args:
        filename (str, optional): Имя файла для записи логов.
                                 Если None, логи выводятся в консоль.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Записываем информацию о запуске функции
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успешном выполнении
                log_message = f"{start_time} - {func_name} ok\n"

                # Записываем в файл или выводим в консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = (
                    f"{start_time} - {func_name} error: {type(e).__name__}: {str(e)}. " f"Inputs: {args}, {kwargs}\n"
                )

                # Записываем в файл или выводим в консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
