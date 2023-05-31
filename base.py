"""
Режимы открытия файла
r - read - чтение (режим по-умолчанию)
w - write - запись (предыдущее содержимое файла удаляется)
a - append - ДОзапись
"""

filename = 'text.txt'

def write_to_db(user_id, query, name, photo):
    user_id = str(user_id)
    with open(filename, 'a') as file:
        file.write(user_id)
        file.write('\t', )
        file.write(str(query)) # TODO вот здесь исправила (неуверенна что так можно)
        file.write('\t')
        file.write(name)
        file.write('\t')
        file.write(photo)
        file.write('\n')



def get_user_from_db(my_user_id):
    with open(filename, 'r') as file:
        for line in file:
            user_id, query, name, photo = line.strip().split('\t')
            if str(my_user_id) == user_id:
                return {'user_id': user_id, 'query.data': query, 'name': name, 'photo': photo}


if __name__ == '__main__':
    write_to_db('1234', '10н', 'Юлиана', 'нет фото')