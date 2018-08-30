# VG-relations
Visual Genome Relationship Visualization  
Hosted at (Visual Genome Link)

This is a tool for visualizing the frequency of object relationships in the Visual Genome dataset.

![Visualization Example](kiwi.gif)

It was built with [this d3 Sankey diagram library.](https://github.com/q-m/d3.chart.sankey)

# Data Processing
For this visualization, I tallied up all the relations in all the images in Visual Genome into this JSON format:
```
{
    "subject": {
        "relation": { "object": occurrences }
    }
}
```
Example:
```
{
    "person": {
        "wears": { "backpack": 12, "hat": 10 },
        "eats": { "pizza": 9 }
    },
    "plate": {
        "on": { "table": 5, "placemat": 3 }
    }
}
```
I found this data format interesting as it potentially suggests a method for commonsense inference on visual data using priors from this dataset. For example, 'what kinds of objects usually contain food? → bowls, plates, table'.

# Installation
Clone or download the repository, then download the relation data from the Visual Genome Dataset [here](https://visualgenome.org/static/data/dataset/relationships.json.zip).  
In the main project directory, make a directory called `data` and extract `relationships.json` there.

Next, run `python scripts/count_relations.py`. This creates a `data/subjects` directory populated with a json file for every object in Visual Genome.  
This prevents us from needing to load a really large file into our explorer every time we want to use it.

You should now be able to open `explorer.html` in your web browser of choice (I used Chrome).

# Navigation
Type an item into the search bar and hit submit to see relations in which the item was the subject.  
From there, click on any object node to see relationships in which that object was the subject.  
Additionally, click on a subject → relation link to narrow your focus to that relation and show additional objects.

If you found this useful or interesting, feel free to extend the visualization with new functionality, or use the processed data in another interesting way!
