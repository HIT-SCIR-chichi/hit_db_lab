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
        num, name, c_num = ui.stu_num.text(), ui.stu_name.text(), ui.class_num.text()
        if not num or not name or not c_num:
            QMessageBox.warning(self, '警告', '请输入学号、姓名与班号')
        elif not num.isdigit() or len(num) != 10 or not c_num.isdigit() or len(c_num) != 3:
            QMessageBox.warning(self, '警告', '学号为10位数字，班号为3位数字')
        else:
            query = 'select * from student where num=%s'
            if cur.execute(query, [num]):
                QMessageBox.warning(self, '插入异常', '该学号已存在，请重新输入')
            elif not cur.execute('select * from class where num=%s', [c_num]):
                QMessageBox.warning(self, '插入异常', '该班号在班级表中不存在，请尝试在班级表中插入对应条目')
            else:
                QMessageBox.information(self, '成功', '成功插入一条学生数据')
                query = 'insert into student(num,name,c_num) values (%s,%s,%s)'
                cur.execute(query, [num, name, c_num])
                con.commit()  # 修改数据时，需要commit操作

    def stu_delete(self):  # 删除学生信息
        num = ui.stu_num.text()
        if not num:
            QMessageBox.warning(self, '警告', '学号为空')
        elif not num.isdigit() or len(num) != 10:
            QMessageBox.warning(self, '警告', '学号只可为10位数字')
        else:
            query = 'select * from student where num=%s'
            if not cur.execute(query, [num]):
                QMessageBox.warning(self, "删除异常", "该学号不存在，请重新输入")
            elif cur.execute('select * from sc where snum =%s', [num]):
                QMessageBox.warning(self, "删除异常", "该学号正被选课表作为外键引用，请尝试删除对应条目")
            else:
                QMessageBox.information(self, '成功', '成功删除一条学生数据')
                query = 'delete from student where num=%s'
                cur.execute(query, [num])
                con.commit()  # 修改数据时，需要commit操作

    def course_insert(self):  # 新建学生信息
        num, name, t_num = ui.course_num.text(), ui.course_name.text(), ui.teacher_num.text()
        if not num or not name or not t_num:
            QMessageBox.warning(self, '警告', '请输入课程号、课程名和任课教师号')
        elif not num.isdigit() or len(num) != 3 or not num.isdigit() or len(t_num) != 10:
            QMessageBox.warning(self, '警告', '课程号为3位数字，教师号为10位数字')
        else:
            query = 'select * from course where num=%s'
            if cur.execute(query, [num]):
                QMessageBox.warning(self, '插入异常', '该课程号已存在，请重新输入')
            elif not cur.execute('select * from teacher where num=%s', [t_num]):
                QMessageBox.warning(self, '插入异常', '该教师号在教师表中不存在，请尝试在教师表中插入对应条目')
            else:
                QMessageBox.information(self, '成功', '成功插入一条课程数据')
                query = 'insert into course(num,name,t_num) values (%s,%s,%s)'
                cur.execute(query, [num, name, t_num])
                con.commit()  # 修改数据时，需要commit操作

    def course_delete(self):  # 删除学生信息
        num = ui.course_num.text()
        if not num:
            QMessageBox.warning(self, '警告', '课程号为空')
        elif not num.isdigit() or len(num) != 3:
            QMessageBox.warning(self, '警告', '课程号只可为3位数字')
        else:  # todo 考虑完整性约束
            query = 'select * from course where num=%s'
            if not cur.execute(query, [num]):
                QMessageBox.warning(self, "删除异常", "该课程号不存在，请重新输入")
            elif cur.execute('select * from sc where cnum=%s', [num]):
                QMessageBox.warning(self, "删除异常", "该课程号正被选课表作为外键引用，请尝试删除对应条目")
            else:
                QMessageBox.information(self, '成功', '成功删除一条课程数据')
                query = 'delete from course where num=%s'
                cur.execute(query, [num])
                con.commit()  # 修改数据时，需要commit操作

    def sc_insert(self):  # 新建信息
        s_num, c_num, grade = ui.sc_snum.text(), ui.sc_cnum.text(), ui.sc_grade.text()
        if not s_num or not c_num:
            QMessageBox.warning(self, '警告', '请输入学号课程号')
        elif not s_num.isdigit() or len(s_num) != 10 or not c_num.isdigit() or len(c_num) != 3:
            QMessageBox.warning(self, '警告', '学号为10为数字，课程号为3位数字')
        else:
            query = 'select * from sc where snum=%s and cnum=%s'
            if cur.execute(query, [s_num, c_num]):
                QMessageBox.warning(self, '插入异常', '该选课信息已存在，请重新输入')
            elif not cur.execute('select * from student where num=%s', [s_num]):
                QMessageBox.warning(self, '插入异常', '该学号在学生表中不存在，请尝试在学生表中插入对应条目')
            elif not cur.execute('select * from course where num=%s', [c_num]):
                QMessageBox.warning(self, '插入异常', '该课程号在课程表中不存在，请尝试在课程表中插入对应条目')
            else:
                QMessageBox.information(self, '成功', '成功插入一条学生数据')
                query = 'insert into sc(snum,cnum,grade) values (%s,%s,%s)'
                cur.execute(query, [s_num, c_num, grade])
                con.commit()  # 修改数据时，需要commit操作

    def sc_delete(self):  # 删除信息
        s_num, c_num = ui.sc_snum.text(), ui.sc_cnum.text()
        if not s_num or not c_num:
            QMessageBox.warning(self, '警告', '请输入学号课程号')
        elif not s_num.isdigit() or len(s_num) != 10 or not c_num.isdigit() or len(c_num) != 3:
            QMessageBox.warning(self, '警告', '学号为10为数字，课程号为3位数字')
        else:
            query = 'select * from sc where snum=%s and cnum=%s'
            if not cur.execute(query, [s_num, c_num]):
                QMessageBox.warning(self, "删除异常", "该选课信息不存在，请重新输入")
            else:
                QMessageBox.information(self, '成功', '成功删除一条选课信息')
                query = 'delete from sc where snum=%s and cnum=%s'
                cur.execute(query, [s_num, c_num])
                con.commit()  # 修改数据时，需要commit操作

    def get_name(self):
        c_count, res = int(ui.sc_stu_count.text()), []
        query = 'select student.name from student,sc where student.num = sc.snum group by student.num HAVING count(*) > %s'
        cur.execute(query, [c_count])
        for item in cur.fetchall():
            res.append(item[0])
        QMessageBox.information(self, '成功', ' '.join(res) if len(res) > 0 else '无结果')

    def get_name_by_cnum(self):
        c_num, res = ui.sc_stu_cnum.text(), []
        if not c_num:
            QMessageBox.warning(self, '警告', '请输入课程号')
        elif not c_num.isdigit() or len(c_num) != 3:
            QMessageBox.warning(self, '警告', '班号为3位数字')
        else:
            query = 'select name from student where num in (select snum from sc where cnum = %s)'
            cur.execute(query, [c_num])
            for item in cur.fetchall():
                res.append(item[0])
            QMessageBox.information(self, '成功', ' '.join(res) if len(res) > 0 else '无结果')

    def get_avg_grade(self):
        name, res = ui.sc_stu_sname.text(), []
        if not name:
            QMessageBox.warning(self, '警告', '请输入姓名')
        else:
            query = 'select snum, avg(grade) from sc where snum in (select num from student where name = %s)  and grade >= 60 group by snum'
            cur.execute(query, [name])
            for item in cur.fetchall():
                res.append(item[0] + '\t' + str(item[1]))
            QMessageBox.information(self, '成功', '\n'.join(res) if len(res) != 0 else '无结果')


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
