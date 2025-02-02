"""Channel join handler module."""
import logging
import os

from slack_bolt.context.async_context import AsyncBoltContext

from modules.models.slack_models.action_models import SlackActionRequestBody
from modules.models.slack_models.command_models import SlackCommandRequestBody
from modules.slack.blocks.shared_blocks import (
    channel_join_request_action,
    channel_join_request_blocks,
    channel_join_request_reset_action,
    channel_join_request_successful_block,
)
from modules.utils import log_to_thread, slack_team

logger = logging.getLogger(__name__)


async def handle_channel_join_request(
    parsed_body: SlackCommandRequestBody,
    context: AsyncBoltContext,
) -> None:
    """Handle the channel join request.

    :param parsed_body: The parsed body of the request.
    :param context: The Slack Bolt context.
    """
    logger.info("STAGE: Handling channel join command...")
    await context.ack()
    channel_id = ""
    channel_name = ""
    try:
        if parsed_body.command == "/join-pride":
            channel_id = slack_team.pride_channel.id
            channel_name = os.getenv("PRIDE_CHANNEL_NAME", "")
        if parsed_body.command == "/join-blacks-in-tech":
            channel_id = slack_team.blacks_in_tech.id
            channel_name = os.getenv("BLACKS_IN_TECH_CHANNEL_NAME", "")
        await context.client.chat_postMessage(
            channel=channel_id,
            blocks=channel_join_request_blocks(parsed_body.user_name),
            text="New channel join request...",
        )
        await context.client.chat_postEphemeral(
            channel=parsed_body.user_id,
            user=parsed_body.user_id,
            blocks=[channel_join_request_successful_block(channel_name)],
            text=f"Your request to join {channel_name} was successful...",
        )

    except Exception as general_exception:
        logger.exception("Unable to handle the channel join request")
        raise general_exception from general_exception


async def handle_channel_join_request_claim(
    parsed_body: SlackActionRequestBody,
    context: AsyncBoltContext,
) -> None:
    """Handle the claim for a channel join request.

    :param parsed_body: The parsed body of the request.
    :param context: The Slack Bolt context.
    """
    logger.info("STAGE: Handling channel join request claim...")
    await context.ack()
    try:
        blocks = parsed_body.message.blocks
        blocks[-1] = channel_join_request_reset_action(parsed_body.user.username)
        await log_to_thread(
            client=context.client,
            channel_id=parsed_body.channel.id,
            message_ts=parsed_body.message.ts,
            username=parsed_body.user.username,
            action_ts=parsed_body.actions[0].action_ts,
            claim=True,
        )
        await context.respond(
            text="Someone has claimed the invite request...",
            blocks=blocks,
            replace_original=True,
        )

    except Exception as general_exception:
        logger.exception("Unable to handle the channel join request claim")
        raise general_exception from general_exception


async def handle_channel_join_request_claim_reset(
    parsed_body: SlackActionRequestBody,
    context: AsyncBoltContext,
) -> None:
    """Handle the reset of claim for a channel join request.

    :param parsed_body: The parsed body of the request.
    :param context: The Slack Bolt context.
    """
    logger.info("STAGE: Handling channel join request claim reset...")
    await context.ack()
    try:
        blocks = parsed_body.message.blocks
        blocks[-1] = channel_join_request_action()
        await log_to_thread(
            client=context.client,
            channel_id=parsed_body.channel.id,
            message_ts=parsed_body.message.ts,
            username=parsed_body.user.username,
            action_ts=parsed_body.actions[0].action_ts,
            claim=False,
        )
        await context.respond(
            text="Someone has reset the invite request...",
            blocks=blocks,
            replace_original=True,
        )

    except Exception as general_exception:
        logger.exception("Unable to handle the channel join request claim reset")
        raise general_exception from general_exception
