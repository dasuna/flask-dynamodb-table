from flask import Flask, request, render_template
import boto3

app = Flask(__name__)


@app.route('/') 
def index():
    return render_template("index.html")
    #return 'Hello, World!'


@app.route('/create') 
def create_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.create_table(
        TableName='StudentDetails',
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


@app.route('/update') 
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



@app.route('/update-via-form', methods=["POST"]) 
def update_table_via_form():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('StudentDetails')
    
    # Get the data from the request body
    data = request.form.to_dict()
    table.put_item(Item=data)

    
    return "Sucessfully updated"
    
    
if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
