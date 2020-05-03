#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from random import randint

disk_dir = './disk/relation/'  # 模拟磁盘所在的目录
tuple_num, blk_num1, blk_num2 = 7, 16, 32  # 每个磁盘块可以保存的元组数目，关系R的磁盘块数，关系S的磁盘块数


class Buffer:
    def __init__(self, blk_num: int = 8):
        self.io_num = 0  # 磁盘IO次数
        self.blk_num = blk_num  # 缓冲区中可以保存的块数目
        self.free_blk_num = self.blk_num  # 缓冲区中可用的块数目
        self.data_occupy = [False] * self.blk_num  # False表示未被占用
        self.data = [[]] * self.blk_num  # 缓存中按块放置的数据，数据为str类型

    def get_free_blk(self) -> int:
        for idx, flag in enumerate(self.data_occupy):
            if not flag:
                self.data_occupy[idx] = True
                self.free_blk_num -= 1
                return idx
        return -1

    def free_blk(self, index) -> bool:  # 释放缓冲区的一个磁盘块
        flag = self.data_occupy[index]
        if flag:
            self.free_blk_num += 1
            self.data_occupy[index] = False
        return flag

    def load_blk(self, addr: str) -> int:  # 加载磁盘块到缓冲区中，输入参数形如'./disk/relation/r15.blk'
        index = self.get_free_blk()
        if index != -1:
            with open(addr) as f:
                self.data_occupy[index] = True
                self.data[index] = f.read().split('\n')
                self.io_num += 1
        return index

    def write_blk(self, addr, index):  # 将缓冲区中数据写入磁盘块
        with open(addr, 'w') as f:
            self.io_num += 1
            self.free_blk_num += 1
            self.data_occupy[index] = False
            f.write('\n'.join(self.data[index]))
            return True

    def write_buffer(self, data_lst: list, addr):  # 将CPU处理后的数据暂存入缓冲区，再存入磁盘
        index = self.get_free_blk()
        if index != -1:
            self.data[index] = data_lst
            self.write_blk(addr, index)
        return index != -1


def drop_blk(addr: str) -> bool:  # 存在返回真，不存在返回假
    blk_path = disk_dir + addr + '.blk'
    blk_exists = os.path.exists(blk_path)
    if blk_exists:
        os.remove(blk_path)
    return blk_exists


def drop_blk_in_dir(file_dir: str):
    for file in os.listdir(file_dir):
        os.remove(file_dir + file)


def gene_data():
    drop_blk_in_dir(disk_dir)
    all_data, item = [([], set(), blk_num1 * tuple_num, 1, 40), ([], set(), blk_num2 * tuple_num, 20, 60)], None
    for data in all_data:
        for idx in range(data[2]):  # data[2]保存的是关系元组数目
            while True:
                item = (randint(data[3], data[4]), randint(1, 1000))  # data[3]和data[4]保存属性A和C的值域上下界
                if item not in data[1]:  # data[1]是一个集合，用于生成唯一的元组
                    break
            data[0].append(item)  # data[0]用于保存最终结果
            data[1].add(item)
    return all_data[0][0], all_data[1][0]


def write_disk(r_lst: list, s_lst: list):
    all_data = [('r', blk_num1, r_lst), ('s', blk_num2, s_lst)]
    for data in all_data:  # 将关系实例写入模拟磁盘
        for idx in range(data[1]):
            with open('%s%s%d.blk' % (disk_dir, data[0], idx), 'w') as f:
                blk_data = ['%d %d' % item for item in data[2][idx * tuple_num:(idx + 1) * tuple_num]]
                f.write('\n'.join(blk_data))


if __name__ == '__main__':
    r, s = gene_data()  # 生成关系R和S的随机数据
    write_disk(r, s)  # 将数据写入模拟磁盘
