# import json
# import os
# import logging

# logger = logging.getLogger(__name__)
# FILE_NAME = "data.json"

# def load_data():
#     if not os.path.exists(FILE_NAME):
#         return []
#     try:
#         with open(FILE_NAME, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except json.JSONDecodeError:
#         logger.warning(f"Файл {FILE_NAME} повреждён, возвращаю пустой список")
#         return []

# def save_data(data):
#     with open(FILE_NAME, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

# def add_fighter(fighter):
#     if not isinstance(fighter, dict):
#         logger.error("Fighter должен быть словарём!")
#         return
#     required_keys = {"name", "style", "age"}
#     if not required_keys.issubset(fighter.keys()):
#         logger.error(f"Fighter должен содержать ключи {required_keys}")
#         return
#     data = load_data()
#     data.append(fighter)
#     save_data(data)
#     logger.info(f"Боец {fighter['name']} добавлен")

# def delete_fighter(name):
#     data = load_data()
#     original_len = len(data)
#     data = [f for f in data if f.get("name", "").lower() != name.lower()]
#     if len(data) < original_len:
#         save_data(data)
#         logger.info(f"Боец {name} удалён")
#     else:
#         logger.warning(f"Боец {name} не найден")

# def get_all_fighters():
#     return load_data()

import json
import os
import logging

logger = logging.getLogger(__name__)
FILE_NAME = "data.json"

def load_data():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.warning(f"Файл {FILE_NAME} пошкоджено, повертаю порожній список")
        return []

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_fighter(fighter):
    if not isinstance(fighter, dict):
        logger.error("Боєць має бути словником!")
        return
    required_keys = {"name", "style", "age"}
    if not required_keys.issubset(fighter.keys()):
        logger.error(f"Боєць має містити ключі {required_keys}")
        return
    data = load_data()
    data.append(fighter)
    save_data(data)
    logger.info(f"Бійця {fighter['name']} додано")

def delete_fighter(name):
    data = load_data()
    original_len = len(data)
    data = [f for f in data if f.get("name", "").lower() != name.lower()]
    if len(data) < original_len:
        save_data(data)
        logger.info(f"Бійця {name} видалено")
    else:
        logger.warning(f"Бійця {name} не знайдено")

def get_all_fighters():
    return load_data()