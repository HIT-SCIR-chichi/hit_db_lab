# !/usr/bin/python
# -*- coding: utf-8 -*-
from extmem import disk_dir, tuple_num, blk_num2, blk_num1
from math import ceil, floor
import extmem

select_dir, project_dir = './disk/select/', './disk/project/'  # 关系选择、投影结果所在的磁盘目录
nlj_dir = './disk/join/nlj/'  # 关系连接磁盘目录
sort_temp_dir = './disk/join/sort/sort/'  # 归并排序连接算法中得到的已排序的磁盘文件目录
sort_res_dir = './disk/join/sort/res/'
hash_temp_dir = './disk/join/hash/hash/'
hash_res_dir = './disk/join/hash/res/'
blk_num = 8  # 缓冲区大小


def linear_search(buffer: extmem.Buffer):  # 关系选择：线性搜索R.A=40, S.C=60；并将结果写入到磁盘中
    two_items, buffer.io_num = [('r', extmem.blk_num1, [], 40), ('s', extmem.blk_num2, [], 60)], 0
    for item in two_items:
        for disk_idx in range(item[1]):  # item[1]表示关系占用的物理磁盘块数
            index = buffer.load_blk('%s%s%d.blk' % (disk_dir, item[0], disk_idx))  # 加载磁盘块内容到缓冲区中
            for data in buffer.data[index]:
                data0, data1 = map(int, data.split())
                if data0 == item[3]:
                    item[2].append((data0, data1))  # item[2]表示关系选择的结果
            buffer.free_blk(0)
    all_data = [('r', two_items[0][2]), ('s', two_items[1][2])]
    extmem.drop_blk_in_dir(select_dir)  # 删除文件夹下的所有模拟磁盘文件
    for data in all_data:
        for idx in range(ceil(len(data[1]) / extmem.tuple_num)):  # 写入结果所用的磁盘块数
            with open('%s%s%d.blk' % (select_dir, data[0], idx), 'w') as f:
                blk_data = ['%d %d' % item for item in data[1][idx * extmem.tuple_num:(idx + 1) * extmem.tuple_num]]
                f.write('\n'.join(blk_data))
    return two_items[0][2], two_items[1][2]


def relation_project(buffer: extmem.Buffer):  # 关系投影，对R的A属性进行投影并需要去重，并将结果写入到磁盘中
    r_res, buffer.io_num = [], 0  # 投影选择的结果
    for disk_idx in range(extmem.blk_num1):
        index = buffer.load_blk('%sr%d.blk' % (disk_dir, disk_idx))  # 加载磁盘块内容到缓冲区中
        for data in buffer.data[index]:
            if data.split()[0] not in r_res:
                r_res.append(data.split()[0])
        buffer.free_blk(0)
    extmem.drop_blk_in_dir(project_dir)  # 删除文件夹下的所有模拟磁盘文件
    for idx in range(ceil(len(r_res) / extmem.tuple_num / 2)):
        with open('%sr%d.blk' % (project_dir, idx), 'w')as f:
            f.write('\n'.join(r_res[idx * extmem.tuple_num * 2:(idx + 1) * extmem.tuple_num * 2]))


def nested_loop_join(buffer: extmem.Buffer):
    res, buffer.io_num = [], 0
    for outer_idx in range(extmem.blk_num1):  # 关系R做外层for循环内容
        outer_data = buffer.data[buffer.load_blk('%sr%d.blk' % (disk_dir, outer_idx))]  # 关系S做内层for循环内容
        for inner_idx in range(extmem.blk_num2):
            inner_data = buffer.data[buffer.load_blk('%ss%d.blk' % (disk_dir, inner_idx))]
            for outer_item in outer_data:
                r_a, r_b = outer_item.split()
                for inner_item in inner_data:
                    s_c, s_d = inner_item.split()
                    if r_a == s_c:
                        res.append(' '.join([r_a, r_b, s_c, s_d]))
            buffer.free_blk(1)
        buffer.free_blk(0)
    extmem.drop_blk_in_dir(nlj_dir)  # 删除文件夹下的所有模拟磁盘文件
    for idx in range(ceil(len(res) / floor(extmem.tuple_num / 2))):
        with open('%srs%d.blk' % (nlj_dir, idx), 'w') as f:
            f.write('\n'.join(res[idx * floor(extmem.tuple_num / 2):(idx + 1) * floor(extmem.tuple_num / 2)]))


def sort_merge_join(buffer: extmem.Buffer):
    res, buffer.io_num, all_data = [], 0, [('r', extmem.blk_num1), ('s', extmem.blk_num2)]
    for data in all_data:
        # 块内排序，由于缓冲区块数^2 < 关系R或S的磁盘块数，可以采用两阶段多路归并算法
        num = floor(data[1] / buffer.blk_num) + 1  # 将待排序磁盘块划分为num个集合
        if num >= buffer.blk_num:
            print('错误，两阶段归并不可行')
            return False
        for idx in range(num):  # 缓冲区的7块放置待排序数据，1块放置排序输出数据
            stop, blk_data = ((idx + 1) * (buffer.blk_num - 1)), []
            for idy in range(idx * (buffer.blk_num - 1), stop if stop < data[1] else data[1]):
                blk_data.extend(buffer.data[buffer.load_blk('%s%s%d.blk' % (disk_dir, data[0], idy))])  # 加载磁盘块内容到缓冲区中
            blk_data = sorted(blk_data, key=lambda item1: int(item1.split()[0]))
            for idy in range(int(len(blk_data) / extmem.tuple_num)):
                buffer.write_buffer(blk_data[idy * extmem.tuple_num:(idy + 1) * extmem.tuple_num],
                                    '%s%s%d.blk' % (extmem.disk_dir, data[0], idx * extmem.tuple_num + idy))
                buffer.free_blk(idy)

        # 块间排序
        count, blk_data, sorted_blk = 0, [[]] * num, []  # count表示已写入磁盘块数
        idx_lst = [idx * (buffer.blk_num - 1) for idx in range(num)]  # 保存num个索引，用于指向磁盘所在位置
        while True:
            for idx, item in enumerate(blk_data):
                if not item:
                    buffer.free_blk(idx)
                    if idx_lst[idx] < min((idx + 1) * (buffer.blk_num - 1), data[1]):  # 缓冲区待归并数据已被取空
                        blk_data[idx] = buffer.data[buffer.load_blk('%s%s%d.blk' % (disk_dir, data[0], idx_lst[idx]))]
                        idx_lst[idx] += 1
            flag = True if len(list(filter(None, blk_data))) else False
            if count == data[1] and not flag:  # 数据已经遍历完毕且缓冲区中无剩余数据
                break
            elif flag:  # 缓冲区中有剩余数据
                index, digit = 0, 1e4  # 找到最小的一个元素
                for idx in range(num):
                    if blk_data[idx] and int(blk_data[idx][0].split()[0]) < digit:
                        index, digit = idx, int(blk_data[idx][0].split()[0])
                sorted_blk.append(blk_data[index][0])  # 加入到输出缓冲区
                blk_data[index].pop(0)
                if len(sorted_blk) == extmem.tuple_num:
                    buffer.write_buffer(sorted_blk, '%s%s%d.blk' % (sort_temp_dir, data[0], count))
                    count, sorted_blk = count + 1, []
    # del idx, index, idy, idx_lst, num, stop, sorted_blk, item, digit, data, blk_data, flag, all_data

    # 执行连接算法
    extmem.drop_blk_in_dir(sort_res_dir)  # 删除文件夹下的所有模拟磁盘文件
    r_idx, s_idx, count, res = 0, 0, 0, []
    r_data = buffer.data[buffer.load_blk('%sr0.blk' % sort_temp_dir)]
    s_data = buffer.data[buffer.load_blk('%ss0.blk' % sort_temp_dir)]
    while r_idx < blk_num1 * tuple_num and s_idx < blk_num2 * tuple_num:
        data0, data2 = int(r_data[r_idx % tuple_num].split()[0]), int(s_data[s_idx % tuple_num].split()[0])
        if data0 == data2:  # 先记录原位置，然后向右滑动
            res.append('%s %s' % (r_data[r_idx % tuple_num], s_data[s_idx % tuple_num]))
            if len(res) == floor(tuple_num / 2):  # 结果缓冲区块已满
                buffer.write_buffer(res, '%srs%d.blk' % (sort_res_dir, count))
                res, count = [], count + 1
            idx_temp = s_idx + 1  # S变量临时向右滑动
            while idx_temp < blk_num2 * tuple_num:
                if not idx_temp % tuple_num:
                    buffer.free_blk(1)
                    s_data = buffer.data[buffer.load_blk('%ss%d.blk' % (sort_temp_dir, floor(idx_temp / tuple_num)))]
                if data0 == int(s_data[idx_temp % tuple_num].split()[0]):
                    res.append('%s %s' % (r_data[r_idx % tuple_num], s_data[idx_temp % tuple_num]))
                    idx_temp += 1  # 继续滑动
                    if len(res) == int(tuple_num / 2):  # 结果缓冲区块已满
                        buffer.write_buffer(res, '%srs%d.blk' % (sort_res_dir, count))
                        res, count = [], count + 1
                else:
                    break
            if floor(idx_temp / tuple_num) > floor(s_idx / tuple_num):  # 如果关系S临时滑动到了新的一块
                buffer.free_blk(1)
                s_data = buffer.data[buffer.load_blk('%ss%d.blk' % (sort_temp_dir, floor(s_idx / tuple_num)))]
            idx_temp = r_idx + 1  # 关系R临时向右滑动
            while idx_temp < blk_num1 * tuple_num:
                if not idx_temp % tuple_num:
                    buffer.free_blk(0)
                    r_data = buffer.data[buffer.load_blk('%sr%d.blk' % (sort_temp_dir, floor(idx_temp / tuple_num)))]
                if int(r_data[idx_temp % tuple_num].split()[0]) == data2:
                    res.append('%s %s' % (r_data[idx_temp % tuple_num], s_data[s_idx % tuple_num]))
                    idx_temp += 1
                    if len(res) == int(tuple_num / 2):
                        buffer.write_buffer(res, '%srs%d.blk' % (sort_res_dir, count))
                        res, count = [], count + 1
                else:
                    break
            if floor(idx_temp / tuple_num) > floor(r_idx / tuple_num):  # 如果关系R临时滑动到了新的一块
                buffer.free_blk(0)
                r_data = buffer.data[buffer.load_blk('%sr%d.blk' % (sort_temp_dir, floor(r_idx / tuple_num)))]
            r_idx, s_idx = r_idx + 1, s_idx + 1  # R和S向右滑动
            if not r_idx % tuple_num and r_idx < blk_num1 * tuple_num:
                buffer.free_blk(0)
                r_data = buffer.data[buffer.load_blk('%sr%d.blk' % (sort_temp_dir, floor(r_idx / tuple_num)))]
            if not s_idx % tuple_num and s_idx < blk_num2 * tuple_num:
                buffer.free_blk(1)
                s_data = buffer.data[buffer.load_blk('%ss%d.blk' % (sort_temp_dir, floor(s_idx / tuple_num)))]
        elif data0 > data2:
            s_idx += 1
            if not s_idx % tuple_num and s_idx < blk_num2 * tuple_num:
                buffer.free_blk(1)
                s_data = buffer.data[buffer.load_blk('%ss%d.blk' % (sort_temp_dir, floor(s_idx / tuple_num)))]
        else:
            r_idx += 1
            if not r_idx % tuple_num and r_idx < blk_num1 * tuple_num:
                buffer.free_blk(0)
                r_data = buffer.data[buffer.load_blk('%sr%d.blk' % (sort_temp_dir, floor(r_idx / tuple_num)))]
    if res:
        buffer.write_buffer(res, '%srs%d.blk' % (sort_res_dir, count))  # 将结果磁盘上的剩余数据写入磁盘


def hash_join(buffer: extmem.Buffer):
    buffer.__init__(blk_num)
    extmem.drop_blk_in_dir(hash_temp_dir)
    # 对关系R进行hash操作，将缓存中的blk_num-2块作为Hash桶，1块作为输出，1块保存另外1个关系
    all_data, hash_blk = [('r', blk_num1, [[] for idx in range(blk_num - 2)]),
                          ('s', blk_num2, [[] for idx in range(blk_num - 2)])], [[] for idx in range(blk_num - 2)]
    for item in all_data:
        for idx in range(item[1]):
            blk_data = buffer.data[buffer.load_blk('%s%s%d.blk' % (disk_dir, item[0], idx))]
            for data in blk_data:
                hash_idx = int(data.split()[0]) % (blk_num - 2)
                hash_blk[hash_idx].append(data)
                if len(hash_blk[hash_idx]) == tuple_num:  # HASH桶已满，需要输出
                    addr = '%s%s%d_%d.blk' % (hash_temp_dir, item[0], hash_idx, len(item[2][hash_idx]))
                    buffer.write_buffer(hash_blk[hash_idx], addr)
                    item[2][hash_idx].append(addr)
                    hash_blk[hash_idx] = []
            buffer.free_blk(0)
        for idx in range(blk_num - 2):
            if hash_blk[idx]:
                addr = '%s%s%d_%d.blk' % (hash_temp_dir, item[0], idx, len(item[2][idx]))
                buffer.write_buffer(hash_blk[idx], addr)
                item[2][idx].append(addr)
                hash_blk[idx] = []
    del hash_idx, hash_blk

    # 进行连接操作，将缓存中的blk_num-2块保存第i个桶的内容，1块作为输出，1块保存另外1个关系
    res, count, buffer.data_occupy = [], 0, [False] * blk_num
    extmem.drop_blk_in_dir(hash_res_dir)
    for idx in range(blk_num - 2):
        r_buffer_data, s_buffer_data, flag = [], [], False
        for addr in all_data[0][2][idx]:
            r_buffer_data.extend(buffer.data[buffer.load_blk(addr)])
            if ceil(len(r_buffer_data) / tuple_num) == 6:
                # todo 更加完善算法，考虑缓冲区大小不足的情况
                print('缓冲区大小不足，需要设计算法')
                return  # 执行分批次连接
        for addr in all_data[1][2][idx]:  # 将S的第i个hash桶内容逐个加入
            s_buffer_data = buffer.data[buffer.load_blk(addr)]
            for r_data in r_buffer_data:
                for s_data in s_buffer_data:
                    if r_data.split()[0] == s_data.split()[0]:
                        res.append('%s %s' % (r_data, s_data))
                        if len(res) == int(tuple_num / 2):
                            buffer.write_buffer(res, '%srs%d' % (hash_res_dir, count))
                            res = []
                            count += 1
            buffer.free_blk(ceil(len(r_buffer_data) / tuple_num))
        buffer.data_occupy = [False] * blk_num


def get_res():  # 直接计算自然连接的结果，用于测试其他算法的正确性
    all_data, res = [('r', blk_num1, []), ('s', blk_num2, [])], []
    for data in all_data:
        for idx in range(data[1]):
            with open('%s%s%d.blk' % (disk_dir, data[0], idx), 'r') as f:
                data[2].extend(list(map(str.split, f.read().split('\n'))))
    for lst1 in all_data[0][2]:
        for lst2 in all_data[1][2]:
            if lst1[0] == lst2[0]:
                res.append(' '.join(lst1 + lst2))
    return res


def main():
    buffer = extmem.Buffer(blk_num)
    linear_search(buffer)  # 关系选择，线性搜索
    print('关系选择的磁盘IO次数为：%d' % buffer.io_num)
    relation_project(buffer)  # 关系投影
    print('关系投影的磁盘IO次数为：%d' % buffer.io_num)
    nested_loop_join(buffer)
    print('nest-loop-join算法的磁盘IO次数为：%d' % buffer.io_num)
    sort_merge_join(buffer)
    print('sort-merge-join算法的磁盘IO次数为：%d' % buffer.io_num)
    hash_join(buffer)
    print('hash-join算法的磁盘IO次数为：%d' % buffer.io_num)
    # get_res()


if __name__ == '__main__':
    main()
