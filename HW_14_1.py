# 📌 На семинаре 13 был создан проект по работе с пользователями (имя, id, уровень)
# 📌 Напишите 3-7 тестов pytest (или unittest на ваш выбор) для данного проекта
# 📌 ОБЯЗАТЕЛЬНО! Используйте фикстуры

import json
from Sem_13_task_5 import Project
from Sem_13_task_4 import User
import pytest


@pytest.fixture
def load_list_person(filename="users.json"):
    list_person = Project.load(filename)
    list_person.set_admin(user_id="123", name="Sergio", level=1)
    return list_person


def test_add(load_list_person):
    assert load_list_person.add_user(user_id="235", name="Eugen", level=2) == "User added"


def test_login(load_list_person):
    assert load_list_person.login(user_id="963", name="Blade", level=3) == "Logging sucsess"


def test_admin(load_list_person):
    assert load_list_person.set_admin(user_id="519", name="Mary", level=4) == User(user_id="519", name="Mary", level=4)


if __name__ == '__main___':
    pytest.main()