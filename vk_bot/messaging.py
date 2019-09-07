import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time
import keyboards
import pickle
from token_and_codes import token
from token_and_codes import codes

vk = vk_api.VkApi(token=token)


def write_msg(user_id, message, keyboard=None):
    vk.method('messages.send',
              {'user_id': user_id, 'random_id': time.gmtime(), 'message': message, 'keyboard': keyboard})


def messages_listening(users):
    longpoll = VkLongPoll(vk)

    for event in longpoll.listen():
        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:
            print(event.user_id, event.text)
            # Если оно имеет метку для меня( то есть бота)
            if event.to_me:
                request = event.text
                if request == 'Управление':
                    write_msg(event.user_id, 'Настройки сенсора', keyboards.options)
                elif request == 'Помощь':
                    text = """
                    Это краткое руководство по работе с устройством.
Для прикрепления устройства нажмите УПРАВЛЕНИЕ, далее ДОБАВИТЬ УСТРОЙСТВО и система предложит ввести код устройства.
Для открепления устройства нажмите УПРАВЛЕНИЕ, далее ОТКРЕПИТЬ уСТРОЙСТВО, Вам будет предложен список прикрепленных устройств, отправьте в ответ номер устройтва в списке, которое хотите открепить.
Сведения о нас можно запросить нажав О НАС.
При возникновении ошибок или отсутсвии клавиатуры управления просто отправьте боту сообщение с любой буквой.
                    """
                    write_msg(event.user_id, text, keyboards.menu)
                elif request == 'О нас':
                    write_msg(event.user_id, """
Это учебный проект студента группы ИКБО-02-16 Волкова Максима для проектного конкурса IOT Академии Samsung на базе университета РТУ.
                    """)
                elif request == 'Добавить устройство':
                    write_msg(event.user_id, 'Введите уникальный код устройства...')
                elif request == 'Открепить устройство':
                    try:
                        print(users[event.user_id])
                        if len(users[event.user_id]) > 0:
                            device_list = 'Выберите устройство для удаления\n'
                            for device in users[event.user_id]:
                                device_list += '{0} - {1}\n'.format(users[event.user_id].index(device) + 1, device)
                            write_msg(event.user_id, device_list)
                        else:
                            write_msg(event.user_id, 'У вас нет прикрепленных устройств', keyboards.menu)
                    except Exception as e:
                        print(e)
                        write_msg(event.user_id, 'Вы еще не прикрепили ни одного устройсвта', keyboards.menu)

                elif request.isdigit():
                    try:
                        del users[event.user_id][int(request) - 1]
                    except Exception as E:
                        print(E)
                        write_msg(event.user_id, 'Ошибка удаления!', keyboards.menu)
                    else:
                        write_msg(event.user_id, 'Устройство успешно откреплено!', keyboards.menu)
                        dbfile = open('users.db', 'wb')
                        pickle.dump(users, dbfile)
                        dbfile.close()
                # создание отношения между пользователем и устройством
                elif len(request) == 8:
                    if request in codes:
                        if event.user_id not in users:
                            users[event.user_id] = []
                        users[event.user_id].append(request)
                        write_msg(event.user_id, 'Привязка успешно выполнена!', keyboards.menu)
                        dbfile = open('users.db', 'wb')
                        pickle.dump(users, dbfile)
                        dbfile.close()
                    else:
                        write_msg(event.user_id, 'Неверный код!', keyboards.menu)
                else:
                    write_msg(event.user_id, 'Ошибка. Выберите комманду в меню.', keyboards.menu)
