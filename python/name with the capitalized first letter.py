#при вводе имени пользователь возможно введет все с маленькой буквы
#по идее:
# 1. Нужно проверить какой символ первый (можно и пропустить)
# 2. Если это буква - сделать заглавной
# 3. Сохранить/вставить в значение
# 4. Посмотреть раздел про индексы в формате str
name5=input("Введите свое имя ");
ch=name5[0].capitalize();
#name5[0]=ch;	#условие выдает ошибку
print('Hello, ',name5,'!')