import random
from http import HTTPStatus

import dashscope

with open('F:/ProgrammeProject/PythonProject/api_key.txt', 'r') as f:  # 请更改文件路径，文件中应只包含API Key
    dashscope.api_key = f.readlines()[0]  # 设置API Key


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
