import unittest

graph = [[1],
         [3,2,0],
         [1],
         [5,4,1],
         [3],
         [7,6,3],
         [5],
         [10,8,5],
         [10,9,7],
         [8],
         [11,8,7],
         [13,12,10],
         [11],
         [15,14,11],
         [13],
         [13]]

def way_out(graph, startnode, targetnode):
    visited = [False]*len(graph)

    # Zusatz-Infos für Lösung
    preorder = []
    dead_ends = 0
    
    def visit(node, targetnode):
        # Notwendig um auf die Variable außerhalb des scopes zuzugreifen.
        nonlocal dead_ends

        print(f"Aktuell in {node}")

        if node == targetnode:
            print(f"Target reached: {dead_ends} Sackgassen")
            return True

        if not visited[node]:
            visited[node] = True
            preorder.append(node)
            for neighbor in graph[node]:
                # Hier muss überprüft werden, ob wir evtl. Nachbarn schon
                # besucht haben. Ansonsten wird beispielsweise Knoten 15 von
                # Knoten 13 aus direkt wieder besucht, da der "if not
                # visited"-Check erst im visit()-call passiert.
                if visited[neighbor]:
                    continue
                if visit(neighbor, targetnode):
                    return True
                else:
                    print(f"Aktuell in {node} (backtrack)")
        print("Sackgasse")
        dead_ends += 1
        return False
    
    visit(startnode, targetnode)
    return preorder


def way_out_stack(graph, startnode, targetnode):
    visited = [False]*len(graph)

    stack = []
    stack.append(startnode)

    # Zusatz-Infos für Lösung
    preorder = []
    dead_ends = 0

    while len(stack) > 0:
        node = stack.pop()
        print(f"Aktuell in {node}")

        if node == targetnode:
            print(f"Target reached: {dead_ends} Sackgassen.")
            #TODO:
            # Eigentlich sollte hier gespeichert werden, dass das Ziel erreicht
            # wurde, dann mit "break" aus der Schleife gesprungen werden. Dann
            # hat die Funktion nicht zwei returns. So brauchen wir aber keine
            # Zusatzvariable.
            return preorder

        if not visited[node]:
            visited[node] = True
            preorder.append(node)

            # Wir müssen unbesuchte Nachbarn zählen, um zu checken, ob wir in
            # einer Sackgasse sind.
            unvisitedNeighbors = 0
            for neighbor in reversed(graph[node]):
                if visited[neighbor]:
                    continue
                stack.append(neighbor)
                unvisitedNeighbors += 1
            if unvisitedNeighbors == 0:
                dead_ends += 1
                print("Sackgasse")

    print("Ziel unerreichbar.")
    return preorder

class wayOutTest(unittest.TestCase):

    def testSamePreorder(self):
        for startnode in range(len(graph)):
            for endnode in range(len(graph)):
                recursivePreorder = way_out(graph, startnode, endnode)
                iterativePreorder = way_out_stack(graph, startnode, endnode)
                self.assertEqual(recursivePreorder, iterativePreorder)

if __name__ == "__main__":
    print("--- Rekursive Lösung ---")
    print(way_out(graph, 15, 0))
    print("\n--- Iterative Lösung ---")
    print(way_out_stack(graph, 15, 0))

    # buffer=True sorgt dafür, dass die erfolgreichen Tests nicht die ganze
    # Konsole vollschreiben
    unittest.main(buffer=True)
