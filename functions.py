from anytree import Node, RenderTree, search

def make_map(list_child_parent):
    has_parent = set()
    all_items = {}
    
    for child, parent in list_child_parent:
        if parent not in all_items:
            all_items[parent] = {}
            
        if child not in all_items:
            all_items[child] = {}
        
        all_items[parent][child] = all_items[child]
        has_parent.add(child)

    result = {}
    
    for key, value in all_items.items():
        if key not in has_parent:
            result[key] = value
    
    return result

def createTree(tree_dict, root):
    for key, item in tree_dict.items():
        child = Node(key, parent=root)

        if tree_dict[key] != '':
            createTree(tree_dict[key], child)
        else:
            return          
        
def traceConversation(dataframe, tree, node):
    # parent = search.find_by_attr(tree, node).children
    
    print("All child nodes:")
    children_nodes_list = getAllChildNodes(tree, node, [])
    
    return dataframe[(dataframe['reply_to'].isin(children_nodes_list)) | (dataframe['id'].isin(children_nodes_list + [node]))]

def getAllChildNodes(tree, node, children_nodes_list):
    children_nodes = search.find_by_attr(tree, node).children
    
    for i in children_nodes:
        print(i.name)
        children_nodes_list.append(i.name)
        
        if i.children != None:
            getAllChildNodes(tree, i.name, children_nodes_list)
            
        else:
            return
            
    return children_nodes_list

def confirmationBiasScore(scores, current_score, threshold = 0.5):
    positive_evidence = 0
    negative_evidence = 0
    agree = 0
    disagree = 0
    
    for i in range(len(scores)):
        if scores[i] < threshold:
            negative_evidence += 1
            
            if i < len(scores) - 1 and scores[i+1] >= threshold:
                disagree += 1
            else:
                agree += 1
        else:
            positive_evidence += 1
            
            if i < len(scores) - 1 and scores[i+1] < threshold:
                disagree += 1
            else:
                agree += 1
    
    H1 = agree / (agree + disagree)
    H2 = disagree / (agree + disagree)
            
    # Assume D1 is positive evidence
    D1 = positive_evidence / (positive_evidence + negative_evidence)
    D2 = negative_evidence / (positive_evidence + negative_evidence)
    
#     print('H1', H1, agree)
#     print('H2', H2, disagree)
#     print('D1', D1, positive_evidence)
#     print('D2', D2, negative_evidence)
    
    try:
        prob_D1_H1 = (D1 * H1) / ((D1 * H1) + (D2 * H1))
    except:
        prob_D1_H1 = 0
        
    try:
        prob_D1_H2 = (D1 * H2) / ((D1 * H2) + (D2 * H2))
#         prob_D1_H2 = (D2 * H2) / ((D2 * H2) + (D1 * H2))
    except:
        prob_D1_H2 = 0
    
    return prob_D1_H1, prob_D1_H2    