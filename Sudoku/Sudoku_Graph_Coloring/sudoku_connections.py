from graph import Graph

class SudokuConnections: 
    def __init__(self):  # constructor

        self.graph = Graph() # Graph Object

        self.rows = 9
        self.cols = 9
        self.total_blocks = self.rows*self.cols #81

        self.__generateGraph() # Generates all the nodes
        self.connectEdges() # connects all the nodes acc to sudoku constraints

        self.allIds = self.graph.getAllNodesIds() # storing all the ids in a list

    def __generateGraph(self): 
        """
        Generates nodes with id from 1 to 81.
        Both inclusive
        """
        
        for idx in range(1, self.total_blocks+1): 
            _ = self.graph.addNode(idx)

    def connectEdges(self): 
        """
        Connect nodes according to Sudoku Constraints: 
        """

        matrix = self.getGridMatrix()

        head_connections = dict()

        for row in range(9):
            for col in range(9): 
                
                head = matrix[row][col] #id of the node
                connections = self.whatToConnect(matrix, row, col)
                
                head_connections[head] = connections

        # connect all the edges
        self.__connectThose(head_connections=head_connections)
        
    def __connectThose(self, head_connections): 
        for head in head_connections.keys(): #head is the start idx
            connections = head_connections[head]
            for key in connections:  #get list of all the connections
                for v in connections[key]: 
                    self.graph.addEdge(src=head, dst=v)

 
    def whatToConnect(self, matrix, rows, cols):
        """
        matrix: stores the id of each node representing each cell
        returns dictionary
        """

        connections = dict()

        row = []
        col = []
        block = []

        # ROWS
        for c in range(cols+1, 9): 
            row.append(matrix[rows][c])
        
        connections["rows"] = row

        # COLS 
        for r in range(rows+1, 9):
            col.append(matrix[r][cols])
        
        connections["cols"] = col

        # BLOCKS
        if rows%3 == 0: 
            if cols%3 == 0:
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+1][cols+2])
                block.append(matrix[rows+2][cols+1])
                block.append(matrix[rows+2][cols+2])
            elif cols%3 == 1:
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+2][cols-1])
                block.append(matrix[rows+2][cols+1])
            elif cols%3 == 2:
                block.append(matrix[rows+1][cols-2])
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+2][cols-2])
                block.append(matrix[rows+2][cols-1])
        elif rows%3 == 1:
            if cols%3 == 0:
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows-1][cols+2])
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+1][cols+2])
            elif cols%3 == 1:
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+1][cols+1])
            elif cols%3 == 2:
                block.append(matrix[rows-1][cols-2])
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows+1][cols-2])
                block.append(matrix[rows+1][cols-1])
        elif rows%3 == 2:
            if cols%3 == 0:
                block.append(matrix[rows-2][cols+1])
                block.append(matrix[rows-2][cols+2])
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows-1][cols+2])
            elif cols%3 == 1:
                block.append(matrix[rows-2][cols-1])
                block.append(matrix[rows-2][cols+1])
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows-1][cols+1])
            elif cols%3 == 2:
                block.append(matrix[rows-2][cols-2])
                block.append(matrix[rows-2][cols-1])
                block.append(matrix[rows-1][cols-2])
                block.append(matrix[rows-1][cols-1])
        
        connections["blocks"] = block
        return connections

    def getGridMatrix(self): 
        """
        Generates the 9x9 grid or matrix consisting of node ids.
        
        This matrix will act as amapper of each cell with each node 
        through node ids
        """

        matrix = [[0 for cols in range(self.cols)] 
        for rows in range(self.rows)]

        count = 1
        for rows in range(9):
            for cols in range(9):
                matrix[rows][cols] = count
                count+=1
        return matrix
  
def test_connections(): 
    sudoku = SudokuConnections()
    sudoku.connectEdges()
    print("All node Ids: ")
    print(sudoku.graph.getAllNodesIds())
    print()
    for idx in sudoku.graph.getAllNodesIds(): 
        print(idx, "Connected with:", sudoku.graph.allNodes[idx].getConnections())

test_connections()