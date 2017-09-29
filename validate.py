from oauth.token.validator import authorizer
from common.logs import Log
log = Log()


def validation_handler(event, context):
    return authorizer.authorize(event)


if __name__== "__main__":
    event = {
        "access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIxMjM0NSIsImlzcyI6ImFiYy5jb20iLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJqdGkiOiJzYWo5SXJsam9yMXprIiwiZXhwIjoxNTA2NTQzNjE4LCJpYXQiOjE1MDY1NDAwMTgsInNjb3BlIjp7ImFjY2VzcyI6eyIvZ3JhbnQiOlsiUE9TVCJdLCIvZXZlbnQiOlsiUEFUQ0giLCJHRVQiXX0sImdyYW50X2FjY2VzcyI6WyJ1cGRhdGUtZXZlbnQiLCJncmFudC1hY2Nlc3MiLCJnZXQtZXZlbnQiXX0sInJvbGwiOlsiQURNSU4iXSwic3ViIjoiYmlqb3kucGF1bEB0b3RoZW5ldy5jb20ifQ.GsTvubVQmIRI7fuDSxRb433lyZT7XSq5zflP4558WvI",
        "client_id": "12345",
        "client_request_data": {
            "todo":"TODO"
        }
    }
    log.info(validation_handler(event, None))
