"""
NO LONGER IN USE - this is now done in javascript, which can be seen in explorer.html.
I figured I'd leave it in case it ends up being useful.

Sankey diagram expects list of nodes + list of edges between nodes.
The edges are specified by source and target indices in the list of nodes.
This script converts the VG relation dict structure into that format for a given subject.
"""

import json
import argparse


"""Takes a tree-style dict of strings to strings to strings... to numbers.
Returns the sum of all the leaf node numbers."""
def sum_branches(input_dict):
    total = 0
    for k, v in input_dict.iteritems():
        if type(v) is dict:
            total += sum_branches(v)
        else:
            total += v
    return total

def gen_sankey_data(subj_name, subj):
    nodes = [{ "name":  subj_name }]
    links = []

    # dicts mapping object and relation names to the index of their corresponding nodes
    rel_indices, obj_indices = {}, {}
    curr_index = 1
    top_rels = sorted(subj.keys(), key=lambda rel: sum_branches(subj[rel]), reverse=True)[:args.top_k]
    for rel_name in top_rels:
        rel_indices[rel_name] = curr_index
        curr_index += 1
        nodes.append({ "name": rel_name })
        links.append({
            "source": 0,
            "target": rel_indices[rel_name],
            "value": sum_branches(subj[rel_name])
        })
        top_objs = sorted(subj[rel_name].keys(), key=subj[rel_name].get, reverse=True)[:4]
        for obj_name in top_objs:
            if obj_name not in obj_indices:
                obj_indices[obj_name] = curr_index
                nodes.append({ "name": obj_name })
                curr_index += 1
            links.append({
                "source": rel_indices[rel_name],
                "target": obj_indices[obj_name],
                "value": subj[rel_name][obj_name]
            })
    return nodes, links

def main(args):
    print "Loading data..."
    try:
        with open(args.input) as f:
            data = json.load(f)
        print "Done"
    except:
        print "Error loading data. Exiting."
        exit()
    
    subjects = data['subjects']
    objects = data['objects']
    
    for subj_name, subj in subjects.iteritems():
        nodes, links = gen_sankey_data(subj_name, subj)
        
#         print "There will be {} nodes in the resulting sankey diagram.".format(len(nodes))
#         print "Outputting JSON..."
        output = { "nodes": nodes, "links": links }
        try:
            with open('data/subjects/{}.json'.format(subj_name), 'w') as o:
    #             with open(args.output, 'w') as o:
                json.dump(output, o)
    #             print "Done."
        except IOError:
            pass
        except UnicodeEncodeError:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default='data/vg_relations.json',
                        help="JSON file containing VG relation counts")
#     parser.add_argument('--output', type=str, required=True,
#                         help="Where to store the filtered output")
    parser.add_argument('--top-k', type=int, default=30,
                        help="Where to store the filtered output")

    args = parser.parse_args()
                          
    main(args)