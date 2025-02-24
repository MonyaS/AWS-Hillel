import aws_cdk as core
import aws_cdk.assertions as assertions

from url_shoarter.url_shoarter_stack import UrlShoarterStack


# example tests. To run these tests, uncomment this file along with the example
# resource in url_shoarter/url_shoarter_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = UrlShoarterStack(app, "url-shoarter")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
