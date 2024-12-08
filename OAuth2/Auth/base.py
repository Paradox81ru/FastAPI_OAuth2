from abc import ABC, abstractmethod


class AbstractPwdContext(ABC):
    @abstractmethod
    def hash(self, password) -> str:
        """ Рассчитывает ХЭШ сумму указанного пароля """
        raise NotImplementedError()

    @abstractmethod
    def verify(self, password, _hash) -> bool:
        """
        Проверяет пароль
        :param password: строка пароля для проверки
        :param _hash: ХЭШ пароля, с которым производится проверка
        :return:
        """
        raise NotImplementedError