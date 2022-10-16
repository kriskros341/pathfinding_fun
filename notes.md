Tower defence needs either a vector field or a distance field 
(also called Dijkstra Map)

There are several classic algorithms
    One Source, One destination:
        Greedy Best First Algorithm,
        A*
    One Source, All Destinations or All Sources, One Destination:
        Breatdth First Search - Unweighted
        Dijkstra's Algorithm - Weighted
        Bellman-Ford - Supports Negative Weights
    All Sources All Destinations:
        Floyd-Warshall
        Johnson's Algorithm

Breatdth First fits perfectly. It's also called a flood fill.
it includes a frontier queue that holds fields adjecent to ones searched
uses:
    Mark All Reachable Nodes
    Find Paths
    Measure Distances

