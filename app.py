from flask import Flask, request, render_template
import boto3

app = Flask(__name__)


@app.route('/') 
def index():
    return render_template("index.html")


@app.route('/create-table', methods=["POST"]) 
def create_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = request.form["tableName"]
    partition_key = request.form["partitionKey"]
    sort_key = request.form["sortKey"]

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': partition_key,
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': sort_key,
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': partition_key,
                'AttributeType': 'S'
            },
            {
                'AttributeName': sort_key,
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    # Wait until the table is created
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    # Check the table status
    if table.table_status == 'ACTIVE':
        return f"Table '{table_name}' created successfully"
    else:
        return f"Error creating table. Table status: {table.table_status}"

    
if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
