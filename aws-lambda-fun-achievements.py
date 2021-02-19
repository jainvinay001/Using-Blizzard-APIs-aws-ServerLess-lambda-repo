import json
import boto3
import requests
import datetime

# create a boto3 object
dynamodb = boto3.resource('dynamodb')

# define a function authenticate and create access token for access player achievements in world of warcarft 

def create_access_token(client_id, client_secret, region, realmSlug, characterName):
   
    data = {'grant_type': 'client_credentials'}
    
    response = requests.post('https://%s.battle.net/oauth/token' %
                             region, data=data, auth=(client_id, client_secret))
    response = response.json()
    
    # use access token, realmSlug and characterName for fetching all achievements of the player
    
    result = requests.get('https://{reg}.api.blizzard.com/profile/wow/character/{slug}/{name}/achievements?namespace=profile-us&locale=en_US&access_token={access_token}'.format(
        reg=region, slug=realmSlug, name=characterName, access_token=response['access_token']))
    
    return result.json()

# open a gameclient table for insert result of achievements of the player in gameclient table
# table = dynamodb.Table('gameclient')

# define lambda handler for handle the serverless rest api event
def lambda_handler(event, context):
    #battle.net CLIENT_ID and CLIENT_SECRET
    YOUR_CLIENT_ID = event['CLIENT_ID']
    YOUR_CLIENT_SECRET = event['CLIENT_SECRET']
    
    # use url body data build with get and post method event["queryStringParameters"]['queryparam1'] or event['pathParameters']['param1']
    region=event['region']
    realmSlug=event['realmSlug']
    characterName=event['characterName']
    
    #calling create_access_token function 
    result = create_access_token(
        YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, region, realmSlug, characterName)
    # table attributes     
    # trans = {}
    # trans['playerName'] = 'sicarious'
    # trans['reteievedAt'] = str(datetime.datetime.now())
    # trans['slug'] = 'executus'
    # trans['total_quantity'] = result['total_quantity']
    # trans['total_points'] = result['total_points']
    # trans['achievements'] = result['achievements']
    # print(event)
    # insert a data in dynamodb table
    # response = table.put_item(Item=trans)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(result['achievements'])

    }
