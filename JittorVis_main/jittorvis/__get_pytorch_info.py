import torch

GETATTR_KIND = 'prim::GetAttr'
CLASSTYPE_KIND = 'ClassType'
TENSOR_KIND = 'TensorType'

MULTIPLE_OUTPUTS_TYPE = ['aten::cat']
count_nodes = 0
attr_to_scope = {}

nodes = {}
map_id_node = {}
edges = []

class Node(object):
    def __init__(self, index, title, type, node):
        self.node = node
        self.index = index
        self.title = title
        self.type = type
        self.scope = ""
        self.is_op = True
        self.inputs = []
        self.outputs = []
        self.attributes = ''
        self.inputs_tensor_size = []
        self.outputs_tensor_size = []

class OPNode(Node):
    def __init__(self, index, title, type, node, is_outputed=False, is_used_inputs=False):
        # is_op checks the Node is op or io node
        super(OPNode, self).__init__(index, title, type, node)
        self.next = []
        self.pre = []
        self.path = "" # path(e.g.RNN) is different with scope(e.g.__module) in io node
        self.parent = -1
        self.attr = {
            "has_feature": False,
            "name": title,
            "shape": "",
            "var_node_id": 0
        }
        self.is_op = True
        self.children = []
        self.is_outputed = is_outputed
        self.inputs_size = []
        self.outputs_size = []
        self.is_used_inputs = is_used_inputs
        if node != None:
            for m in ['inputs', 'outputs']:
                list_of_node = list(getattr(node, m)())
                io_unique_names = []
                io_tensor_sizes = []
                for n in list_of_node:
                    io_unique_names.append(n.debugName())
                    if n.isCompleteTensor():
                        io_tensor_sizes.append(n.type().sizes())
                    else:
                        io_tensor_sizes.append(None)

                setattr(self, m, io_unique_names)
                setattr(self, m + '_tensor_size', io_tensor_sizes)

class IONode(Node):
    def __init__(self, index, title, type, node, inputs, scope, tensor_size=None, attributes=None):
        super(IONode, self).__init__(index, title, type, node)
        # node(type str) is different from opnode(type Node)
        self.is_op = False
        self.inputs = inputs
        self.scope = scope
        self.tensor_size = tensor_size
        self.attributes = attributes
        self.debugName = ""
        self.in_OPNode = None # OPNode as inputs


class Edge(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.start_stack = []
        self.end_stack = []


def get_internal_relation(original_node):
    global edges
    in_tensor_sizes = []
    out_tensor_sizes = []

    for n in original_node.inputs():
        if n.isCompleteTensor():
            in_tensor_sizes.append(n.type().sizes())
        if n.node() != original_node:
            for j in nodes.keys():
                if n.node() == nodes[j].node and nodes[j].is_outputed:
                    add_edge(j, map_id_node[attr_to_scope[original_node]])
                    break

    for n in original_node.outputs():
        if n.isCompleteTensor():
            out_tensor_sizes.append(n.type().sizes())
    nodes[map_id_node[attr_to_scope[original_node]]].inputs_size = in_tensor_sizes
    nodes[map_id_node[attr_to_scope[original_node]]].outputs_size = out_tensor_sizes

def populate_namespace_from_OP_to_IO(nodes_io, shallowest_scope_name):
    # add io nodes
    scope_name_appeared = []
    unique_name_to_scoped_name = {}
    count_io = 0
    for node_index in nodes.keys():
        node = nodes[node_index]
        if node.is_used_inputs:
            for node_output, outputSize in zip(node.outputs, node.outputs_tensor_size):
                scope_name_appeared.append(node.path)
                count_io += 1
                nodes_io[node_output] = IONode(count_io, "IO", node.type, node_output, node.inputs, node.path, outputSize,
                                               node.attributes)
                nodes_io[node_output].debugName = node_output
                nodes_io[node_output].in_OPNode = node.node

    for node_index in nodes.keys():
        node = nodes[node_index]
        if node.is_used_inputs:
            for input_node_id in node.inputs:
                unique_name_to_scoped_name[input_node_id] = node.path + '/' + input_node_id
    for key, node in nodes_io.items():
        if node.title == 'Input' or node.title == 'Output':
            unique_name_to_scoped_name[key] = node.title + '/' + node.debugName

        else:
            unique_name_to_scoped_name[key] = node.scope + '/' + node.debugName
            if node.scope == '' and shallowest_scope_name:
                unique_name_to_scoped_name[node.debugName] = shallowest_scope_name + '/' + node.debugName

    # replace name
    for key, node in nodes_io.items():
        nodes_io[key].inputs = [unique_name_to_scoped_name[node_input_id] for node_input_id in
                                     node.inputs]
        if node.debugName in unique_name_to_scoped_name:
            nodes_io[key].debugName = unique_name_to_scoped_name[node.debugName]
    unique_reverse = {}
    for name in unique_name_to_scoped_name.keys():
        unique_reverse[unique_name_to_scoped_name[name]] = name

    # make the edges through inputs or outputs for cat type
    for node_index in nodes.keys():
        node = nodes[node_index]
        if node.type in MULTIPLE_OUTPUTS_TYPE:
            if node.type != GETATTR_KIND and node.is_used_inputs == True and node.is_outputed == True:
                input_nodes = []  # satisfy the node needs in making the edges through inputs or outputs
                for node_input in node.inputs:
                    flag_add_input_nodes = False
                    if node_input in nodes_io.keys():
                        if nodes_io[node_input].in_OPNode != None:
                            if nodes_io[node_input].in_OPNode in attr_to_scope:
                                input_nodes.append(nodes_io[node_input].in_OPNode)
                                flag_add_input_nodes = True
                        if not flag_add_input_nodes:
                            for j in nodes_io[node_input].inputs:
                                if unique_reverse[j] in nodes_io:
                                    if nodes_io[unique_reverse[j]].in_OPNode != None:
                                        if nodes_io[unique_reverse[j]].in_OPNode in attr_to_scope:
                                            input_nodes.append(nodes_io[unique_reverse[j]].in_OPNode)
                for i in input_nodes:
                    target = map_id_node[attr_to_scope[i]]
                    add_edge(target, node.index)
    return nodes_io, unique_reverse

def add_edge(start, end):
    global edges
    flag = True
    for edge in edges:
        # if (edge.start == start and edge.end == end) or (edge.start == end and edge.end == start):
        if (edge.start == start and edge.end == end):
            flag = False
            break
    if flag and nodes[start].is_outputed and nodes[end].is_outputed:
        edges.append(Edge(start, end))


def check_no_ancestor(node1, node2):
    #check if node2 is not the ancestor of node1
    node = node1
    while node.parent != -1:
        if node.parent == node2.index:
            return False
        node = nodes[node.parent]
    return True

def make_edges_through_inputs_item(node, node_original, nodes_io, unique_reverse):
    # make the edges through inputs or outputs except cat type
    for j in node.inputs:
        target_j = j
        if target_j in unique_reverse:
            target_j = unique_reverse[target_j]
        if target_j in nodes_io:
            input_node = nodes_io[target_j]
            if input_node.in_OPNode is not None:
                if input_node.in_OPNode in attr_to_scope:
                    if nodes[map_id_node[attr_to_scope[input_node.in_OPNode]]].is_outputed:
                        if check_no_ancestor(nodes[map_id_node[attr_to_scope[input_node.in_OPNode]]], node_original):
                            add_edge(map_id_node[attr_to_scope[input_node.in_OPNode]], node_original.index)
                else:
                    make_edges_through_inputs_item(input_node, node_original, nodes_io, unique_reverse)


def parse(graph, trace, args=None):

    global count_nodes
    global attr_to_scope
    global nodes
    global edges

    nodes_io = {}
    count_io = 0
    def get_root(graph):
        in_tensor_sizes = []
        out_tensor_sizes = []
        node =  OPNode(0, '', 'root', None, True)
        node.scope = ''
        nodes[0] = node

        for n in graph.inputs():
            if n.isCompleteTensor():
                in_tensor_sizes.append(n.type().sizes())
        for n in graph.outputs():
            if n.isCompleteTensor():
                out_tensor_sizes.append(n.type().sizes())
        nodes[0].inputs_size = in_tensor_sizes
        nodes[0].outputs_size = out_tensor_sizes
        nodes[0].inputs = [i for i in graph.inputs()]
        nodes[0].outputs = [i for i in graph.outputs()]


    get_root(graph)

    for node in graph.inputs():
        if node.type().kind() != CLASSTYPE_KIND:
            count_io += 1
            nodes_io[node.debugName()] = IONode(count_io, 'Input', node.type().kind(), node.node(), [],
                                                node.debugName())
            nodes_io[node.debugName()].debugName = node.debugName()

    for node in graph.nodes():
        if node.kind() == GETATTR_KIND:
            attr_name = node.s('name')
            parent = node.input().node()
            if parent.kind() != GETATTR_KIND:
                # If the parent node is the top-level "self" node
                # conv1 bn1 conv2 bn2 -> block
                # add OPNode
                attr_scope_all = '__module.{}'.format(attr_name)
                attr_to_scope[node] = attr_scope_all
                count_nodes += 1
                nodes[count_nodes] = OPNode(count_nodes, attr_name, node.kind(), node, True)
                nodes[count_nodes].scope = attr_scope_all
                nodes[count_nodes].parent = 0
                add_edge(count_nodes, nodes[count_nodes].parent)
                map_id_node[attr_scope_all] = count_nodes
            else:
                parent_scope = attr_to_scope[parent]
                attr_scope = parent_scope.split('/')[-1]
                attr_scope_all = '{}/{}.{}'.format(parent_scope, attr_scope, attr_name)
                attr_to_scope[node] = attr_scope_all
                count_nodes += 1
                nodes[count_nodes] = OPNode(count_nodes, attr_name, node.kind(), node, True)
                nodes[count_nodes].scope = attr_to_scope[node]
                nodes[count_nodes].parent = map_id_node[parent_scope]
                add_edge(count_nodes, nodes[count_nodes].parent)
                map_id_node[attr_scope_all] = count_nodes
            if node.output().type().kind() != CLASSTYPE_KIND:
                nodes[count_nodes].is_used_inputs = True
            get_internal_relation(node)
        else:
            try:
                if node.output().type().kind() == TENSOR_KIND:
                    # debug
                    # about {%113 : Tensor = prim::GetAttr[name="weight"](%87): [87 defined in (%87 : __torch__.torch.nn.modules.conv.Conv2d = prim::GetAttr[name="conv1"](%self.1))]}
                    # add OPNode
                    attr_name = node.kind()
                    if node.scopeName() != '':
                        parent_scope = node.scopeName().split('/')[-1]
                        attr_scope_all = '{}/{}.{}'.format(node.scopeName(), parent_scope, attr_name)
                        attr_to_scope[node] = attr_scope_all
                        count_nodes += 1
                        nodes[count_nodes] = OPNode(count_nodes, attr_name, attr_name, node, True, True)
                        nodes[count_nodes].scope = attr_scope_all
                        nodes[count_nodes].parent = map_id_node[node.scopeName()]
                        add_edge(count_nodes, nodes[count_nodes].parent)
                        map_id_node[attr_scope_all] = count_nodes
                    else:
                        # If the parent node is the top-level "self" node, such as the atten::
                        attr_scope_all = '__module.{}'.format(attr_name)
                        attr_to_scope[node] = attr_scope_all
                        count_nodes += 1
                        nodes[count_nodes] = OPNode(count_nodes, attr_name, attr_name, node, True, True)
                        nodes[count_nodes].scope = attr_scope_all
                        nodes[count_nodes].parent = 0
                        add_edge(count_nodes, nodes[count_nodes].parent)
                        map_id_node[attr_scope_all] = count_nodes
                    get_internal_relation(node)
                else:
                    # add more op nodes without outputting
                    count_nodes += 1
                    nodes[count_nodes] = OPNode(count_nodes, node.kind(), node.kind(), node, False, True)
            except RuntimeError as e:
                if node.outputs() != None:
                    flag = 0
                    for j in node.outputs():
                        if j.type().kind() == TENSOR_KIND:
                            flag = 1
                            break
                    if flag == 1:
                        attr_name = node.kind()
                        if node.scopeName() != '':
                            parent_scope = node.scopeName().split('/')[-1]
                            attr_scope_all = '{}/{}.{}'.format(node.scopeName(), parent_scope, attr_name)
                            attr_to_scope[node] = attr_scope_all
                            count_nodes += 1
                            nodes[count_nodes] = OPNode(count_nodes, attr_name, attr_name, node, True, True)
                            nodes[count_nodes].scope = attr_scope_all
                            nodes[count_nodes].parent = map_id_node[node.scopeName()]
                            add_edge(count_nodes, nodes[count_nodes].parent)
                            map_id_node[attr_scope_all] = count_nodes
                        else:
                            # If the parent node is the top-level "self" node, such as the atten::
                            attr_scope_all = '__module.{}'.format(attr_name)
                            attr_to_scope[node] = attr_scope_all
                            count_nodes += 1
                            nodes[count_nodes] = OPNode(count_nodes, attr_name, attr_name, node, True, True)
                            nodes[count_nodes].scope = attr_scope_all
                            nodes[count_nodes].parent = 0
                            add_edge(count_nodes, nodes[count_nodes].parent)
                            map_id_node[attr_scope_all] = count_nodes
                        get_internal_relation(node)
                else:
                    # add more op nodes without outputting
                    count_nodes += 1
                    nodes[count_nodes] = OPNode(count_nodes, node.kind(), node.kind(), node, False, True)

    for i, node in enumerate(graph.outputs()):  # Create sink nodes for output ops
        count_io += 1
        nodes_io["output.{}".format(i + 1)] = IONode(count_io, 'Output', node.type().kind(), node.node(), [node.debugName()], "output.{}".format(i + 1))
        nodes_io["output.{}".format(i + 1)].debugName = "output.{}".format(i + 1)

    def parse_traced_name(module):
        if isinstance(module, torch.jit.TracedModule):
            module_name = module._name
        else:
            module_name = getattr(module, 'original_name', "Module")
        return module_name

    alias_to_name = dict()
    base_name = parse_traced_name(trace)
    for name, module in trace.named_modules(prefix='__module'):
        mod_name = parse_traced_name(module)
        attr_name = name.split('.')[-1]
        alias_to_name[name] = '{}[{}]'.format(mod_name, attr_name)

    scope_to_path = {}
    for index in nodes.keys():
        node = nodes[index]
        scope1 = node.scope.split('-')[0]
        scope2 = ''.join(node.scope.split('-')[1:])
        module_aliases = scope1.split('/')
        replacements = [
            alias_to_name[alias]
            if alias in alias_to_name
            else alias.split('.')[-1]
            for alias in module_aliases
        ]
        node.path = base_name
        if any(replacements):
            node.path += '/' + '/'.join(replacements)
        node.path += scope2
        scope_to_path[node.scope] = node.path

    nodes[0].title = base_name
    nodes[0].attr["name"] = base_name
    nodes[0].scope = '__module'

    nodes_io, unique_reverse = populate_namespace_from_OP_to_IO(nodes_io, base_name)

    count_nodes = 0
    for node in graph.nodes():
        count_nodes += 1
        if node.kind() == GETATTR_KIND:
            attr_name = node.s('name')
            parent = node.input().node()
            if parent.kind() != GETATTR_KIND:
                attr_scope_all = '__module.{}'.format(attr_name)
                attr_to_scope[node] = attr_scope_all
                map_id_node[attr_scope_all] = count_nodes
                make_edges_through_inputs_item(nodes[count_nodes], nodes[count_nodes], nodes_io, unique_reverse)

            else:
                parent_scope = attr_to_scope[parent]
                attr_scope = parent_scope.split('/')[-1]
                attr_scope_all = '{}/{}.{}'.format(parent_scope, attr_scope, attr_name)
                attr_to_scope[node] = attr_scope_all
                map_id_node[attr_scope_all] = count_nodes
                make_edges_through_inputs_item(nodes[count_nodes], nodes[count_nodes], nodes_io, unique_reverse)
        else:

            try:
                if node.output().type().kind() == TENSOR_KIND:
                    attr_name = node.kind()
                    if node.scopeName() != '':
                        parent_scope = node.scopeName().split('/')[-1]
                        attr_scope_all = '{}/{}.{}'.format(node.scopeName(), parent_scope, attr_name)
                        attr_to_scope[node] = attr_scope_all
                        map_id_node[attr_scope_all] = count_nodes
                        make_edges_through_inputs_item(nodes[count_nodes], nodes[count_nodes], nodes_io,
                                                       unique_reverse)
                    else:
                        # If the parent node is the top-level "self" node, such as the atten::
                        attr_scope_all = '__module.{}'.format(attr_name)
                        attr_to_scope[node] = attr_scope_all
                        map_id_node[attr_scope_all] = count_nodes
                        make_edges_through_inputs_item(nodes[count_nodes], nodes[count_nodes], nodes_io,
                                                       unique_reverse)

            except RuntimeError as e:
                if node.outputs() != None:
                    flag = 0
                    for j in node.outputs():
                        if j.type().kind() == TENSOR_KIND:
                            flag = 1
                            break
                    if flag == 1:
                        attr_name = node.kind()
                        if node.scopeName() != '':
                            parent_scope = node.scopeName().split('/')[-1]
                            attr_scope_all = '{}/{}.{}'.format(node.scopeName(), parent_scope, attr_name)
                            attr_to_scope[node] = attr_scope_all
                            map_id_node[attr_scope_all] = count_nodes
                            make_edges_through_inputs_item(nodes[count_nodes], nodes[count_nodes], nodes_io,
                                                           unique_reverse)

                        else:
                            # If the parent node is the top-level "self" node, such as the atten::
                            attr_scope_all = '__module.{}'.format(attr_name)
                            attr_to_scope[node] = attr_scope_all
                            map_id_node[attr_scope_all] = count_nodes
                            make_edges_through_inputs_item(nodes[count_nodes], nodes[count_nodes], nodes_io,
                                                           unique_reverse)

    # made the size of root related to atten output as the size of its father or ancestor
    for node_index in nodes.keys():
        node = nodes[node_index]
        if node.parent != -1 :
            if node.type.find("aten::") != -1:
                parent = nodes[node.parent]
                while True:
                    if len(parent.outputs_size) == 0 and len(node.outputs_size) != 0:
                        for size_per in node.outputs_size:
                            parent.outputs_size.append(size_per)
                    if len(parent.inputs_size) == 0 and len(node.inputs_size) != 0:
                        for size_per in node.inputs_size:
                            parent.inputs_size.append(size_per)
                    if parent.parent == -1:
                        break
                    else:
                        parent = nodes[parent.parent]
    nodes_copy = {}
    real_count = -1
    fake_to_real_index = {}
    for node_index in nodes.keys():
        node = nodes[node_index]
        if node.is_outputed:
            real_count += 1
            node.index = real_count
            nodes_copy[real_count] = node
            fake_to_real_index[node_index] = real_count
            if node.parent != -1:
                node.parent = fake_to_real_index[node.parent]
    nodes = nodes_copy
    for edge in edges:
        edge.start = fake_to_real_index[edge.start]
        edge.end = fake_to_real_index[edge.end]

def graph(model, args, verbose=False):
    with torch.onnx.select_model_mode_for_export(model, torch.onnx.TrainingMode.EVAL):  # TODO: move outside of torch.onnx?
        try:
            trace = torch.jit.trace(model, args)
            graph = trace.graph
            torch._C._jit_pass_inline(graph)
        except RuntimeError as e:
            print(e)
            print('Error occurs, No graph saved')
            raise e

    if verbose:
        print(graph)
    parse(graph, trace, args)
    get_output_json()
    return {
        "nodes": nodes,
        "edges": edges
    }


def get_output_json(writed=False):
    import json
    nodes_json = []
    with open('test_nodes.json','w') as f:
        for node_index in nodes.keys():
            node = nodes[node_index]
            delattr(node, 'node')
            delattr(node, 'inputs')
            delattr(node, 'outputs')
            dict = {}
            dict.update(node.__dict__)
            nodes_json.append(dict)
        n_nodes = json.dumps(nodes_json, indent=4)
        print('\n')
        print('=' * 20)
        print(n_nodes)
        if writed:
            json.dump(n_nodes, f)

    edges_json = []
    with open('test_edges.json', 'w') as f:
        for edge in edges:
            dict = {}
            dict.update(edge.__dict__)
            edges_json.append(dict)
        if writed:
            json.dump(edges_json, f)