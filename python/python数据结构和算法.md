# python数据结构和算法

## 查找和排序
### 二分查找
二分查找（Binary Search）是一种在有序数组中查找特定元素的搜索算法。该算法通过将搜索范围逐步二等分，每次比较中间元素与目标元素，将搜索范围缩小一半，从而实现对目标元素的快速查找。

以下是二分查找的Python实现：

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

在上述代码中，`left` 和 `right` 分别表示搜索范围的左右边界。`mid` 是当前搜索范围的中间位置。如果中间元素等于目标元素，则返回其位置；如果中间元素小于目标元素，则将搜索范围调整为中间元素的右侧（即，`left = mid + 1`）；如果中间元素大于目标元素，则将搜索范围调整为中间元素的左侧（即，`right = mid - 1`）。如果找不到目标元素，则返回 -1。

二分查找的时间复杂度为 O(log n)，其中 n 是数组的长度。这是因为每次比较后，搜索范围都会减少一半。因此，二分查找可以在大型数据集上高效地找到目标元素。

> 注意，二分查找的前提是数组必须是有序的。如果数组未排序，你需要先对其进行排序，或者使用其他搜索算法。

### 冒泡排序
冒泡排序（Bubble Sort）是一种简单的排序算法。该算法重复地遍历需要排序的列表，比较每对相邻的项，如果它们的顺序错误就把它们交换过来。遍历列表的工作是重复地进行直到没有更多的交换需要，也就是说该列表已经排序完成。

以下是冒泡排序的Python实现：

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

在上述代码中，外层循环 `for i in range(n)` 用于控制遍历的次数，内层循环 `for j in range(0, n - i - 1)` 用于比较和交换元素。`if arr[j] > arr[j + 1]` 判断了当前元素是否大于下一个元素，如果是，则交换它们。

冒泡排序的时间复杂度为 O(n²)，其中 n 是列表的长度。这是因为冒泡排序需要遍历所有的元素，并对每个元素进行比较。因此，对于大型数据集，冒泡排序的效率并不高。

如果在一次完整的遍历过程中没有进行过任何交换，那么这个列表就已经是有序的，我们可以提前结束排序过程。这种改进后的冒泡排序被称为优化版冒泡排序。

以下是优化版冒泡排序的 Python 实现：

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        flag = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                flag = True
        if not flag:
            break
    return arr
```

在这个版本中，我们添加了一个标识 `flag` 来检查在遍历过程中是否进行了交换。如果在一次遍历过程中没有发生交换，`flag` 就会保持为 `False`，然后就会跳出排序的循环。

这种优化在对已经（或几乎）有序的列表进行排序时，能够显著提高冒泡排序的性能。但要注意的是，即使进行了这种优化，冒泡排序在最坏情况下的时间复杂度仍然是 O(n²)。

### 选择排序
选择排序（Selection Sort）是一种简单直观的比较排序算法。此算法的基本思想是：首先在未排序序列中找到最小（或最大）元素，存放到排序序列的起始位置，然后，再从剩余未排序元素中继续寻找最小（或最大）元素，然后放到已排序序列的末尾。以此类推，直到所有元素均排序完毕。

选择排序的性能在平均和最坏的情况下都是 O(n²)，其中 n 是列表的长度，因为无论列表的初始顺序如何，选择排序都会执行相同的操作次数。

以下是选择排序的Python实现：

```python
def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr
```

### 插入排序
插入排序（Insertion Sort）是一种简单直观的排序算法。它的工作方式是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。插入排序在实现上通常使用in-place排序（即只需用到O(1)的额外空间的排序），因此你可以将元素逐个插入到正确的位置。

以下是插入排序的 Python 实现：

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```
插入排序最好的情况时间复杂度是 O(n)，这会发生在输入数组已经是排序状态的时候。平均和最坏情况下的时间复杂度是 O(n^2)。尽管在最坏情况下它不如分治算法（如快速排序、归并排序）高效，但是在小规模数据或基本有序的数组上，插入排序是一个非常有效的算法。此外，由于其简单性，它通常比更高级的算法在常数较小的情况下表现得更好。

### 快速排序
快速排序（Quick Sort）是一种使用分治策略的高效排序算法。快速排序的基本思想是选择一个"基准"元素，然后将数组分为两部分，一部分包含所有小于基准的元素，另一部分包含所有大于或等于基准的元素。然后递归地对这两部分进行快速排序。

快速排序的Python实现1：
```python
def quick_sort(arr):
    if len(arr) < 2:
        return arr
    pivot = arr[0]
    less = [i for i in arr[1:] if i <= pivot] 
    greater = [i for i in arr[1:] if i > pivot]
    return quick_sort(less) + [pivot] + quick_sort(greater)
```

快速排序的Python实现2：
```python
# 定义排序函数
def quick_sort(arr, left, right):
    # 递归终止条件
    if left >= right:
    return
    # 设置基准位
    pivot = arr[left]
    # 左右指针  
    i = left 
    j = right
    while i < j:
    # 右指针从右向左移动  
    while i < j and arr[j] >= pivot:
        j -= 1
    # 左指针从左向右移动       
    while i < j and arr[i] <= pivot: 
        i += 1
    # 交换两个指针位置的元素      
    if i < j:
        arr[i], arr[j] = arr[j], arr[i]
    # 把基准元素放到正确位置      
    arr[left], arr[i] = arr[i], arr[left]
    # 递归调用排序函数
    quick_sort(arr, left, i-1)
    quick_sort(arr, i+1, right)
```

快速排序的Python实现3-非递归：
```python
def quick_sort_iterative(arr):
    stack = []
    # 初始范围是整个数组
    stack.append(0)
    stack.append(len(arr) - 1)

    # 栈不为空，继续排序
    while stack:
        end = stack.pop()
        start = stack.pop()
        pivot_index = partition(arr, start, end)

        # 如果有左子数组，将其起止位置入栈
        if pivot_index - 1 > start:
            stack.append(start)
            stack.append(pivot_index - 1)

        # 如果有右子数组，将其起止位置入栈
        if pivot_index + 1 < end:
            stack.append(pivot_index + 1)
            stack.append(end)

    return arr

def partition(arr, start, end):
    pivot = arr[start]
    low = start + 1
    high = end
    while True:
        while low <= high and arr[high] >= pivot:
            high = high - 1
        while low <= high and arr[low] <= pivot:
            low = low + 1
        if low <= high:
            arr[low], arr[high] = arr[high], arr[low]
        else:
            break
    arr[start], arr[high] = arr[high], arr[start]
    return high
```

快速排序在平均情况下的时间复杂度是 O(n log n)，其中 n 是数组的长度。这是因为每次分区操作，我们只需要遍历一次数组，然后递归处理两个分区。在最坏情况下，快速排序的时间复杂度是 O(n²)，但这种情况在实践中很少出现，可以通过合理地选择基准元素来避免。

### 堆排序
堆排序（Heap Sort）是一种基于比较的排序算法，使用二叉堆数据结构来帮助实现排序过程。二叉堆可以是一个最大堆或最小堆，在最大堆中，父节点的值总是大于或等于其子节点的值；在最小堆中，父节点的值总是小于或等于其子节点的值。

堆排序的步骤大致如下：

1. 构建最大堆（Build Max Heap）：将输入数组组织进一个最大堆中，即所有父节点的值都大于其子节点的值。
2. 交换堆顶元素与最后一个元素：将堆顶（最大值）和堆的最后一个元素交换，这样最大元素就放在了数组的最后一个位置。
3. 修复堆：由于堆的最后一个元素已经移动到了数组的开头，需要进行堆调整（Heapify）操作，确保剩余的堆仍然是最大堆。
4. 重复步骤2和3，直至堆中只剩下一个元素。

堆排序算法的时间复杂度是 O(n log n)，其中 n 是数组的长度。这是因为创建堆的时间复杂度是 O(n)，而进行 n 次调整堆的操作的时间复杂度是 O(n log n)。

堆排序的 Python 实现 1：
```python
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is greater than root
    if l < n and arr[i] < arr[l]:
        largest = l

    # See if right child of root exists and is greater than root
    if r < n and arr[largest] < arr[r]:
        largest = r

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap

        # Heapify the root.
        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr)

    # Build a maxheap.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)
```

```python
def heap_sort(arr):
    # 创建大根堆
    n = len(arr)
    for i in range(n//2-1, -1, -1):
        heapify(arr, i, n-1)
    print(arr)
        
    for i in range(n-1):
        arr[0], arr[n-i-1] = arr[n-i-1], arr[0]
        heapify(arr, 0, n-i-2)


def heapify(arr, cur, last):
    i = cur
    j = 2 * i + 1
    
    while j <= last:
        if j + 1 <= last and arr[j+1] > arr[j]:
            j = j + 1
        if arr[j] > arr[i]:
            arr[i], arr[j] = arr[j], arr[i]
            i = j
            j = 2 * i + 1
        else:
            break
```

在该实现中，`heapify` 函数用于将一个数组调整为堆结构，`heapSort` 函数是主要的排序函数，它首先构造最大堆，然后将堆顶元素（最大值）与堆的最后一个元素交换，再调整剩余部分的堆结构，直至堆中只剩下一个元素。

堆排序的 Python 实现 2：
```python

```

### 归并排序