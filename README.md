**Игра "Змейка"**
=================
### **Постановка задачи**  
Разработать игру "Змейка"  
### **Use cases**  
Змейка состоит из нескольких звеньев. Нужно съесть как можно больше элементов. При каждом поедании длина змейки увеличивается, старый элемент исчезает, и случайно на поле появляется новый. При нажатии на клавиши изменения направления движения увеличивается скорость змейки. Текущая длина отображается в поле Счет. В левой колонке отображается текущий рейтинг по сравнению с другими играми. Показыввается рейтинг по последним 10 играм. Сложность заключается в том, что нельзя врезаться в стены и в себя. Если это происходит, то игра оканчивается, и всплавает окно, которое предлагает ввести имя для отображения в рейтинге результата игры. При изменении размера окна окно игрового поле изменяется соответственно, т.е. тоже либо расширяется, либо сужается. Есть кнопки+-, которыми можно увеличивать/уменьшать скорость.  
### **Управление**  
стрелки влево, вправо, вперед, назад - меняют направление движения
пробел - пауза
кнопка q - выход  
При нажатии на кнопку "Цвет фона" меняется цвет фона, при нажатии на "Цвет змейки" - меняется цвет змейки, при нажатии на "Цвет цели" - меняется цвет цели, при нажатии на "Скорость" - меняется скорость  
### **Тесты**  
Надо написать тесты для функции, проверяющей столкновения, протестировать ситуации столкновения со всеми стенами и самим с собой, тест, иметирующий нажатие поворотов, проверяющий правильность сортировки рейтинга и т.д.  
###  **Запуск**  
Игра: python3 snake.py  
Тесты: python3 -m unittest snake_test.py  
Можно установить колесо: перейти в директорию dict (cd dict), установить командой: python3 -m pip install snake-0.0.1-py3-none-any.whl и запустить командой python3 -m snake  
Можно собрать колесо командами python3 setup.py build потом python3 setup.py sdist bdist_wheel потом перейти в папку dist разархивировать его командой wheel unpack snake-0.0.1-py3-none-any.whl перейти в папке snake-0.0.1(cd snake-0.0.1) потом в папку snake(cd snake) и запустить python3 snake.py  
### **GUI**  
![GUI](https://github.com/ilpol/Python-project/blob/master/interfaceNew.png)


