import os
from Display import Display

class Simulation:
    defaultnode = "O"
    defaultagent = "a"
    defaultsource = "s"
    defaulttarget = "t"

    def fromfile(path):
        nodes = []
        edges = {}
        agents = []
        agenttosource = {}
        agenttotarget = {}
        width = 20
        height = 20
        positiontonode = {}
        nodetochar = {}
        agenttochar = {}
        
        with open(path, "r") as f:
            matrix = f.read().split("\n")

        width = len(matrix[0])
        height = len(matrix)

        for y, line in enumerate(matrix):
            for x, char in enumerate(line):
                if char != " ":
                    nodes.append(nodes[-1] + 1 if nodes else 0)
                    edges[nodes[-1]] = {nodes[-1]}
                    positiontonode[(x, y)] = nodes[-1]

                    if char != Simulation.defaultnode and char.isalpha():
                        if char.islower():
                            agents.append(char)
                            agenttochar[char] = char
                            agenttosource[char] = nodes[-1]
                        else:
                            agenttotarget[char] = nodes[-1]

        return Simulation(nodes, edges, agents, agenttosource, agenttotarget, width, height, positiontonode, nodetochar, agenttochar)

    def __init__(self, nodes, edges, agents, agenttosource, agenttotarget, width, height, positiontonode, nodetochar, agenttochar):
        assert len(agenttosource) == len(agenttotarget) == len(agents), (agenttosource, agenttotarget, agents)

        self.nodes = nodes
        self.edges = edges
        self.agents = agents
        self.agenttosource = agenttosource
        self.sourcetoagent = {agenttosource[node] : node for node in agenttosource}
        self.agenttotarget = agenttotarget
        self.targettoagent = {agenttotarget[node] : node for node in agenttotarget}
        self.nodetoagent = self.sourcetoagent.copy()

        self.setvisual(width, height, positiontonode, nodetochar, agenttochar)

    def setvisual(self, width, height, positiontonode, nodetochar, agenttochar):
        self.positiontonode = positiontonode
        self.width = width
        self.height = height
        self.nodetochar = nodetochar
        self.agenttochar = agenttochar

    def getstring(self, positions=True, sources=False, targets=True):
        string = []
        for y in range(self.height):
            for x in range(self.width):
                char = " "

                if (x, y) in self.positiontonode:
                    node = self.positiontonode[(x, y)]
                    char = self.nodetochar.get(node, Simulation.defaultnode)

                    position = False
                    if positions and node in self.nodetoagent:
                        agent = self.nodetoagent[node]
                        char = self.agenttochar.get(agent, Simulation.defaultagent)
                        position = True

                    source = False
                    if sources and node in self.sourcetoagent:
                        agent = self.sourcetoagent[node]
                        char = Display.color["red"] + self.agenttochar.get(agent, Simulation.defaultsource)
                        source = True

                    target = False
                    if targets and node in self.targettoagent:
                        agent = self.targettoagent[node]
                        char = Display.color["yellow" if source else "green"] + self.agenttochar.get(agent, Simulation.defaulttarget)
                        target = True
                    
                    if target + source + position > 1:
                        char = Display.color["greyback"] + char

                string.append(char)
            string.append("\n")
        return string
