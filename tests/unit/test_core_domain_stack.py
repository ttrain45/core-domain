import aws_cdk as core
import aws_cdk.assertions as assertions

from core_domain.core_domain_stack import CoreDomainStack

# example tests. To run these tests, uncomment this file along with the example
# resource in core_domain/core_domain_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CoreDomainStack(app, "core-domain")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
