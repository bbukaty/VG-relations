// Load data into window
subjects = null;
d3.json("<subjects_all.json hosting link>", function(error, json) {
    if (error != null) {
        console.log(error);
        return;
    }
    subjects = json;
    
    document.getElementById('loader').remove();
    document.getElementById('subjInput').style.visibility = 'visible';
    // example chart
    createSankey('kiwi');
});


/* Get input from the subject form and prevent default form behavior */
function captureForm() {
    createSankey(document.getElementById('subject').value);
    return false;
}

/* Accepts a dict of dicts of dicts, etc... of numbers.
Returns the sum of all the 'leaf node' numbers in this data structure. */ 
function sumBranches(obj) {
    var total = 0;
    if (typeof obj == 'number') {
        return obj;
    } else {
        total = 0
        for (var key in obj) {
            total += sumBranches(obj[key]);
        }
        return total;
    }
}

/* Given a subject name and an optional relation name, generates data for a
Sankey visualization and displays it in the page. */
function createSankey(subjName, relName=null) {
    if (!(subjName in subjects)) {
        document.getElementById('loadError').style.visibility='visible';
        return;
    }
    // reset the error message on successful submission
    document.getElementById('loadError').style.visibility='hidden';
    if (relName == null) {
        sankeyData = genSubjData(subjName, subjects[subjName]);
    } else {
        sankeyData = genSubjRelData(subjName, relName, subjects[subjName]);
    }

    displaySankey(sankeyData);
}

/* Takes in a subject name and its corresponding dict of relations.
Generates lists of nodes and links for a Sankey diagram. */ 
function genSubjData(subjName, subj) {
    var nodes = [{ name: subjName, type: 'subj' }];
    var links = [];

    // keep track of indices of objects and relations so we can link things
    var relIndices = {};
    var objIndices = {};
    currIndex = 1;

    topRels = Object.keys(subj).sort(function(a,b){
        return sumBranches(subj[b])-sumBranches(subj[a]);
    }).slice(0,30);
    topRels.forEach(function (relName) {
        relIndices[relName] = currIndex;
        currIndex++;
        nodes.push({ name: relName, type: 'rel' });
        links.push({
            source: 0,
            target: relIndices[relName],
            value: sumBranches(subj[relName])
        });
        topObjs = Object.keys(subj[relName]).sort(function(a,b){
            return subj[relName][b] - subj[relName][a];
        }).slice(0,4);
        topObjs.forEach(function (objName) {
            if (!(objName in objIndices)) {
                objIndices[objName] = currIndex;
                nodes.push({ name: objName, type: 'obj' });
                currIndex++;
            }
            links.push({
                source: relIndices[relName],
                target: objIndices[objName],
                value: subj[relName][objName]
            });
        });
    })
    return { nodes: nodes, links: links };
}

/* Takes in a subject name, a relation name, and its corresponding dict of relations.
Generates lists of nodes and links for a Sankey diagram (focused on the relation). */ 
function genSubjRelData(subjName, relName, subj) {
    var nodes = [{ name: subjName, type: 'subj' },
                 { name: relName, type: 'rel' }];
    var links = [{ source: 0, target: 1, value: sumBranches(subj[relName]) }];

    topObjs = Object.keys(subj[relName]).sort(function(a,b){
            return subj[relName][b] - subj[relName][a];
        }).slice(0, 30);
    topObjs.forEach(function (objName) {
        nodes.push({ name: objName, type: 'obj' });
        links.push({
            source: 1,
            target: nodes.length-1,
            value: subj[relName][objName]
        });
    });

    return { nodes: nodes, links: links }
}

/* Draws the diagram and initializes click handlers and tooltips. */
function displaySankey(sankeyData) {
    d3.select("svg").remove(); // clear existing chart
    var chart = d3.select("#chart").append("svg").chart("Sankey.Path");
    chart
        .colorLinks('#a0a0a0')
        .nodeWidth(20)
        .spread(true)
        .on('node:click', function(node) {
            if (node.type == 'rel') {
                createSankey(sankeyData.nodes[0].name, node.name);
            } else {
                createSankey(node.name);
            }
        })
        .on('link:click', function(link) {
            if (link.source.type == 'subj') {
                createSankey(link.source.name, link.target.name);
            } else {
                createSankey(link.target.name);
            }
        })
        .draw(sankeyData);
    // add tooltips to links
    d3.select("svg").selectAll(".link").append("title").text(function(link) {
        return link.source.name + " → " + link.target.name + "\n" + link.value + " occurrences"
    });
}