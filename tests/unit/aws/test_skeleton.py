from typing import Dict, List, TypedDict

from botocore.parsers import create_parser

from localstack.aws.api import RequestContext, ServiceException, handler
from localstack.aws.skeleton import Skeleton
from localstack.aws.spec import load_service

""" Stripped down version of the SQS API generated by the Scaffold. """

String = str
StringList = List[String]

Binary = bytes
BinaryList = List[Binary]
Integer = int


class MessageAttributeValue(TypedDict):
    StringValue: String
    BinaryValue: Binary
    StringListValues: StringList
    BinaryListValues: BinaryList
    DataType: String


class MessageSystemAttributeName(str):
    SenderId = "SenderId"
    SentTimestamp = "SentTimestamp"
    ApproximateReceiveCount = "ApproximateReceiveCount"
    ApproximateFirstReceiveTimestamp = "ApproximateFirstReceiveTimestamp"
    SequenceNumber = "SequenceNumber"
    MessageDeduplicationId = "MessageDeduplicationId"
    MessageGroupId = "MessageGroupId"
    AWSTraceHeader = "AWSTraceHeader"


class MessageSystemAttributeNameForSends(str):
    AWSTraceHeader = "AWSTraceHeader"


class SendMessageResult(TypedDict):
    MD5OfMessageBody: String
    MD5OfMessageAttributes: String
    MD5OfMessageSystemAttributes: String
    MessageId: String
    SequenceNumber: String


class MessageSystemAttributeValue(TypedDict):
    StringValue: String
    BinaryValue: Binary
    StringListValues: StringList
    BinaryListValues: BinaryList
    DataType: String


MessageBodyAttributeMap = Dict[String, MessageAttributeValue]
MessageSystemAttributeMap = Dict[MessageSystemAttributeName, String]
MessageBodySystemAttributeMap = Dict[
    MessageSystemAttributeNameForSends, MessageSystemAttributeValue
]


class InvalidMessageContents(ServiceException):
    pass


class UnsupportedOperation(ServiceException):
    pass


class TestSqsApi:
    service = "sqs"
    version = "2012-11-05"

    @handler("SendMessage")
    def send_message(
        self,
        context: RequestContext,
        queue_url: String,
        message_body: String,
        delay_seconds: Integer = None,
        message_attributes: MessageBodyAttributeMap = None,
        message_system_attributes: MessageBodySystemAttributeMap = None,
        message_deduplication_id: String = None,
        message_group_id: String = None,
    ) -> SendMessageResult:
        return {
            "MD5OfMessageBody": "String",
            "MD5OfMessageAttributes": "String",
            "MD5OfMessageSystemAttributes": "String",
            "MessageId": "String",
            "SequenceNumber": "String",
        }


class TestSqsApiNotImplemented:
    service = "sqs"
    version = "2012-11-05"

    @handler("SendMessage")
    def send_message(
        self,
        context: RequestContext,
        queue_url: String,
        message_body: String,
        delay_seconds: Integer = None,
        message_attributes: MessageBodyAttributeMap = None,
        message_system_attributes: MessageBodySystemAttributeMap = None,
        message_deduplication_id: String = None,
        message_group_id: String = None,
    ) -> SendMessageResult:
        raise NotImplementedError


""" Test implementations """


def test_skeleton_e2e_sqs_send_message():
    sqs_service = load_service("sqs")
    skeleton = Skeleton(sqs_service, TestSqsApi())
    context = RequestContext()
    context.account = "test"
    context.region = "us-west-1"
    context.service = sqs_service
    context.request = {
        "method": "POST",
        "path": "/",
        "body": "Action=SendMessage&Version=2012-11-05&QueueUrl=http%3A%2F%2Flocalhost%3A4566%2F000000000000%2Ftf-acc-test-queue&MessageBody=%7B%22foo%22%3A+%22bared%22%7D&DelaySeconds=2",
        "headers": {
            "Remote-Addr": "127.0.0.1",
            "Host": "localhost:4566",
            "Accept-Encoding": "identity",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "aws-cli/1.20.47 Python/3.8.10 Linux/5.4.0-88-generic botocore/1.21.47",
            "X-Amz-Date": "20211009T185815Z",
            "Authorization": "AWS4-HMAC-SHA256 Credential=test/20211009/us-east-1/sqs/aws4_request, SignedHeaders=content-type;host;x-amz-date, Signature=d9f93b13a07dda8cba650fba583fab92e0c72465e5e02fb56a3bb4994aefc339",
            "Content-Length": "169",
            "x-localstack-request-url": "http://localhost:4566/",
            "X-Forwarded-For": "127.0.0.1, localhost:4566",
        },
    }
    result = skeleton.invoke(context)

    # Use the parser from botocore to parse the serialized response
    response_parser = create_parser(sqs_service.protocol)
    parsed_response = response_parser.parse(
        result, sqs_service.operation_model("SendMessage").output_shape
    )

    # Test the ResponseMetadata and delete it afterwards
    assert "ResponseMetadata" in parsed_response
    assert "RequestId" in parsed_response["ResponseMetadata"]
    assert len(parsed_response["ResponseMetadata"]["RequestId"]) == 52
    assert "HTTPStatusCode" in parsed_response["ResponseMetadata"]
    assert parsed_response["ResponseMetadata"]["HTTPStatusCode"] == 200
    del parsed_response["ResponseMetadata"]

    # Compare the (remaining) actual payload
    assert parsed_response == {
        "MD5OfMessageBody": "String",
        "MD5OfMessageAttributes": "String",
        "MD5OfMessageSystemAttributes": "String",
        "MessageId": "String",
        "SequenceNumber": "String",
    }


def test_skeleton_e2e_sqs_send_message_not_implemented():
    sqs_service = load_service("sqs")
    skeleton = Skeleton(sqs_service, TestSqsApiNotImplemented())
    context = RequestContext()
    context.account = "test"
    context.region = "us-west-1"
    context.service = sqs_service
    context.request = {
        "method": "POST",
        "path": "/",
        "body": "Action=SendMessage&Version=2012-11-05&QueueUrl=http%3A%2F%2Flocalhost%3A4566%2F000000000000%2Ftf-acc-test-queue&MessageBody=%7B%22foo%22%3A+%22bared%22%7D&DelaySeconds=2",
        "headers": {
            "Remote-Addr": "127.0.0.1",
            "Host": "localhost:4566",
            "Accept-Encoding": "identity",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "aws-cli/1.20.47 Python/3.8.10 Linux/5.4.0-88-generic botocore/1.21.47",
            "X-Amz-Date": "20211009T185815Z",
            "Authorization": "AWS4-HMAC-SHA256 Credential=test/20211009/us-east-1/sqs/aws4_request, SignedHeaders=content-type;host;x-amz-date, Signature=d9f93b13a07dda8cba650fba583fab92e0c72465e5e02fb56a3bb4994aefc339",
            "Content-Length": "169",
            "x-localstack-request-url": "http://localhost:4566/",
            "X-Forwarded-For": "127.0.0.1, localhost:4566",
        },
    }
    result = skeleton.invoke(context)

    # Use the parser from botocore to parse the serialized response
    response_parser = create_parser(sqs_service.protocol)
    parsed_response = response_parser.parse(
        result, sqs_service.operation_model("SendMessage").output_shape
    )

    # Test the ResponseMetadata
    assert "ResponseMetadata" in parsed_response
    assert "RequestId" in parsed_response["ResponseMetadata"]
    assert len(parsed_response["ResponseMetadata"]["RequestId"]) == 52
    assert "HTTPStatusCode" in parsed_response["ResponseMetadata"]
    assert parsed_response["ResponseMetadata"]["HTTPStatusCode"] == 501

    # Compare the (remaining) actual eror payload
    assert "Error" in parsed_response
    assert parsed_response["Error"] == {
        "Code": "InternalFailure",
        "Message": "API action 'SendMessage' for service 'sqs' not yet implemented",
    }
