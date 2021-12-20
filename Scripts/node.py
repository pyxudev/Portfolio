import math

route_list = [[0, 50, 80, 0, 0], [0, 0, 20, 15, 0 ], [0, 0, 0, 10, 15], [0, 0, 0, 0, 30], [0, 0, 0, 0, 0]] # 初期のノード間の距離のリスト

node_num = len(route_list)

unsearched_nodes = list(range(node_num))
distance = [math.inf] * node_num
previous_nodes = [-1] * node_num
distance[0] = 0

def get_target_min_index(min_index, distance, unsearched_nodes):
    start = 0

    while True:
        index = distance.index(min_index, start)
        found = index in unsearched_nodes

        if found:
            return index

        else:
            start = index + 1

while(len(unsearched_nodes) != 0):
    posible_min_distance = math.inf

    for node_index in unsearched_nodes:

        if posible_min_distance > distance[node_index]:
            posible_min_distance = distance[node_index]

    target_min_index = get_target_min_index(posible_min_distance, distance, unsearched_nodes) # 未探索ノードのうちで最小のindex番号を取得
    unsearched_nodes.remove(target_min_index)

    target_edge = route_list[target_min_index]

    for index, route_dis in enumerate(target_edge):

        if route_dis != 0:

            if distance[index] > (distance[ target_min_index] + route_dis):
                distance[index] = distance[ target_min_index] + route_dis
                previous_nodes[index] =  target_min_index

print("-----route-----")
previous_node = node_num - 1

while previous_node != -1:

    if previous_node !=0:
        print(str(previous_node + 1) + " <- ", end='')

    else:
        print(str(previous_node + 1))

    previous_node = previous_nodes[previous_node]

print("-----distance-----")
print(distance[node_num - 1])
