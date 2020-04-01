#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from lab1 import gui
import pymysql
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./lab1/src/system.png'))

    def stu_insert(self):  # 新建学生信息
        num, name = ui.stu_num.text(), ui.stu_name.text()
        if not num or not name:
            QMessageBox.warning(self, '警告', '学号或姓名为空')
        elif not num.isdigit() or len(num) != 10:
            QMessageBox.warning(self, '警告', '只可为10位数字')
        else:  # todo 考虑完整性约束
            query = 'select * from student where num=%s'
            if cur.execute(query, [num]):
                QMessageBox.warning(self, '学号已存在', '该学号已存在，请重新输入')
            else:
                QMessageBox.information(self, '操作成功', '成功插入一条学生数据')
                query = 'insert into student(num,name) values (%s,%s)'
                cur.execute(query, [num, name])
                con.commit()  # 修改数据时，需要commit操作

    def stu_delete(self):  # 删除学生信息
        num = ui.stu_num.text()
        if not num:
            QMessageBox.warning(self, '警告', '学号或姓名为空')
        elif not num.isdigit() or len(num) != 10:
            QMessageBox.warning(self, '警告', '只可为10位数字')
        else:  # todo 考虑完整性约束
            query = 'select * from student where num=%s'
            if not cur.execute(query, [num]):
                QMessageBox.warning(self, "学号不存在", "该学号不存在，请重新输入")
            else:
                QMessageBox.information(self, '操作成功', '成功删除一条学生数据')
                query = 'delete from student where num=%s'
                cur.execute(query, [num])
                con.commit()  # 修改数据时，需要commit操作

    def get_grade(self):  # 删除学生信息
        s_num = ui.sc_snum.text()
        c_num = ui.sc_cnum.text()
        if not s_num or not c_num:
            QMessageBox.warning(self, '警告', '学号或课程号为空')
        elif not s_num.isdigit() or len(s_num) != 10 or not c_num.isdigit():
            QMessageBox.warning(self, '警告', '学号只可为10位数字，课程号只可为数字')
        else:
            query = 'select student.name, grade.grade from student,grade where snum=%s and cnum=%s'
            if not cur.execute(query, [s_num, c_num]):
                QMessageBox.Warning(self, '操作失败', '无法找到该选课信息')
            else:
                res = cur.fetchone()
                print(res)


if __name__ == "__main__":
    con = pymysql.connect(host='localhost', port=3306, user='root', password='123456', charset='utf8',
                          database='teaching_management_system')  # 连接数据库
    cur = con.cursor()  # 执行sql语句的游标

    app = QApplication(sys.argv)

    main_win = MainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(main_win)

    main_win.show()
    sys.exit(app.exec_())
