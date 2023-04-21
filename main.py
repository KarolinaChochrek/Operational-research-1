from typing import Dict, List, Tuple
import numpy as np


# musze zrobic 2 funkcje, w tym jedna sprawdza czy w ogole polaczenie miedzy wierzcholkami istenieje
# na koniec musi wiedziec ze idzie tylko do poczatkowego

def greedy_tsp(G: Dict[int, List[int]], a: List[List[int]]):  # parametry: lista sąsiedztwa
    # i macierz sąsiedztwa grafu
    n = len(a)  # liczba wierzchołków w grafie
    growing_edges = []  # krawędzie posortowane według rosnących wag
    visited = set()  # najpierw żaden wierzchołek nie jest odwiedzony
    path = []  # odwiedzone wierzchołki w zadanej przez algorytm kolejności
    cost = 0  # koszt przebycia zadanej drogi
    # utworzenie listy z krawędziami oraz odpowiadającymi im wagami
    for i in range(n):
        for j in range(n):
            if a[i][j] == np.inf:
                pass
            else:
                growing_edges.append((i, j, a[i][j]))
    # posortowanie listy z krawędziami według rosnących wag
    growing_edges.sort(key=lambda x: x[2])
    # wybór pierwszego wierzchołka, któremu odpowiada najmniejsza waga
    # dodanie go do ścieżki
    path.append(growing_edges[0][0])
    # dodanie pierwszego wierzchołka do zbioru 'odwiedzonych'
    visited.add(growing_edges[0][0])
    # zmienna 'rodzic' zabezpieczająca przed powstaniem podcyklu
    parent = growing_edges[0][0]
    # kopia listy rosnących krawędzi, ponieważ będziemy z niej
    # usuwać krawędzie
    growing_edges_copy = growing_edges
    # pierwsza pętla powraca zawsze do początku listy z krawędziami,
    # ponieważ możemy napotkać krawędź, która ma mniejszą wagę niż
    # poprzednie
    j = 0
    while j < len(growing_edges_copy):
        # druga pętla poszukuje w liście wierzchołka, do którego przejdziemy
        i = 0
        while i < len(growing_edges_copy):
            # oddzielna 'krawędź' z listy krawędzi
            # jest to krotka z trzema elementami
            edge = growing_edges_copy[i]
            # rozpakowujemy krotkę do wierzchołków i wagi krawędzi
            x, y, weight = edge[0], edge[1], edge[2]
            # jeżeli jeden wierzchołek jest rodzicem a drugi
            # wierzchołek nie został odwiedzony
            if x == parent and y not in visited:
                # zabezpieczenie, czy na pewno istnieje
                # krawędź pomiędzy wierzchołkami
                if y in G[x]:
                    # uaktualnij koszty, ścieżkę,
                    # zbiór odwiedzonych wierzchołków i rodzica
                    visited.add(y)
                    path.append(y)
                    cost += weight
                    parent = y
                    # zabezpieczenie przed powrotem
                    # usuń krotkę z listy i zakończ
                    # wewnętrzną, poszukującą pętlę
                    del growing_edges_copy[i]
                    break
                # w przeciwnym wypadku, kontynuuj
                else:
                    i += 1
            # to samo co wyżej, tylko dla przeciwnych x i y
            elif y == parent and x not in visited:
                if x in G[y]:
                    visited.add(x)
                    path.append(x)
                    cost += weight
                    parent = x
                    del growing_edges_copy[i]
                    break
                else:
                    i += 1
            else:
                i += 1
        j += 1
    # jeżeli ścieżka osiągnęła wszystkie wierzchołki
    # oraz ostatni element ścieżki znajduję się w wartościach
    # listy sąsiedztwa od pierwszego elementu ścieżki, to
    # powróć do pierwszego elementu ścieżki i uaktualnij koszty
    if len(path) == n and path[-1] in G[path[0]]:
        cost += a[path[-1]][path[0]]
        path.append(path[0])
    else:
        print('Uzyskana ścieżka nie utworzyła cyklu Hamiltona')
    return cost, path


if __name__ == '__main__':
    # np.inf = 9999999
    graph = {
        0: [1, 2, 5],
        1: [0, 2, 3],
        2: [0, 1, 3, 5],
        3: [1, 2, 4],
        4: [3, 5],
        5: [0, 2, 4]
    }

    a = [
        [np.inf, 1, 9, np.inf, np.inf, 14],
        [1, np.inf, 10, 15, np.inf, np.inf],
        [9, 10, np.inf, 11, np.inf, 2],
        [np.inf, 15, 11, np.inf, 6, np.inf],
        [np.inf, np.inf, np.inf, 6, np.inf, 9],
        [14, np.inf, 2, np.inf, 9, np.inf]
    ]

    graph1 = {
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [0, 1, 2]
    }
    a1 = [
        [np.inf, 10, 15, 20],
        [10, np.inf, 35, 25],
        [15, 35, np.inf, 30],
        [20, 25, 30, np.inf]
    ]
    graph2 = {
        0: [1, 2, 5],
        1: [0, 3, 4],
        2: [0, 3, 5, 6, 8],
        3: [1, 2, 5, 6, 7, 8],
        4: [1, 6, 7],
        5: [0, 2, 3, 6, 8],
        6: [2, 3, 4, 5, 7, 8, 9],
        7: [3, 4, 6],
        8: [2, 3, 5, 6, 9],
        9: [6, 8]
    }
    a2 = [
        [np.inf, 5, 3, np.inf, np.inf, 8, np.inf, np.inf, np.inf, np.inf],
        [5, np.inf, np.inf, 2, 4, np.inf, np.inf, np.inf, np.inf, np.inf],
        [3, np.inf, np.inf, 4, np.inf, 7, 7, np.inf, 7, np.inf],
        [np.inf, 2, 4, np.inf, np.inf, 5, 8, 5, 9, np.inf],
        [np.inf, 4, np.inf, np.inf, np.inf, np.inf, 3, 2, np.inf, np.inf],
        [8, np.inf, 7, 5, np.inf, np.inf, 6, np.inf, 4, np.inf],
        [np.inf, np.inf, 7, 8, 3, 6, np.inf, 1, 6, 4],
        [np.inf, np.inf, np.inf, 5, 2, np.inf, 1, np.inf, np.inf, np.inf],
        [np.inf, np.inf, 7, 9, np.inf, 4, 6, np.inf, np.inf, 5],
        [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 4, np.inf, 5, np.inf]
    ]

    graph3 = {
        0: [1, 2, 5],
        1: [3],
        2: [0, 3, 5, 6, 8],
        3: [2, 5, 6, 7, 8],
        4: [1, 6, 7],
        5: [0, 2, 3, 6, 8],
        6: [2, 3, 4, 5, 7, 8, 9],
        7: [3, 4, 6],
        8: [2, 3, 5, 6, 9],
        9: [6, 8]
    }
    a3 = [
        [np.inf, 5, 3, np.inf, np.inf, 8, np.inf, np.inf, np.inf, np.inf],
        [np.inf, np.inf, np.inf, 2, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
        [3, np.inf, np.inf, 4, np.inf, 7, 7, np.inf, 7, np.inf],
        [np.inf, np.inf, 4, np.inf, np.inf, 5, 8, 5, 9, np.inf],
        [np.inf, 4, np.inf, np.inf, np.inf, np.inf, 3, 2, np.inf, np.inf],
        [8, np.inf, 7, 5, np.inf, np.inf, 6, np.inf, 4, np.inf],
        [np.inf, np.inf, 7, 8, 3, 6, np.inf, 1, 6, 4],
        [np.inf, np.inf, np.inf, 5, 2, np.inf, 1, np.inf, np.inf, np.inf],
        [np.inf, np.inf, 7, 9, np.inf, 4, 6, np.inf, np.inf, 5],
        [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 4, np.inf, 5, np.inf]
    ]
    graph4 = {  # pelny
        0: [1, 2, 3, 4, 5, 6, 7, 8, 9],
        1: [0, 2, 3, 4, 5, 6, 7, 8, 9],
        2: [0, 1, 3, 4, 5, 6, 7, 8, 9],
        3: [0, 1, 2, 4, 5, 6, 7, 8, 9],
        4: [0, 1, 2, 3, 5, 6, 7, 8, 9],
        5: [0, 1, 2, 3, 4, 6, 7, 8, 9],
        6: [0, 1, 2, 3, 4, 5, 7, 8, 9],
        7: [0, 1, 2, 3, 4, 5, 6, 8, 9],
        8: [0, 1, 2, 3, 4, 5, 6, 7, 9],
        9: [0, 1, 2, 3, 4, 5, 6, 7, 8],
    }
    a4 = [
        [np.inf, 5, 3, 2, 6, 8, 9, 2, 4, 5],
        [5, np.inf, 5, 2, 4, 9, 3, 2, 1, 7],
        [3, 5, np.inf, 4, 5, 7, 7, 6, 7, 2],
        [2, 2, 4, np.inf, 6, 5, 8, 5, 9, 4],
        [6, 4, 5, 6, np.inf, 7, 3, 2, 1, 8],
        [8, 9, 7, 5, 7, np.inf, 6, 1, 4, 3],
        [9, 3, 7, 8, 3, 6, np.inf, 1, 6, 4],
        [2, 2, 6, 5, 2, 1, 1, np.inf, 3, 4],
        [4, 1, 7, 9, 1, 4, 6, 3, np.inf, 5],
        [5, 7, 2, 4, 8, 3, 4, 4, 5, np.inf]
    ]
    # print(greedy_tsp(graph, a))
    # print(greedy_tsp(graph1, a1))
    # print(greedy_tsp(graph2, a2))
    # print(greedy_tsp(graph3, a3))
    print(greedy_tsp(graph4, a4))

