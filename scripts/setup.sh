#!/bin/bash

printf "Downloading Visual Genome relations data...\n\n"
wget https://visualgenome.org/static/data/dataset/relationships.json.zip
mkdir data
unzip relationships.json.zip -d data
rm relationships.json.zip

printf "Processing data...\n"
python scripts/count_relations.py
printf "Done."