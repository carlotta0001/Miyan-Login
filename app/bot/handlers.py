from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from app.core import database
from app.bot.decorators import admin_required
from app.utils.time_helpers import calculate_expiry_date

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Key Management Bot is running.\n\n"
        "/key <key> - Check the status and expiry of your key.\n\n"
    )

@admin_required
async def add_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usage_text = "Usage: /add <key> <amount> <unit>\nExample: /add my-secret-key 30 days"
    if len(context.args) != 3:
        await update.message.reply_text(usage_text)
        return

    key, amount, unit = context.args
    expires_at = calculate_expiry_date(amount, unit)

    if not expires_at:
        await update.message.reply_text(f"Invalid amount or unit.\n{usage_text}")
        return

    if database.add_key(key, expires_at):
        await update.message.reply_text(f"Success: Key '{key}' has been added.\nExpires on: {expires_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    else:
        await update.message.reply_text("Error: Key already exists in the database.")

@admin_required
async def set_expire_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usage_text = "Usage: /setexpire <key> <amount> <unit>\nExample: /setexpire my-secret-key 2 weeks"
    if len(context.args) != 3:
        await update.message.reply_text(usage_text)
        return

    key, amount, unit = context.args
    expires_at = calculate_expiry_date(amount, unit)

    if not expires_at:
        await update.message.reply_text(f"Invalid amount or unit.\n{usage_text}")
        return

    if database.set_key_expiration(key, expires_at):
        await update.message.reply_text(f"Success: Expiration for key '{key}' has been updated.\nNew expiration: {expires_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    else:
        await update.message.reply_text("Error: Key not found.")

@admin_required
async def remove_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        key = context.args[0]
        if database.remove_key(key):
            await update.message.reply_text(f"Success: Key '{key}' has been removed.")
        else:
            await update.message.reply_text("Error: Key not found.")
    except IndexError:
        await update.message.reply_text("Usage: /remove <key>")

@admin_required
async def reset_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        key = context.args[0]
        if database.reset_device_id(key):
            await update.message.reply_text(f"Success: Device ID for key '{key}' has been reset.")
        else:
            await update.message.reply_text("Error: Key not found.")
    except IndexError:
        await update.message.reply_text("Usage: /reset <key>")

async def key_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        key = context.args[0]
    except IndexError:
        await update.message.reply_text("Usage: /key <your-key>")
        return

    key_info = database.get_key_info(key)

    if not key_info:
        await update.message.reply_text("Key not found.")
        return

    expires_at = key_info.get('expires_at')
    if expires_at:
        expiry_str = expires_at.strftime('%Y-%m-%d %H:%M') + " UTC"
        if expires_at < datetime.utcnow():
            expiry_str += " (EXPIRED)"
    else:
        expiry_str = "Never"

    message = (
        f"Key Information:\n\n"
        f"Key: `{key_info['key']}`\n"
        f"Expires: `{expiry_str}`"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

@admin_required
async def list_keys_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys = database.get_all_keys()
    if not keys:
        await update.message.reply_text("The database is empty.")
        return

    message_parts = ["List of Keys:\n"]
    for item in keys:
        device = item.get('device_id') or "Not yet registered"
        expires_at = item.get('expires_at')
        if expires_at:
            expiry_str = expires_at.strftime('%Y-%m-%d %H:%M') + " UTC"
            if expires_at < datetime.utcnow():
                expiry_str += " (EXPIRED)"
        else:
            expiry_str = "Never"
        
        message_parts.append(f"\nKey: `{item['key']}`\nDevice: `{device}`\nExpires: `{expiry_str}`\n")

    await update.message.reply_text("".join(message_parts), parse_mode='Markdown')