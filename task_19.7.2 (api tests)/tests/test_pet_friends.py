# task 19.7.2 (api tests)

from api import PetFriends
from settings import valid_email, valid_email1, valid_email2, \
    valid_password, valid_password1, valid_password2
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Ron', animal_type='British', age='2', pet_photo='images/01.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Rin', animal_type='Котэ', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Ron", "British", "2", "images/01.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()



# added tests:

def test_add_new_pet_without_photo(name='Ron', animal_type='British', age='2', pet_photo=''):
    """проверяем возможность добавления нового питомца без фото мотодом 'post':/api/create_pet_simple"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet(pet_photo='images/01.jpg'):
    """проверяем возможность добавления фото питомцу мотодом 'post':/api/pets/set_photo/{pet_id}"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200


def test_successful_update_self_pet_info_empty(name=' ', animal_type=' ', age=' '):
    """проверяем возможность обновления информации о питомце пустыми значениями мотодом 'put':/api/pets/{pet_id}"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_5_pets(name='Ron', animal_type='British', age='2', pet_photo='images/01.jpg'):
    """проверяем возможность добавления 5-и новых питомцев мотодом 'post':/api/create_pet_simple"""

    for i in range(5):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        assert status == 200
        assert result['name'] == name


def test_get_api_key_for_not_valid_email(email=valid_email1, password=valid_password1):
    """проверяем возможность авторизации на сайте с невалидным логином 'valid_email1' -> settings.py
    метод 'get'/:"""

    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_not_valid_password(email=valid_email2, password=valid_password2):
    """проверяем возможность авторизации на сайте с невалидным паролем 'valid_password2' -> settings.py
    метод 'get'/:"""

    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' not in result


def test_add_invaild_photo_of_pet(pet_photo='images/02.png'):
    """проверяем возможность добавления валидного фото формата .PNG питомцу мотодом
    'post':/api/pets/set_photo/{pet_id},"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200


def test_successful_update_self_pet_info_maximum_values(name='10values' * 100, animal_type='10values' * 100,
                                                        age='10values' * 100):
    """проверяем возможность обновления информации о питомце строками == 100 символов, мотодом 'get'/:/api/pets/{pet_id}"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_update_self_pet_info_emoji_values(name='😻', animal_type='😹', age='🕺'):
    """проверяем возможность обновления информации о питомце строками == Emoji, мотодом 'get'/:/api/pets/{pet_id}"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_delete_self_all_pets():
    """удаляем всех питомцев мотодом 'delete'/:/api/pets/{pet_id}"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    while len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert pet_id not in my_pets.values()

    assert status == 200
    assert len(my_pets['pets']) == 0
