# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class LambdaPermissionProperties(TypedDict):
    Action: Optional[str]
    FunctionName: Optional[str]
    Principal: Optional[str]
    EventSourceToken: Optional[str]
    FunctionUrlAuthType: Optional[str]
    Id: Optional[str]
    PrincipalOrgID: Optional[str]
    SourceAccount: Optional[str]
    SourceArn: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class LambdaPermissionProvider(ResourceProvider[LambdaPermissionProperties]):
    TYPE = "AWS::Lambda::Permission"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[LambdaPermissionProperties],
    ) -> ProgressEvent[LambdaPermissionProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - FunctionName
          - Action
          - Principal

        Create-only properties:
          - /properties/SourceAccount
          - /properties/FunctionUrlAuthType
          - /properties/SourceArn
          - /properties/Principal
          - /properties/Action
          - /properties/FunctionName
          - /properties/EventSourceToken
          - /properties/PrincipalOrgID

        Read-only properties:
          - /properties/Id


        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_

        params = util.select_attributes(
            model=model, params=["FunctionName", "Action", "Principal", "SourceArn"]
        )

        params["StatementId"] = util.generate_default_name(
            request.stack_name, request.logical_resource_id
        )

        response = lambda_client.add_permission(**params)

        parsed_statement = json.loads(response["Statement"])
        model["Id"] = parsed_statement["Sid"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[LambdaPermissionProperties],
    ) -> ProgressEvent[LambdaPermissionProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[LambdaPermissionProperties],
    ) -> ProgressEvent[LambdaPermissionProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_
        try:
            lambda_client.remove_permission(
                FunctionName=model.get("FunctionName"), StatementId=model["Id"]
            )
        except lambda_client.exceptions.ResourceNotFoundException:
            pass

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[LambdaPermissionProperties],
    ) -> ProgressEvent[LambdaPermissionProperties]:
        """
        Update a resource


        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_

        if not model.get("Id"):
            model["Id"] = request.previous_state["Id"]

        params = util.select_attributes(
            model=model, params=["FunctionName", "Action", "Principal", "SourceArn"]
        )

        lambda_client.remove_permission(
            FunctionName=model.get("FunctionName"), StatementId=model["Id"]
        )
        lambda_client.add_permission(StatementId=model["Id"], **params)

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )
