from slackclient import SlackClient

slack_client = SlackClient('xoxb-676821839270-663291810786-f8URnHjoegykxUuqepHjsD3z')
slack_client.api_call('api.test')

print(slack_client.api_call('auth.test'))

