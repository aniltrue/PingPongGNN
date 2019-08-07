from AI.Species import Species

def swap(species: list, index1: int, index2: int):
    temp = species[index1]
    species[index1] = species[index2]
    species[index2] = temp

def basicSort(species: list, left: int, right: int):
    for i in range(left, right + 1):
        for j in range(i + 1, right + 1):
            if species[j].gene > species[i].gene:
                swap(species, i, j)

def Qsort(species: list, left: int, right: int):
    if right - left < 5:
        basicSort(species, left, right)
        return

    i = left
    j = right - 1
    pivot = species[int((left + right) / 2)].gene
    swap(species, right, int((left + right) / 2))

    while j > i:
        while species[i].gene > pivot and j > i:
            i += 1
        while species[j].gene < pivot and j > i:
            j -= 1

        if j > i:
            swap(species, i, j)
            i += 1
            j -= 1

    swap(species, right, i)

    Qsort(species, left, i - 1)
    Qsort(species, i + 1, right)

def sort(species: list):
    Qsort(species, 0, len(species) - 1)