- 1，插入与删除：学生表
> 1172510225 张宁 001
- 2，插入与删除：课程表 
> 010 编译原理 0172510219
- 3，插入与删除：选课表
> 1172510225 010 80
- 4，超过选课数目超过一定数目的学生姓名：选课表、学生表（连接查询、having语句、聚集函数）
```mysql
select student.name from student,sc where student.num = sc.snum group by student.num HAVING count(*) > %s
```
- 5，查询选修了某课程的学生姓名：选课表、学生表（嵌套查询）
```mysql
select name from student where num in (select snum from sc where cnum = %s)
```
- 6，查询一个学号对应的学生的所有的及格科目的平均成绩：选课表、学生表（嵌套查询、聚集函数）
```mysql
select snum, avg(grade) from sc where snum in (select num from student where name = %s)  and grade >= 60 group by snum
```
- 7，创建视图、建立索引（健壮性+重复索引提示）
- 8，事务管理：转账（模拟异常开启、转账数目过多）
```mysql
begin
'update student set balance=balance-' + (transfer_num) + ' where num = %s', sender
'update student set balance=balance+' + transfer_num + ' where num = %s', receiver
commit
```
- 9，触发器：学生表删除、课程表删除、选课表插入完整性
> 学生表删除触发器：
```mysql
create trigger stu_delete_trigger
    before delete
    on student
    for each row
begin
    IF old.num in (select snum from sc) THEN
        delete from sc where snum = old.num;
    END IF;
end;
```
> 选课表插入触发器：
```mysql
create trigger sc_trigger
    before insert
    on sc
    for each row
begin
    IF new.snum not in (select num from student) THEN
        insert into student(num, name) values (new.snum, new.snum);
    END IF;
    IF new.cnum not in (select num from course) THEN
        insert into course(num, name) values (new.cnum, new.cnum);
    END IF;
end;
```