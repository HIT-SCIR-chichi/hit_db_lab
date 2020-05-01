# !/usr/bin/python
# -*- coding: utf-8 -*-

import extmem
from math import ceil

relation_selection_dir = './disk/relation_selection/'  # 关系选择结果所在的磁盘目录


def linear_search(buffer: extmem.Buffer):  # 关系选择：线性搜索R.A=40, S.C=60；并将结果写入到磁盘中
    two_items = [('r', extmem.r_blk_num, [], 40), ('s', extmem.s_blk_num, [], 60)]
    for item in two_items:
        for disk_idx in range(item[1]):  # item[1]表示关系占用的物理磁盘块数
            index = buffer.load_blk('%s%d' % (item[0], disk_idx))  # 加载磁盘块内容到缓冲区中
            for data in buffer.data[index]:
                data0, data1 = map(int, data.split())
                if data0 == item[3]:
                    item[2].append((data0, data1))  # item[2]表示关系选择的结果
            buffer.free_blk()
    all_data = [('r', two_items[0][2]), ('s', two_items[1][2])]
    for data in all_data:
        for idx in range(ceil(len(data[1]) / extmem.num_per_blk)):  # 写入结果所用的磁盘块数
            with open('%s%s%d.blk' % (relation_selection_dir, data[0], idx), 'w') as f:
                blk_data = ['%d %d' % item for item in data[1][idx * extmem.num_per_blk:(idx + 1) * extmem.num_per_blk]]
                f.write('\n'.join(blk_data))
    return two_items[0][2], two_items[1][2]


def nested_loop_join():
    pass


def hash_join():
    pass


def sort_merge_join():
    pass


def main():
    buffer = extmem.Buffer(all_blk_num=8)
    linear_search(buffer)  # 关系选择，线性搜索
    print('关系选择阶段的磁盘IO次数为：%d' % buffer.io_num)


if __name__ == '__main__':
    main()
