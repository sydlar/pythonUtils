# -*-coding:utf8-*-
"""
Modul som kan være nyttig når man skal demonstrere ulike
sorteringsalgoritmer.
"""

def swapper(xs):
    def swap(i,j):
        tmp = xs[i]
        xs[i] = xs[j]
        xs[j] = tmp

    return swap

def bubbleSortPass(xs,n=None):
    xs = xs[:]
    n = n or len(xs)
    
    swap = swapper(xs)

    for i in range(1,n):
        if xs[i] < xs[i-1]:
            swap(i,i-1)
    return xs


def insertionSortPass(xs, n = None):
    xs = xs[:]
    n = n or 0

    swap = swapper(xs)

    for i in reversed(range(1,n)):
        if (xs[i] < xs[i-1]):
            swap(i,i-1)
        else:
            break
    return xs


def selectionSortPass(xs,n=None):
    xs = xs[:]
    n = n or 0
    m = len(xs)

    swap = swapper(xs)

    minimum = n
    for i in range(n+1,m):
        if xs[i] < xs[minimum]:
            minimum = i

    swap(minimum,n)
    return xs


def quickSortPass(xs,pivots=None):
    pivots = pivots or 0
    return


class BubbleSort(object):

    def __init__(self,xs):
        self.xs = xs[:]
        self.n = len(self.xs)
        self.swap = swapper(self.xs)
        self.lastSwap = self.n
        
        self.name ="Bubble sort"

    def __iter__(self):
        return BubbleSort(self.xs)

    def step(self):
        rng = range(1,self.lastSwap)
        self.lastSwap=0
        for i in rng:
            if self.xs[i] < self.xs[i-1]:
                self.swap(i,i-1)
                self.lastSwap = i

    def next(self):
        if self.lastSwap <= 1:
            raise StopIteration
        self.step()
        return self.xs[:]

class SelectionSort(object):

    def __init__(self,xs):
        self.xs = xs[:]
        self.n = len(self.xs)
        self.swap = swapper(self.xs)
        self.current = 0
        
        self.name ="Selection sort"

    def __iter__(self):
        return SelectionSort(self.xs)

    def step(self):
        rng = range(self.current,self.n)
        minimum = self.current
        for i in rng:
            if self.xs[minimum] > self.xs[i]:
                minimum = i
        if (minimum != self.current):
            self.swap(minimum,self.current)
        self.current+=1

    def next(self):
        if self.current == self.n:
            raise StopIteration
        self.step()
        return self.xs[:]

class InsertionSort(object):

    def __init__(self,xs):
        self.xs = xs[:]
        self.n = len(self.xs)
        self.swap = swapper(self.xs)
        self.current = 1
        self.name ="Insertion sort"

    def __iter__(self):
        return InsertionSort(self.xs)

    def step(self):
        i = self.current 
        currentItem = self.xs[self.current]
        while(i > 0 and currentItem < self.xs[i-1]):
            self.xs[i] = self.xs[i-1]
            i-=1
        self.xs[i] = currentItem
        self.current+=1

    def next(self):
        if not self.current < self.n:
            raise StopIteration
        self.step()
        return self.xs[:]

class QuickSort(object):
    def __init__(self,xs):
        self.xs = xs[:]
        self.swap = swapper(self.xs)
        self.sortableSegments = [(0,len(self.xs))]
        self.finished = False
        
        self.name ="Quicksort"

    def __iter__(self):
        return QuickSort(self.xs)

    def step(self):
        def splitUp(lo,hi):
            segment = self.xs[lo:hi]
            pivot = segment[0]
            first = [x for x in segment if x < pivot]
            last = [x for x in segment if x > pivot]
            middle = [x for x in segment if x == pivot]

            self.xs[lo:hi] = first+middle+last
            return lo+len(first),hi-len(last)

        self.finished = True
        newSortableSegments = []
        for lo,hi in self.sortableSegments:
            a,b = splitUp(lo,hi)
            if (lo < a-1):
                newSortableSegments.append((lo,a))
            if (b < hi-1):
                newSortableSegments.append((b,hi))
        self.sortableSegments = newSortableSegments

    def next(self):
        if not self.sortableSegments: raise StopIteration
        self.step()
        return self.xs[:]

class MergeSort(object):
    def __init__(self,xs):
        self.xs = xs[:]
        self.n = len(self.xs)
        self.swap = swapper(self.xs)
        self.level = 0

        self.name = "Merge sort"

    def __iter__(self):
        return MergeSort(self.xs)

    def step(self):
        level = self.level

        def loMidHi(i):
            lo = 2*i*2**level
            mid = lo + 2**level
            mid = mid if mid < self.n else self.n
            hi = mid + 2**level
            hi = hi if hi < self.n else self.n
            return lo,mid,hi

        def merge(lo,mid,hi):
            newData = []
            l = lo
            r = mid
            while l < mid or r < hi:
                if (r == hi):
                    newData.extend(self.xs[l:mid])
                    l = mid
                elif (l == mid):
                    newData.extend(self.xs[r:hi])
                    r = hi
                elif (self.xs[l] < self.xs[r]):
                    newData.append(self.xs[l])
                    l+=1
                else:
                    newData.append(self.xs[r])
                    r+=1
            self.xs[lo:hi] = newData
            


        for lo,mid,hi in (loMidHi(i) for i in range(int(self.n/2**(level+1))+1)):
            merge(lo,mid,hi)

        self.level+=1
    
    def next(self):
        if 2**self.level >= self.n: raise StopIteration
        self.step()
        return self.xs[:]


if __name__ == '__main__':
    import random

    xs = [random.randint(0,100) for i in range(16)]
    print xs
    for lst in MergeSort(xs):
        print lst

