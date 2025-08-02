import functools
from telegram import Update
from telegram.ext import ContextTypes
from app.core.config import ADMIN_ID

def admin_required(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("You are not authorized to use this command.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper