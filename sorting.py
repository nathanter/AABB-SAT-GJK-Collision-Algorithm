import numpy
def sort(array):

    
    place = 0
    if len(array) == 1:
        return array
    if len(array) == 0:
        return []
    pivot = array[-1]
    for x in range(len(array)):
        if array[x].coords[0] < pivot.coords[0]:
            temp = array[place]
            array[place] = array[x]
            array[x] = temp
         
            place += 1
    
   
    temp = array[place]
    array[place] = pivot
    array[-1] = temp

    endarray =  subarray(place+1,len(array),array)
    frontarray = subarray(0,place,array)
    return add(add(sort(frontarray),[pivot]),sort(endarray))
                    
    

def add(array1,array2):
    for x in array2:
        array1.append(x)

    return array1
def subarray(start,stop,array):
    new = []
    for x in range(start,stop):
        new.append(array[x])
    return new



