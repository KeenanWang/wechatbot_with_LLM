import random
from http import HTTPStatus
import dashscope

dashscope.api_key = "sk-a659ea66e9334f338881166d62da54c5"


def call_with_messages(msg):
    messages = [
        {'role': 'system',
         'content': 'You are a very good friend.'},
        {'role': 'user', 'content': msg}]
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        # set the result to be "message" format.
        result_format='message',
    )
    if response.status_code == HTTPStatus.OK:
        return True, response.output.choices[0].message.content
    else:
        return False, response


if __name__ == '__main__':
    print(call_with_messages("怎么样才能变帅？"))
