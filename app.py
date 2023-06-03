from flask import Flask, request, render_template
import boto3

app = Flask(__name__)


@app.route('/') 
def index():
    return render_template("index.html")
    #return 'Hello, World!'


@app.route('/create-table', methods=["POST"]) 
def create_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = request.form["tableName"]

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'regNo',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'name',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'regNo',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Table status:", table.table_status)
    return "Data written successfully"


@app.route('/put-item') 
def update_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('StudentDetails')
    item = {
      'regNo': '001',
      'name': 'Jane',
      'age': 26
    }
    
    table.put_item(Item=item)
    
    return "Sucessfully updated"



@app.route('/put-via-form', methods=["POST"]) 
def update_table_via_form():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('student') # replace 'student' with whatever your table name
    
    # Get the data from the request body
    data = request.form.to_dict()
    # Put the item to the database
    table.put_item(Item=data)

    
    return "Sucessfully updated"
    
    
if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
