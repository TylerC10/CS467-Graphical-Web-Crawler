### D3 tree data structure generator 
### Logic is implemented server size becaue it's much easier to create/traverse trees in Python than JavaScript

def create_d3_tree_datastructure(data):
    # First, lets create a tuple with the raw data in to fit [(id,parent),(id,parent),(id,parent),(id,parent)]
    list_tuple_id_pid = []
    for link in data:
        # If parent_id = None, then its the root, assign id
        if link['parent_id'] == None:
            list_tuple_id_pid.append((link['id'],link['id']))
        else:
            # Create a regular id,parent tuple
            list_tuple_id_pid.append((link['id'],link['parent_id']))
    # From the list of tuples get the highest id to determin 'last url' (needed to highlight on D3) 
    from operator import itemgetter
    last_url_id = min(list_tuple_id_pid,key=itemgetter(1))[0]

    # We have a proper tree structure pattern as a list
    # Next, lets create a nodes dictionary list in preparation for the required tree data for D3
    nodes = {}
    for i in list_tuple_id_pid:
        id, parent_id = i
        nodes[id] = { 'id': id }

    # Finally create tree's or tree's
    trees = []
    
    for i in list_tuple_id_pid:
        id, parent_id = i
        node = nodes[id]
        # Now that we're in the final loop, append the url each node since no more processing will be done on the data
        node['url'] = filter(lambda link: link['id'] == nodes[id]['id'], data)[0]['url']
        # Also check if its the last_url_id to add last_url flag
        if nodes[id]['id'] == last_url_id:
            node['last_url'] = 'last_url'
        # either make the node a new tree or link it to its parent
        if id == parent_id:
            # start a new tree in the parent tree        
            trees.append(node)
        else:
            # add new node as child to parent
            parent = nodes[parent_id]
            if not 'children' in parent:
                # ensure parent has a 'children' field
                parent['children'] = []
            children = parent['children']
            children.append(node)
    #Edge case for single trees to display correctly on D3
    if 'children' not in trees[0]:
        trees[0]['children'] = []
    return trees
