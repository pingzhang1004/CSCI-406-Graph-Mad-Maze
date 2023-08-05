import string
import networkx as graphLibrary
from collections import namedtuple
import matplotlib.pyplot as plotLibrary

#State is the Data Structure for store the location for R and L as point.
State=namedtuple("State","R L")

# read the input file
def setUpInput(inPutfile):
    file = open(inPutfile)
    # set the total number of nodes and the total number of edges
    nodesNumber,edgesNumber = file.readline().replace("\n", "").replace("\r", "").split(" ")
    colors_AllNodes = file.readline().replace("\n", "").replace("\r", "").split(" ")
    # set start location
    startLocation_R,startLocation_L = file.readline().replace("\n", "").replace("\r", "").split(" ")
    startLocation_R = int(startLocation_R)-1
    startLocation_L = int(startLocation_L)-1
    # set direction of edge and color of edge
    readEdges = list()
    for i in range(int(edgesNumber)):
        readEdge = file.readline().replace("\n", "").replace("\r", "").split(" ")
        readEdges.append(readEdge)
    return  int(nodesNumber),int(edgesNumber),colors_AllNodes,startLocation_R,startLocation_L,readEdges

#creat the original Maze Graph
def makeMazeGraph(nodesNumber,edgesNumber,colors_AllNodes,startLocation_R,startLocation_L,readEdges):
	mazeGraph = graphLibrary.DiGraph()	
    # set color for each node, and add node to mazeGraph
	for i in range(len(colors_AllNodes)):
		mazeGraph.add_node(i,color = colors_AllNodes[i])
	# set goal node color is W(white), and add the Goal node to the the mazeGraph
	mazeGraph.add_node(len(colors_AllNodes),color = 'W')
	
	# set color for each edge, and add edge to mazeGraph
	for i in range(int(edgesNumber)):
		mazeGraph.add_edge(int(readEdges[i][0])-1,int(readEdges[i][1])-1,color=str(readEdges[i][2]))
	return mazeGraph,int(nodesNumber)-1,startLocation_R,startLocation_L

#convert the mazeGraph to the resulting Graph
#the node of resulting Graph represents the Location for Rocket and lucky
#the directed edge of resulting Graph represents the moving of Rocket or lucky
def makeResultingGraph(MazeGraph,nodeNumber_Goal,startLocation_R,startLocation_L):
    resultingGraph = graphLibrary.DiGraph()
    check_NextNodes = []
    for i in range(nodeNumber_Goal+1):
        temp_list = []
        for j in range(nodeNumber_Goal+1):
            temp_list.append(-1)
        check_NextNodes.append(temp_list)
    
    # recursive call to check wehther R or L can be move to one of the adjencent nodes
    def checkMovingState(current_State,next_node,checkMove_R):
    # checkMove_R = true it means R move to nextNode
        if checkMove_R:
            if MazeGraph.edges()[(current_State[0],next_node)]['color'] == MazeGraph.nodes()[current_State[1]]['color']:
                next_state = State(next_node,current_State[1])
                resultingGraph.add_node(next_state)            
                resultingGraph.add_edge(current_State,next_state)
                if check_NextNodes[next_state[0]][next_state[1]] != -1:
                    return
                check_NextNodes[next_state[0]][next_state[1]] = next_state
                for next_left in list(MazeGraph.adj.items())[next_state[0]][1]:
                    checkMovingState(next_state,next_left,True)
                for next_right in list(MazeGraph.adj.items())[next_state[1]][1]:
                    checkMovingState(next_state,next_right,False)

    # checkMove_R = false it means L move to nextNode
        else: 
            if MazeGraph.edges()[(current_State[1],next_node)]['color'] == MazeGraph.nodes()[current_State[0]]['color']:
                next_state = State(current_State[0],next_node)
                resultingGraph.add_node(next_state)
                resultingGraph.add_edge(current_State,next_state)
                if check_NextNodes[next_state[0]][next_state[1]] != -1:
                    return
                check_NextNodes[next_state[0]][next_state[1]] = next_state
                for next_left in list(MazeGraph.adj.items())[next_state[0]][1]:
                    checkMovingState(next_state,next_left,True)
                for next_right in list(MazeGraph.adj.items())[next_state[1]][1]:
                    checkMovingState(next_state,next_right,False)
    
    # Firstly, check the adjencent nodes of R  to find all the possible moving 
    # Secondly check adjencent nodes of L to find all the possible moving 
    starting_state=State(startLocation_R,startLocation_L)
    if check_NextNodes[starting_state[0]][starting_state[1]] != -1:
        return
    check_NextNodes[starting_state[0]][starting_state[1]] = starting_state
    for next_left in list(MazeGraph.adj.items())[starting_state[0]][1]:
        checkMovingState(starting_state,next_left,True)
    for next_right in list(MazeGraph.adj.items())[starting_state[1]][1]:
        checkMovingState(starting_state,next_right,False)
    
    return resultingGraph

# convert the number of node to Alphabet letter 
# Alphabet letter is shown in the output file
def nodeID_to_Letter(nodeNumber_total,nodeNumber_Goal):
	list_AlphabetLetter = ""
	if nodeNumber_total == nodeNumber_Goal+1: return 'end'
	for i in range(int((nodeNumber_total-1)/26)+1):
	    list_AlphabetLetter = list_AlphabetLetter+list(string.ascii_uppercase)[(nodeNumber_total-1)%26]
	    nodeNumber_total = nodeNumber_total-26
	return list_AlphabetLetter

#  Link the nodeID of node and Alphabet letter of node to a string
#  the linking string is shown in the in the output file
def outPutFormat(nodeID,nodeNumber_Goal):
    R_listAlphabetLetter = ""
    L_nodeNumberTotal = nodeID[0][1]+1
    R_ListAlphabetLetter = ""
    R_nodeNumberTotal = nodeID[0][0]+1
    if nodeID[0][0] == nodeID[1][0]:       
        if L_nodeNumberTotal == nodeNumber_Goal+1: 
            return 'end'
        for i in range(int((L_nodeNumberTotal-1)/26)+1):
            R_listAlphabetLetter = R_listAlphabetLetter+list(string.ascii_uppercase)[(L_nodeNumberTotal-1)%26]
            L_nodeNumberTotal = L_nodeNumberTotal-26  
        return('L ' + str(nodeID[0][1]+1)+'\t// Lucky moves to '+ R_listAlphabetLetter)
    else:
        if R_nodeNumberTotal == nodeNumber_Goal+1: 
            return 'end'
        for i in range(int((R_nodeNumberTotal-1)/26)+1):
            R_ListAlphabetLetter = R_ListAlphabetLetter+list(string.ascii_uppercase)[(R_nodeNumberTotal-1)%26]
            R_nodeNumberTotal = R_nodeNumberTotal-26  
        return('R ' + str(nodeID[0][1]+1)+'\t// Lucky moves to '+ R_ListAlphabetLetter)

#traverse BFS tree ot get the shortest path
def shortestPath_BFStree(BSF_tree,nodeNumber_Goal):
    IsFindGoal = False
    # extract the idx of those states which contain the "GOAL"
    indices_goal = []
    for i in range(len(BSF_tree)):
        if BSF_tree[-i-1][0][0] == nodeNumber_Goal or BSF_tree[-i-1][0][1] == nodeNumber_Goal:
            indices_goal.append(i)

    paths_AllPossible = list()
    shortest_length = 50000   # a large integer
    best_idx = 0    # index of shortest paths in all paths_AllPossible
    for j in range(len(indices_goal)):
        cur_idx = indices_goal[j]
        temp_list = list()
        paths_AllPossible.append(temp_list)
        index = 0
        IsFindGoal = False
        for i in range(cur_idx, len(BSF_tree)):
            if IsFindGoal == False and (BSF_tree[-i - 1][0][0] == nodeNumber_Goal or BSF_tree[-i - 1][0][1] == nodeNumber_Goal):
                IsFindGoal = True
                paths_AllPossible[j].append(outPutFormat(BSF_tree[-i - 1], nodeNumber_Goal))
                index = i
            if IsFindGoal == True and BSF_tree[-i - 1][0] == BSF_tree[-index - 1][1]:
                index = i
                paths_AllPossible[j].append(outPutFormat(BSF_tree[-i - 1], nodeNumber_Goal))
        if len(paths_AllPossible[j]) < shortest_length:
            shortest_length = len(paths_AllPossible[j])
            best_idx = j

    return paths_AllPossible,best_idx
       
#draw the resulting graph and save it as png
#using the matplotlib.pyplot library to save the graph as png 
def drawRresultingGraph(resultingGraph, nodePosition_figure):
    # set the resulting graph size
    plotLibrary.figure(figsize = (10,10),dpi = 400)
        
    # draw all nodes of the resulting graph 
    for node in resultingGraph.nodes():
        graphLibrary.draw_networkx_nodes(resultingGraph, nodePosition_figure, nodelist = list(resultingGraph.nodes()), node_size = 250, node_color = 'Yellow', alpha=0.9)

    # draw all edges of the resulting graph 
    for edge in resultingGraph.edges:
        graphLibrary.draw_networkx_edges(resultingGraph, nodePosition_figure, edgelist = list(resultingGraph.edges()),width=2, alpha = 0.9, edge_color = 'Black')
   
    # draw node value 
    # each node has a pair of value such as (Location_R,Location_L) 
    nodeValue = {}
    for node in resultingGraph.nodes():
        # First value is Location of R, and second value is Location of L
        # link the (Location_R,Location_L) as a string
        nodeValue[node] = str(node[0]+1)+", "+str(node[1]+1)
    graphLibrary.draw_networkx_labels(resultingGraph, nodePosition_figure, nodeValue, font_size = 6)
    
    plotLibrary.axis('off')
    plotLibrary.savefig(r"C:\Users\41339\Desktop\CSCI406\project4\Canvas_TestExample\resultingGraph.png", dpi = 400)   

#main function
if __name__ == "__main__":  
    # step1: read input file 
    nodesNumber,edgesNumber,colors_AllNodes,startLocation_R,startLocation_L,readEdges = setUpInput(r"C:\Users\41339\Desktop\CSCI406\project4\Canvas_TestExample\Verification_Input_2.txt")
    # step2: creat maze graph according the inoput file
    original_graph,nodeNumber_Goal,startLocation_R,startLocation_L = makeMazeGraph(nodesNumber,edgesNumber,colors_AllNodes,startLocation_R,startLocation_L,readEdges)
    # step3: creat resulting graph according maze graph
    resultingGraph = makeResultingGraph(original_graph,nodeNumber_Goal,startLocation_R,startLocation_L)
    # step4: traverse the resulting graph by BFS(using the networkx graphLibrary)
    BFStree_rerulingGraph = list(graphLibrary.bfs_predecessors(resultingGraph,State(R = startLocation_R,L = startLocation_L)))
    # step5: traverse the BFS tree and get the shortest path (using the networkx graphLibrary)
    # insert the outformat into the shortest path function
    paths_AllPossible,best_idx = shortestPath_BFStree(BFStree_rerulingGraph,nodeNumber_Goal)
    # step6: draw the esulting graph and save it as png (using the matplotlib.pyplot figure Library)
    # drawRresultingGraph(resultingGraph,nodePosition_figure = graphLibrary.fruchterman_reingold_layout(resultingGraph))
    # step7: print the output in correct format
    print('Length of shortest path is: ', len(paths_AllPossible[best_idx]))   
    for i in range(len(paths_AllPossible[best_idx])):
        print(paths_AllPossible[best_idx][-i-1])
