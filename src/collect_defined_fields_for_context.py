import json
import csv 

# Exported from https://docs.google.com/spreadsheets/d/1uoun-T-QcgBvUlz245RYuWvVB72vDzzQlMV8oprWEWg/edit?gid=0#gid=0
CONSENSUS_FIELDS_SHEET = "/home/ubuntu/src/ome-ld/static/OME-Core Semantic Fields - Fields.tsv"

context_ld_json_path = "/home/ubuntu/src/ome-ld/src/gen-linkml/context-manual.ld.json"

# Load the JSON-LD context file
with open(context_ld_json_path, 'r') as file:
    context_data = json.load(file)

# Access the @context field
context = context_data.get('@context')

# consensus fields from tsv
second_column_values = []
with open(CONSENSUS_FIELDS_SHEET, 'r') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        if len(row) > 1:  # Ensure there are at least two columns
            second_column_values.append(row[1])

for value in second_column_values:
    ome_schema_prefix = "http://www.openmicroscopy.org/Schemas/OME/2016-06#"
    tbd_prefix = "TBD#"
    fieldName = ""
    if value.startswith(ome_schema_prefix):
        fieldName = value.split(ome_schema_prefix)[1]
    elif value.startswith(tbd_prefix):
        fieldName = value.split(tbd_prefix)[1]
    else:
        print("Field %s does not start with OME schema prefix or TBD prefix. Skipping." % value)
        
    # Check if the field is already defined in the context
    if fieldName == "":
        continue
    if fieldName in context:
        print("Field %s is already defined in the context." % fieldName)
    else:
        context[fieldName] = ome_schema_prefix + fieldName
    
# Save the updated context
with open(context_ld_json_path, 'w') as file:
    json.dump(context_data, file, indent=4)