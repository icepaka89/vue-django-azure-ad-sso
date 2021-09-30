import requests
import json

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
    '''
    Sends a request to ther /me endpoint of the MS Graph API with the
    given access token as the bearer token header, and returns the 
    response. If the access token is valid, this endpoint will return
    a user object
    '''
    # Send GET to /me
    user = requests.get(
    '{0}/me'.format(graph_url),
    headers={
        'Authorization': 'Bearer {0}'.format(token)
    },
    params={
        '$select': 'displayName,userPrincipalName'
    })

    # Return the JSON result
    return user.json()
