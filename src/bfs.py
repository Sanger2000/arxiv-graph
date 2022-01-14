import json
from utils import get_data

def bfs(starting_id, out_file="outfile.json"):
    leaf_nodes = [starting_id]

    num_iters = 1e5

    all_data = []
    id_to_idx = {}
    childless_parents = defaultdict(list)


    for epoch in tqdm.tqdm(num_iters):
        next_leaf_nodes = set()
        for leaf_node in leaf_nodes:
            # Get all the data for a json blob from this leaf node
            data = get_data(leaf_node)

            # Set the appropriate index for this. Also once we visit a node
            # we will remember it
            id_to_idx[data["arxiv-id"]] = len(all_data)

            # Now that we are on the childless parent, we add in their
            # children
            data["children"].extend(childless_parents[leaf_node])

            # add the data to the list
            all_data.append(data)

            # Next we follow the edges in this BFS
            parents = data["parents"]

            for parent in parents:
                if parent not in id_to_idx:
                    # If the parent has not yet been seen, we
                    childless_parents[parent].append(leaf_node)
                else:
                    # If the parent has been seen before, we update it with a new child
                    all_data[id_to_idx[parent]]["children"].append(leaf_node)

            next_leaf_nodes.update([child for child in children if child not in visited])

        print(epoch, "Saving new Graph")
        with open(out_file, "w") as f:
            json.dump(all_data, f)

        with open("tmp.json", "w") as f:
            json.dump(all_data, f)


