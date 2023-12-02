from requests import Session

from gsoc2.models.api import GetSecretsDTO, SecretsResponse


def get_secrets_req(api_request: Session, options: GetSecretsDTO) -> SecretsResponse:
    """Send request again Gsoc2 API to fetch secrets.
    See more information on https://soc2.khulnasoft.com/docs/api-reference/endpoints/secrets/read

    :param api_request: The :class:`requests.Session` instance used to perform the request
    :param workspace_id: The ID of the workspace
    :param environment: The environment
    :return: Returns the API response as-is
    """

    response = api_request.get(
        "/api/v3/secrets",
        params={
            "environment": options.environment,
            "workspaceId": options.workspace_id,
            "secretPath": options.path,
            "include_imports": str(options.include_imports).lower()
        },
    )
    data = SecretsResponse.parse_obj(response.json())

    return (data.secrets if data.secrets else [], data.imports if data.imports else [])

