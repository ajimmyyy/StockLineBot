import json
import uvicorn

def lambda_handler(event, context):
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully executed!')
    }
