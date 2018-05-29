# coding: utf-8
# @Time    : 2018/5/28 23:45
# @Author  : xavier


def bubble_sort(li):
    # 冒泡排序
    # 时间复杂度O(n2)
    for j in range(len(li)-1):
        for i in range(1, len(li)):
            if li[i] > li[i-1]:
                li[i], li[i-1] = li[i-1], li[i]
    return li


def insert_sort(li):
    # 插入排序
    # 时间复杂度O(n2)
    for i in range(1,len(li)):
        tmp = li[i]
        j = i - 1
        while j >= 0 and tmp < li[j]: # 找到一个合适的位置插进去
            li[j+1] = li[j]
            j -= 1
        li[j+1] = tmp
    return li


def select_sort(li):
    # 选择排序
    # 时间复杂度O(n2)
    for i in range(len(li)-1):
        min_loc = i         # 假设当前最小的值的索引就是i
        for j in range(i+1,len(li)):
            if li[j] < li[min_loc]:
                min_loc = j
        if min_loc != i:   # min_loc 值如果发生过交换，表示最小的值的下标不是i,而是min_loc
            li[i],li[min_loc] = li[min_loc],li[i]

    return li


def partition(data, left, right): # 左右分别指向两端的元素
    tmp = data[left]                # 把左边第一个元素赋值给tmp,此时left指向空
    while left < right:             # 左右两个指针不重合，就继续
        while left < right and data[right] >= tmp:  # right指向的元素大于tmp,则不交换
            right -= 1                      # right 向左移动一位
        data[left] = data[right]            # 如果right指向的元素小于tmp，就放到左边现在为空的位置
        while left < right and data[left] <= tmp:   # 如果left指向的元素小于tmp,则不交换
            left += 1                       # left向右移动一位
        data[right] = data[left]            # 如果left指向的元素大于tmp,就交换到右边
    data[left] = tmp            # 最后把最开始拿出来的那个值，放到左右重合的那个位置
    return left                 # 最后返回这个位置


#  写好归位函数后，就可以递归调用这个函数，实现排序
def quick_sort(data, left, right):
    # 快速排序
    # 时间复杂度O(nlogn)
    if left < right:
        mid = partition(data, left, right)  # 找到指定元素的位置
        quick_sort(data, left, mid - 1)     # 对左边元素排序
        quick_sort(data, mid + 1, right)    # 对右边元素排序
    return data


def merge(li, left, mid, right):
    # 一次归并过程，把从mid分开的两个有序列表合并成一个有序列表
    i = left
    j = mid + 1
    ltmp = []
    # 两个列表的元素依次比较，按从大到小的顺序放到一个临时的空列表中
    while i <= mid and j <= right:
        if li[i] < li[j]:
            ltmp.append(li[i])
            i += 1
        else:
            ltmp.append(li[j])
            j += 1

    # 如果两个列表并不是平均分的，就会存在有元素没有加入到临时列表的情况，所以再判断一下
    while i<= mid:
        ltmp.append(li[i])
        i += 1
    while j <= right:
        ltmp.append(li[j])
        j += 1
    li[left:right+1] = ltmp
    return li


def _merge_sort(li, left, right):
    # 细分到一个列表中只有一个元素的情况，对每一次都调用merge函数变成有序的列表
    if left < right:
        mid = (left+right)//2
        _merge_sort(li, left, mid)
        _merge_sort(li, mid+1, right)
        merge(li, left, mid, right)
    return li

def merge_sort(li):
    # 归并排序
    return(_merge_sort(li, 0, len(li)-1))

if __name__ == '__main__':
    print insert_sort([1,4,5,73,2,7,95,3,2,56])