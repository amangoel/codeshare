#!/usr/bin/env python3


import random


class Node:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None


def print_tree(root_node: Node):
    def _save_value_width_map(_node, _key, width_map):
        width_map[_key] = len(str(_node.value))
        if _node.left_child is not None:
            _save_value_width_map(_node.left_child, _key + 'L', width_map)
        if _node.right_child is not None:
            _save_value_width_map(_node.right_child, _key + 'R', width_map)

    def _save_subtree_width(_node, _key, _value_width_map, _subtree_width_map):
        width = 0
        if _node.left_child is not None:
            _save_subtree_width(_node.left_child, _key + "L", _value_width_map, _subtree_width_map)
            width += (_subtree_width_map[_key + 'L'] + 1)
        width += _value_width_map[_key]
        if _node.right_child is not None:
            _save_subtree_width(_node.right_child, _key + 'R', _value_width_map, _subtree_width_map)
            width += (_subtree_width_map[_key + 'R'] + 1)
        _subtree_width_map[_key] = width

    def _save_node_pos(_node, _key, _value_width_map, _subtree_width_map, pos_map):
        if _key == '.':
            if _node.left_child is None:
                pos_map[_key] = 0
            else:
                pos_map[_key] = _subtree_width_map['.L'] + 1
        else:
            if _key[-1] == 'L':
                if _node.right_child is not None:
                    pos_map[_key] = pos_map[_key[:-1]] - _subtree_width_map[_key + 'R'] - 2 - _value_width_map[_key]
                else:
                    pos_map[_key] = pos_map[_key[:-1]] - 1 - _value_width_map[_key]
            else:
                if _node.left_child is not None:
                    pos_map[_key] = pos_map[_key[:-1]] + _value_width_map[_key[:-1]] + \
                                    _subtree_width_map[_key + 'L'] + 2
                else:
                    pos_map[_key] = pos_map[_key[:-1]] + _value_width_map[_key[:-1]] + 1

        if _node.left_child is not None:
            _save_node_pos(_node.left_child, _key + 'L', _value_width_map, _subtree_width_map, pos_map)
        if _node.right_child is not None:
            _save_node_pos(_node.right_child, _key + 'R', _value_width_map, _subtree_width_map, pos_map)

    if root_node is None:
        print('There are no nodes in the tree.')
        return
    value_width_map = {}
    subtree_width_map = {}
    node_pos_map = {}
    _save_value_width_map(root_node, '.', value_width_map)
    _save_subtree_width(root_node, '.', value_width_map, subtree_width_map)
    _save_node_pos(root_node, '.', value_width_map, subtree_width_map, node_pos_map)
    current_level = [(root_node, '.')]
    while current_level:
        if current_level[0][0] is not root_node:
            line = [' ' for _ in range(subtree_width_map['.'])]
            for node, key in current_level:
                if key[-1] == 'L':
                    for c in range(node_pos_map[key] + value_width_map[key], node_pos_map[key[:-1]]):
                        line[c] = '-'
                else:
                    for c in range(node_pos_map[key[:-1]] + value_width_map[key[:-1]], node_pos_map[key]):
                        line[c] = '-'
            print(''.join(line))
        line = ''
        for i in range(len(current_level)):
            current_node = current_level[i][0]
            current_key = current_level[i][1]
            if i == 0:
                line += ' ' * node_pos_map[current_key]
            else:
                prev_key = current_level[i-1][1]
                line += ' ' * (node_pos_map[current_key] - node_pos_map[prev_key] - value_width_map[prev_key])
            line += f'{current_node.value}'
        print(line)
        next_level = []
        for node, key in current_level:
            if node.left_child is not None:
                next_level.append((node.left_child, key + 'L'))
            if node.right_child is not None:
                next_level.append((node.right_child, key + 'R'))
        current_level = next_level


print('Creating tree ...')
max_num_nodes = random.randint(0, 50)
print(f'Max number of nodes = {max_num_nodes}')
if max_num_nodes == 0:
    root_node = None
else:
    *values, = range(max_num_nodes)
    root_node = Node(random.choice(values))
    values.remove(root_node.value)
    print(f'Initialized root node with value = {root_node.value}')
    actual_num_nodes = 1
    nodes_with_missing_children = [root_node]
    for _ in range(max_num_nodes - 1):
        if not nodes_with_missing_children:
            break
        rand_node = random.choice(nodes_with_missing_children)
        if random.randint(0, 1):
            if not rand_node.left_child:
                value = random.choice(values)
                values.remove(value)
                rand_node.left_child = Node(value)
                nodes_with_missing_children.append(rand_node.left_child)
                print(f'Added left child with value = {value} to node with value = {rand_node.value}')
                actual_num_nodes += 1
        else:
            if not rand_node.right_child:
                value = random.choice(values)
                values.remove(value)
                rand_node.right_child = Node(value)
                nodes_with_missing_children.append(rand_node.right_child)
                print(f'Added right child with value = {value} to node with value = {rand_node.value}')
                actual_num_nodes += 1
        if rand_node.left_child and rand_node.right_child:
            nodes_with_missing_children.remove(rand_node)
    print(f'Actual number of nodes added to the tree = {actual_num_nodes}')
print('*******************************************************************************')
print_tree(root_node)


