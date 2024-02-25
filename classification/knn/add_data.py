import weaviate

# Training and data to classify
training_data = [
    # ...
]

data_to_classify = [
    # ...
]

# Sentiments
sentiments = [
    "positive",
    "neutral",
    "negative"
]

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")

# Clear existing schema
client.schema.delete_all()

# Define Sentiment class
sentiments_class = {
    "class": 'Sentiment',
    "description": 'sentiment',  
    "properties": [
        {
            "dataType": [ 'text'],
            "description": 'name of sentiment',
            "name": 'name',
        }
    ]
}

# Create Sentiment class if it doesn't exist
if not client.schema.exists("Sentiment"):
    client.schema.create_class(sentiments_class)
    print("#### ADDING Sentiments")
    # Add sentiment categories
    client.batch.configure(batch_size=100)  # Configure batch
    with client.batch as batch:
        for item in sentiments:
            item_id = batch.add_data_object({"name": item}, "Sentiment", weaviate.util.generate_uuid5(item))
            print(item, item_id)

# Define Comment class
comment_class = {
    "class": 'Comment',
    "description": 'comment',  
    "properties": [
        {
            "name": 'body',
            "description": 'comment text',
            "dataType": [ 'text'],
        },
        {
            "name": 'trained_sentiment',
            "description": 'sentiment provided and mapped',
            "dataType": [ 'text'],
        },
        {
            "name": 'sentiment',
            "description": 'comment sentiment',
            "dataType": ["Sentiment"],
        }
    ]
}

# Create Comment class if it doesn't exist
if not client.schema.exists("Comment"):
    client.schema.create_class(comment_class)
    print("#### ADDING Training Comments")
    client.batch.configure(batch_size=5)  # Configure batch
    # Map relations to add later
    relations = []
    with client.batch as batch:
        for item in training_data:
            print(item)
            item_id = batch.add_data_object(
                {"body": item["text"]}, "Comment"
            )
            # Save relations to add later
            relations.append(
                [item_id, weaviate.util.generate_uuid5(item["sentiment"])]
            )
    # Add relations
    for relation in relations:
        print("ADDING RELATION", relation)
        reference = client.data_object.reference.add(
            from_class_name="Comment",
            from_uuid=relation[0],
            from_property_name="sentiment",
            to_class_name="Sentiment",
            to_uuid=relation[1],
        )

    print("#### ADDING Non Classificated Comments")
    client.batch.configure(batch_size=5)  # Configure batch
    # Map relations to add later
    relations = []
    with client.batch as batch:
        for item in data_to_classify:
            print(item)
            item_id = batch.add_data_object(
                {"body": item["text"]}, "Comment"
            )
            # Save relations to add later
            relations.append(
                [item_id, weaviate.util.generate_uuid5(item["sentiment"])]
            )

# Check data
print("#### OUR DATA SHOULD BE IMPORTED")
client.query.get("Comment", "body sentiment{... on Sentiment{name}}").do()

# Schedule classification
classification_status = (
    client.classification.schedule()
    .with_type("knn")
    .with_class_name("Comment")
    .with_based_on_properties(["body"])
    .with_classify_properties(["sentiment"])
    .with_settings({"k": 3})
    .do()
)
print("CLASSIFICATION STATUS: ", classification_status)

# Check classified data
results = client.query.get(
    "Comment", "body sentiment{... on Sentiment{name}}"
).with_additional(
    "classification{basedOn classifiedFields completed id scope}"
).do()

print("DATA CLASSIFIED", results)
