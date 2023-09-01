import json
import boto3
import os

def lambda_handler(event, context):

    table_name = "omit_url"

    #リクエスト情報のログ出力 
    print("===event===")
    print(event)

    print("===context===")
    print(context)

    # eventからidを取得
    id = int(event.get('pathParameters').get('id'))

    # DynamoDBからidをキーにしてデータを取得
    client = boto3.client('dynamodb')
    response = client.get_item(
        TableName=table_name,
        Key={
            'id': {
                'N': str(id)
            }
        }
    )

    print("===response===")
    print(response)

    url = response.get('Item').get('url').get('S')

    # urlへリダイレクトするhtmlを生成する
    html = f"""
    <html>
    <head>
    <meta http-equiv="refresh" content="0;URL={url}">
    </head>
    <body>
    </body>
    </html>
    """

    return {
        'statusCode': 200,
        "headers": {"Content-Type": "text/html"},
        'body': html
    }
