**Игра "Змейка"**
=================
### **Постановка задачи**  
Разработать игру "Змейка"  
### **Use cases**  
Змейка состоит из нескольких звеньев. Нужно съесть как можно больше элементов. При каждом поедании длина змейки увеличивается, старый элемент исчезает, и случайно на поле появляется новый. Текущая длина отображается в поле Счет. Сложность заключается в том, что нельзя врезаться в стены и в себя. Если это происходит, то игра оканчивается, и предлагается начать новую или выйти. Также показывается текущий рейтинг по сравнению с другими играми, можно хранить, например, 10 последних игр. Со временем или в зависимости от длины скорость движения змейки увеличивается. Также есть кнопки+-, которыми можно увеличивать/уменьшать скорость.  
### **Управление**  
стрелки влево, вправо, вперед, назад - меняют направление движения
пробел - пауза
кнопка q - выход  
При нажатии на кнопку "Цвет фона" меняется цвет фона, при нажатии на "Цвет змейки" - меняется цвет змейки, при нажатии на "Цвет цели" - меняется цвет цели, при нажатии на "Скорость" - меняется скорость  
### **Тесты**  
Надо написать тесты для функции, проверяющей столкновения, протестировать ситуации столкновения со всеми стенами и самим с собой, тест, иметирующий нажатие поворотов, проверяющий правильность сортировки рейтинга и т.д.  
### **GUI**  
![GUI](https://github.com/ilpol/Python-project/blob/master/interface.png)


