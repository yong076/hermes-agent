"""Webhook [SILENT] must not turn into an interactive warning."""

from types import SimpleNamespace

import pytest

from gateway.config import Platform
from gateway.run import GatewayRunner
from gateway.session import SessionSource


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "platform,expected_silence",
    [(Platform.WEBHOOK, True), (Platform.TELEGRAM, False)],
)
async def test_autonomous_webhook_silence_vs_human_message(platform, expected_silence):
    runner = object.__new__(GatewayRunner)
    source = SessionSource(platform=platform, chat_id="test-chat", user_id="test-user")
    response, silent, _ = await runner._hmwa_shape_agent_response(
        {"final_response": "[SILENT]", "messages": [], "api_calls": 1},
        source, [], SimpleNamespace(session_id="test-session"), None, None,
        None, "test-session", platform.value, 0,
    )
    assert silent is expected_silence
    if expected_silence:
        assert response == "[SILENT]"
    else:
        assert "silence marker" in response
