from typing import List, Optional, Union, Dict, Literal
from pydantic import BaseModel, Field
import datetime


class FunctionCall(BaseModel):
    arguments: str
    name: str

# chain | systemMessage | assitemMessage | promtptemple | model | outputparser

class ToolCall(BaseModel):
    id: str
    # "Currently, only function is supported"
    type: Literal["function"] = "function"
    # function: ToolCallFunction
    function: FunctionCall


class LogProbToken(BaseModel):
    token: str
    logprob: float
    bytes: Optional[List[int]]


class MessageContentLogProb(BaseModel):
    token: str
    logprob: float
    bytes: Optional[List[int]]
    top_logprobs: Optional[List[LogProbToken]]


class Message(BaseModel):
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    role: str
    function_call: Optional[FunctionCall] = None  # Deprecated

class Choice(BaseModel):
    finish_reason: str
    index: int
    message: Message
    logprobs: Optional[Dict[str, Union[List[MessageContentLogProb], None]]] = None


class UsageStatistics(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str
    choices: List[Choice]
    created: datetime.datetime
    model: str
    object: Literal["chat.completion"] = "chat.completion"
    usage: UsageStatistics