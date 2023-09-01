import json
import boto3

def lambda_handler(event, context):

    table_name = "omit_url"

    #リクエスト情報のログ出力 
    print("===event===")
    print(event)

    print("===context===")
    print(context)

    # eventからurlを取得
    url = json.loads(event.get('body')).get('url')
    print("===url===")
    print(url)

    # DynamoDBからid(プライマリキー)の最大値を取得
    client = boto3.client('dynamodb')
    response = client.scan(
        TableName=table_name,
        Select='COUNT'
    )

    print("===response===")
    print(response)

    count = int(response.get('Count'))+1

    # DynamoDBにデータを登録
    response = client.put_item(
        TableName=table_name,
        Item={
            'id': {
                'N': str(count)
            },
            'url': {
                'S': url
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f"success: {count}")
    }
