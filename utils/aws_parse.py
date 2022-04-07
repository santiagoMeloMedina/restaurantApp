
from typing import Any, Callable, Dict, Optional, Union
import pydantic
import enum
import json
from utils import encryption


class LambdaEvent(pydantic.BaseModel):
    body: Optional[Dict[str, Any]]
    headers: Optional[Dict[str, Any]]
    params: Optional[Dict[str, Any]]

class HttpCodes(enum.Enum):
    SUCCESS = 200
    ACCEPTED = 300
    ERROR = 500
    BAD_REQUEST = 400

AUTHORIZATION_HEADER_NAME = "Authorization"

def _decode_token_from_header(token: str) -> Dict:
    decoded = encryption.JWTHandler(token=token).decode()
    return decoded

def _inject_user_from_token(event: LambdaEvent) -> str:
    if AUTHORIZATION_HEADER_NAME in event.headers:
        decoded = _decode_token_from_header(event.headers.get(AUTHORIZATION_HEADER_NAME))
        event.body = {
            **event.body, 
            "user": decoded.get("user", "")
        }

def parse_lambda_event(func: Callable[[LambdaEvent, Any], Any]) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            event, context = args
            parsed_event = LambdaEvent.parse_obj(event)
            _inject_user_from_token(parsed_event)
            return func(parsed_event, context)
        except Exception as e:
            return get_response(HttpCodes.ERROR, {"message": str(e)})
    
    return wrapper

def get_response(code: HttpCodes, body: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    return {"statusCode": code.value, "body": json.dumps(body)}


def get_standard_success_response() -> Dict[str, Any]:
    return get_response(HttpCodes.SUCCESS, "Success")


def get_standard_error_response() -> Dict[str, Any]:
    return get_response(HttpCodes.ERROR, "Error")