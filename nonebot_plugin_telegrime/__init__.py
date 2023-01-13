from nonebot import on, on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent, InlineQueryEvent
from nonebot.adapters.telegram.model import (
    InputTextMessageContent,
    InlineQueryResultArticle,
)
from .librime import get_candidate


@on_command("switch").handle()
async def _(bot: Bot, event: MessageEvent):
    pass


# InlineQuery：https://core.telegram.org/bots/inline
@on("").handle()  # 由于我还未给 InlineQueryEvent 分配 event_name，目前只能使用 on("") 来匹配
async def _(bot: Bot, event: InlineQueryEvent):
    candidate = get_candidate(event.query)
    await bot.answer_inline_query(
        inline_query_id=event.id,
        results=[
            InlineQueryResultArticle(
                id=candidate,# type: ignore
                title=candidate,# type: ignore
                input_message_content=InputTextMessageContent(message_text=candidate),# type: ignore
            )
        ],# type: ignore
    )
