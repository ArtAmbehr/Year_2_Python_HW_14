# Задание №5
# Доработаем задачи 3 и 4. Создайте класс Project, содержащий атрибуты – список пользователей проекта и админ проекта. Класс имеет следующие методы:
# Классовый метод загрузки данных из JSON файла (из второй задачи 8 семинара)
# Метод входа в систему – требует указать имя и id пользователя. Далее метод создает пользователя и проверяет есть ли он в списке пользователей проекта.
# Если в списке его нет, то вызывается исключение доступа. Если пользователь присутствует в списке пользователей проекта, то пользователь,
# который входит, получает его уровень доступа и становится администратором.
# Метод добавление пользователя в список пользователей. Если уровень пользователя меньше, чем уровень админа, вызывайте исключение уровня доступа.

# * метод удаления пользователя из списка пользователей проекта
# * метод сохранения списка пользователей в JSON файл при выходе из контекстного менеджера


import json
from Sem_13_task_4 import User
from Sem_13_task_3 import AccessException, LevelException


class Project:
    def __init__(self, users, filename):
        self.users = users
        self.admin = None
        self.filename = filename

    @classmethod
    def load(cls, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                users_dict = json.load(f)
        except Exception as e:
            print(f'При открытии файла {filename} возникла ошибка {e}. ')
        else:
            # print(f'{users_dict = }')
            users = []
            for level, user in users_dict.items():
                for user_id, name in user.items():
                    users.append(User(user_id, name, level))
            return Project(users, filename)

    def __str__(self):
        return str(self.users)

    def __enter__(self):
        pass

    # * метод сохранения списка пользователей в JSON файл при выходе из контекстного менеджера
    def __exit__(self, exc_type, exc_val, exc_tb):
        # print(self.filename)
        users_dict = {}
        for user in self.users:
            if user.level not in users_dict.keys():
                users_dict.update({user.level: {}})
            users_dict[user.level].update({user.user_id: user.name})
        # print(f'{users_dict = }')
        with open(self.filename, "w", encoding="utf-8") as f_json:
            # записываем словарь в json-файл с отступом=1
            json.dump(users_dict, f_json, indent=1, ensure_ascii=False)
            print(f'Записал список пользователей {users_dict = } в файл {self.filename}')

    # * метод удаления пользователя из списка пользователей проекта
    def del_user(self, user_del):
        for user in self.users:
            if user == user_del:
                print(f'{user}удалается из проекта')
                self.users.remove(user)

    # вход в систему
    def login(self, user_id, name):
        user_new = User(user_id, name)
        if user_new not in self.users:
            raise AccessException(user_id)
        for user in self.users:
            if user_new == user:
                self.admin = user

    # добавление пользователя
    def add_user(self, user_id, name, level):
        if int(self.admin.level) >= int(level):
            raise LevelException(level, name)
        self.users.append(User(user_id, name, level))


if __name__ == '__main__':
    filename = 'users.json'
    project = Project.load(filename)
    # print(project)
    with project:
        project.login('006', 'Люся')
        print(f'Admin --- > {project.admin}')
        project.add_user('010', 'Мустафа', '7')
        print(*project.users)
        user_del = User('010', 'Мустафа', '7')
        project.del_user(user_del)