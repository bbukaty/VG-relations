"""
Parses through all the subject-relation-object relationships in Visual Genome and counts relations and objects relative to a given subject. Outputs a json file for 

Output format example (person.json):
{
    "wears": { "backpack": 12, "hat": 10 },
    "eats": { "corn": 9 }
}
"""

import json
import os
import argparse

'''
Deal with some idiosyncrasies in Visual Genome, lowercase everything.
Returns subject, relation, object strings.
'''
def get_triplet(relationship):
    try:
        subj_name = relationship['subject']['names'][0]
    except KeyError:
        subj_name = relationship['subject']['name']
    try:
        obj_name = relationship['object']['names'][0]
    except:
        obj_name = relationship['object']['name']
    return subj_name.lower(), relationship['predicate'].lower(), obj_name.lower()

def main(args):
    print("Loading data...")
    try:
        with open(args.input) as f:
            data = json.load(f)
        print("Done")
    except:
        print("Error loading data. Exiting.")
        exit()
    
    subjects = {}
    for image in data:
        for relationship in image['relationships']:
            subj_name, rel_name, obj_name = get_triplet(relationship)
            
            subj = subjects.get(subj_name, {})
            rel = subj.get(rel_name, {})
            rel[obj_name] = rel.get(obj_name, 0) + 1
            subj[rel_name] = rel
            subjects[subj_name] = subj
    
    # Output data
    with open('{}/subjects_all.json'.format(args.output_dir), 'w') as f:
        json.dump(subjects, f)
    
    subjects_dir = '{}/subjects/'.format(args.output_dir)
    if not os.path.exists(subjects_dir):
        os.makedirs(subjects_dir)
        
    for subj_name, subject in subjects.iteritems():
        try:
            with open('{}/{}.json'.format(subjects_dir, subj_name), 'w') as f:
                json.dump(subject, f)
        # subject name is something wonky so we can't name a file after it /shrug
        except (IOError, UnicodeEncodeError) as e:
            pass
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default='data/relationships.json',
                        help="JSON file containing VG relationship annotations")
    parser.add_argument('--output-dir', type=str, default='data',
                        help="Where to store the tallied output")

    args = parser.parse_args()
    main(args)