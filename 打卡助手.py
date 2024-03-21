import time

from LLMTools import call_with_messages
from wxauto import WeChat

# config
dataBase = False  # 是否使用数据库

if dataBase:
    from database_tools import checkAttendance, attendanceSubmit, getSession

    session = getSession()

# 实例化微信对象
wx = WeChat()

# 指定监听目标
listen_list = [
    'LLM1群',
    '次世代大本营'
]
for i in listen_list:
    wx.AddListenChat(who=i)  # 添加监听对象并且自动保存新消息图片

# 持续监听消息
wait = 2  # 设置2秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        msg = msgs.get(chat)  # 获取消息内容
        print(msg)  # 打印消息
        man, man_msg = None, None  # 确定人和对应信息
        for each in msg:
            if each[0] != 'SYS':
                man = each[0]
                man_msg = each[1]
        if not man_msg:
            continue
        if '@小南同学' in man_msg:
            if dataBase and '今日打卡' in man_msg:
                if checkAttendance(session, man):
                    chat.SendMsg(f'用户{man}今天已签到。')  # 回复已签到
                else:
                    attendanceSubmit(session, man, man_msg)
                    chat.SendMsg(f'好的，今天辛苦了，{man}今天签到成功。')  # 回复签到成功
            else:
                man_msg = man_msg.strip('@小南同学 ')
                status, msg = call_with_messages(man_msg)
                if status:
                    chat.SendMsg(msg)
                else:
                    chat.SendMsg('出现错误，请重试。')
                pass
    time.sleep(wait)
