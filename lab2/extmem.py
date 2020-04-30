#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from random import randint

disk_dir = './disk/'  # 模拟磁盘所在的目录
num_per_blk, r_blk_num, s_blk_num = 7, 16, 32  # 每个磁盘块可以保存的元组数目，关系R的磁盘块数，关系S的磁盘块数


class Buffer:
    def __init__(self, all_blk_num: int):
        self.io_num = 0  # 磁盘IO次数
        self.all_blk_num = all_blk_num  # 缓冲区中可以保存的块数目
        self.free_blk_num = self.all_blk_num  # 缓冲区中可用的块数目
        self.data_occupy = [False] * self.all_blk_num  # False表示未被占用
        self.data = [] * self.all_blk_num  # 缓存中按块放置的数据

    def get_new_blk(self) -> int:
        index = self.all_blk_num - self.free_blk_num if self.free_blk_num else -1
        if self.free_blk_num:
            self.data_occupy[index] = True
            self.free_blk_num -= 1
        return index

    def free_blk(self) -> bool:
        flag = self.all_blk_num < self.free_blk_num
        if flag:
            self.free_blk_num += 1
            self.data_occupy[self.all_blk_num - self.free_blk_num] = False
        return flag

    def load_blk(self, addr: str) -> bool:
        blk_path = disk_dir + addr + '.blk'
        flag = self.all_blk_num < self.free_blk_num and os.path.exists(blk_path)
        index = self.all_blk_num - self.free_blk_num if flag else -1
        if flag:
            with open(blk_path) as f:
                self.data_occupy[index] = True
                self.data[index] = f.read()
                self.free_blk_num -= 1
                self.io_num += 1
        return flag

    def write_blk(self, addr):
        blk_path = disk_dir + addr + '.blk'
        with open(blk_path) as f:
            self.io_num += 1
            self.free_blk_num += 1
            self.data_occupy[self.all_blk_num - self.free_blk_num] = False
            f.write(self.data[self.all_blk_num - self.free_blk_num])
            return True


def drop_blk(addr: str) -> bool:  # 存在返回真，不存在返回假
    blk_path = disk_dir + addr + '.blk'
    blk_exists = os.path.exists(blk_path)
    if blk_exists:
        os.remove(blk_path)
    return blk_exists


def gene_data():
    all_data, item = [([], set(), r_blk_num * num_per_blk, 1, 40), ([], set(), s_blk_num * num_per_blk, 20, 60)], None
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
    all_data = [('r', r_blk_num, r_lst), ('s', s_blk_num, s_lst)]
    for data in all_data:  # 将关系实例写入模拟磁盘
        for idx in range(data[1]):
            with open('%s%s%d.blk' % (disk_dir, data[0], idx), 'w') as f:
                blk_data = ['%d %d' % item for item in data[2][idx * num_per_blk:(idx + 1) * num_per_blk]]
                f.write('\n'.join(blk_data))


if __name__ == '__main__':
    r, s = gene_data()  # 生成关系R和S的随机数据
    write_disk(r, s)  # 将数据写入模拟磁盘
