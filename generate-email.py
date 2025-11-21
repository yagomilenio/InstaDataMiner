import asyncio
import MailTM.mailtmapi as m

async def main() -> None:
    mailtm = m.MailTM()

    temp_mail = await mailtm.get_account()
    print(temp_mail)
    token = temp_mail.token.token
    pre_msgs = None
    
    while True:
        msgs = await mailtm.get_messages(token)

        if msgs != pre_msgs:
            print(msgs)
            pre_msgs = msgs
        await asyncio.sleep(2)

if __name__ == '__main__':
    asyncio.run(main())
