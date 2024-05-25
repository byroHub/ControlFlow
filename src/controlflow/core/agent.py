import logging
from typing import Callable, Optional

from pydantic import Field

import controlflow
from controlflow.tools.talk_to_human import talk_to_human
from controlflow.utilities.asyncio import ExposeSyncMethodsMixin
from controlflow.utilities.types import ControlFlowModel

logger = logging.getLogger(__name__)


def get_default_agent() -> "Agent":
    return controlflow.default_agent


class Agent(ControlFlowModel, ExposeSyncMethodsMixin):
    name: str = Field(
        ...,
        description="The name of the agent. This is used to identify the agent in the system and should be unique per assigned task.",
    )
    description: Optional[str] = Field(
        None, description="A description of the agent, visible to other agents."
    )
    instructions: Optional[str] = Field(
        None, description="Instructions for the agent, private to this agent."
    )
    tools: list[Callable] = Field(
        [], description="List of tools availble to the agent."
    )
    user_access: bool = Field(
        False,
        description="If True, the agent is given tools for interacting with a human user.",
    )
    model: str = Field(
        description="The model used by the agent. If not provided, the default model will be used.",
        default_factory=lambda: controlflow.settings.llm_model,
    )

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

    def get_tools(self) -> list[Callable]:
        tools = self.tools.copy()
        if self.user_access:
            tools.append(talk_to_human)
        return tools


DEFAULT_AGENT = Agent(
    name="Marvin",
    instructions="""
        You are a diligent AI assistant. You complete 
        your tasks efficiently and without error.
        """,
)
