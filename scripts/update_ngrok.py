import boto3
import os


def _check_valid_aws_response(response: dict) -> bool:
    if not response:
        return False
    status = response.get('integrationResponses', None)
    if status:
        if '200' not in status.keys():
            print(f'Rest API Update response codes: {status.keys()}')
            return False
    return True


def update_rest_api_uri(new_uri: str) -> bool:
    """
    :param new_uri: The url to forward request to
    :env BUILD_STATUS_AWS_REST_API_ID: AWS ID of an API Gateway's Rest API
    :env BUILD_STATUS_AWS_RESOURCE_ID: AWS ID of Route used to forward ('/' or '/<route>')
    :env BUILD_STATUS_AWS_STAGE_NAME: AWS Stage Name for stage to deploy your API on
    :env BUILD_STATUS_METHOD: Method used during forwarding
    :return: True if update was successful, otherwise False
    """
    if not new_uri:
        return False

    rest_api_id = os.environ.get('BUILD_STATUS_AWS_REST_API_ID', None)
    resource_id = os.environ.get('BUILD_STATUS_AWS_RESOURCE_ID', None)
    stage_name = os.environ.get('BUILD_STATUS_AWS_STAGE_NAME', None)
    http_method = os.environ.get('BUILD_STATUS_METHOD', None)
    client = boto3.client('apigateway')

    if not rest_api_id or not stage_name or not resource_id or not http_method:
        raise EnvironmentError('Must provide rest api id, method resource id, stage name, and http method')

    try:
        response = client.update_integration(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/uri',
                    'value': new_uri
                },
            ]
        )
        _check_valid_aws_response(response)

        response = client.create_deployment(
            restApiId=rest_api_id,
            stageName=stage_name
        )

        _check_valid_aws_response(response)
    except Exception as e:
        print(e)
        return False

    print(f'Updated API Gateway ({resource_id}) {http_method} route to forward to {new_uri}')
    return True

