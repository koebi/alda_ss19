def binarySearchI(a, key, start, end):
    while start <= end:
        center = (start+end)//2
        if key == a[center]:
            return center
        elif key < a[center]:
            end = center
        else:
            start = center+1
    return None
