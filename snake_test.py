import unittest
import snake
import tkinter


class MyTest(unittest.TestCase):

    def test_collision_left(self):
        tmp = tkinter.Frame()
        sn = snake.GameBoard(tmp)
        head = sn.find_withtag("head")
        sn.move(head, -11, 0)
        sn.checkCollisions()
        self.assertEqual(sn.gameOn, False)

    def test_collision_right(self):
        tmp = tkinter.Frame()
        sn = snake.GameBoard(tmp)
        head = sn.find_withtag("head")
        sn.move(head, 301, 0)
        sn.checkCollisions()
        self.assertEqual(sn.gameOn, False)

    def test_collision_up(self):
        tmp = tkinter.Frame()
        sn = snake.GameBoard(tmp)
        head = sn.find_withtag("head")
        sn.move(head, 0, -60)
        sn.checkCollisions()
        self.assertEqual(sn.gameOn, False)

    def test_collision_down(self):
        tmp = tkinter.Frame()
        sn = snake.GameBoard(tmp)
        head = sn.find_withtag("head")
        sn.move(head, 0, 301)
        sn.checkCollisions()
        self.assertEqual(sn.gameOn, False)


if __name__ == '__main__':
    unittest.main()
