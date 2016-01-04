import itertools


def Dijkstra(matrix, matrix_len, start, end):
    dist = {(i, j): None for i in range(matrix_len)
                              for j in range(matrix_len)}
    dist[start] = 0

    #directions = {(x, y) for x in [-1, 0, 1]
    #                     for y in [-1, 0, 1]}

    directions = set(itertools.product([-1, 0, 1], repeat=2))

    visited = set()

    queue = list()
    queue.append(start)
    while queue:
        si, sj = queue[0]
        for dtn in directions:
            di, dj = dtn
            ind1 = si + di
            ind2 = sj + dj
            if (ind1, ind2) not in visited:
                if ind1 >= 0 and ind1 < matrix_len and ind2 >= 0 and ind2 < matrix_len:
                    if dist[(ind1, ind2)] == None:
                        dist[(ind1, ind2)] = dist[(si, sj)] + abs(matrix[si][sj] - matrix[ind1][ind2]) + 1
                    elif dist[(ind1, ind2)] > dist[(si, sj)] + abs(matrix[si][sj] - matrix[ind1][ind2]) + 1:
                        dist[(ind1, ind2)] = dist[(si, sj)] + abs(matrix[si][sj] - matrix[ind1][ind2]) + 1

                    if (ind1, ind2) not in queue:
                        queue.append((ind1, ind2))
        visited.add((si, sj))
        queue.pop(0)
    return dist[end]


def main():
    matrix_len = int(input())
    start_end = [int(x) for x in input().split()]
    start, end = [(start_end[i], start_end[i + 1])
                  for i in range(0, len(start_end), 2)]
    matrix = []
    for i in range(matrix_len):
        row = [int(x) for x in input().split()]
        matrix.append(row)
    print(Dijkstra(matrix, matrix_len, start, end))


if __name__ == '__main__':
    main()
