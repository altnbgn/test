from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    READER: _ClassVar[ClientType]
    PROCESSOR: _ClassVar[ClientType]

class ResourceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CONNECTED: _ClassVar[ResourceStatus]
    DISCONNECTED: _ClassVar[ResourceStatus]

class CommandType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    READER_START_LIVE: _ClassVar[CommandType]
    READER_STOP_LIVE: _ClassVar[CommandType]
    READER_CONNECT: _ClassVar[CommandType]
    READER_TOKEN_UPDATE: _ClassVar[CommandType]
    READER_STREAMS: _ClassVar[CommandType]
    PROCESSOR_CONNECT: _ClassVar[CommandType]
    PROCESSOR_CURRENT: _ClassVar[CommandType]

class RequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TOKEN_UPDATE: _ClassVar[RequestType]
    CLOSE_READER: _ClassVar[RequestType]
    READER_KEYS: _ClassVar[RequestType]
    START_LIVE: _ClassVar[RequestType]
    CONNECT_PROCESSOR: _ClassVar[RequestType]
    CURRENT_PROCESSOR: _ClassVar[RequestType]
    GET_WORKER: _ClassVar[RequestType]
    GET_RESOURCE: _ClassVar[RequestType]
    SET_CAMERA: _ClassVar[RequestType]
READER: ClientType
PROCESSOR: ClientType
CONNECTED: ResourceStatus
DISCONNECTED: ResourceStatus
READER_START_LIVE: CommandType
READER_STOP_LIVE: CommandType
READER_CONNECT: CommandType
READER_TOKEN_UPDATE: CommandType
READER_STREAMS: CommandType
PROCESSOR_CONNECT: CommandType
PROCESSOR_CURRENT: CommandType
TOKEN_UPDATE: RequestType
CLOSE_READER: RequestType
READER_KEYS: RequestType
START_LIVE: RequestType
CONNECT_PROCESSOR: RequestType
CURRENT_PROCESSOR: RequestType
GET_WORKER: RequestType
GET_RESOURCE: RequestType
SET_CAMERA: RequestType

class ClientRequest(_message.Message):
    __slots__ = ["register", "ping", "resource", "result", "processor"]
    REGISTER_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    register: Register
    ping: Ping
    resource: Resource
    result: Result
    processor: Processor
    def __init__(self, register: _Optional[_Union[Register, _Mapping]] = ..., ping: _Optional[_Union[Ping, _Mapping]] = ..., resource: _Optional[_Union[Resource, _Mapping]] = ..., result: _Optional[_Union[Result, _Mapping]] = ..., processor: _Optional[_Union[Processor, _Mapping]] = ...) -> None: ...

class Register(_message.Message):
    __slots__ = ["type", "id", "endpoint"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    type: ClientType
    id: str
    endpoint: str
    def __init__(self, type: _Optional[_Union[ClientType, str]] = ..., id: _Optional[str] = ..., endpoint: _Optional[str] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class Resource(_message.Message):
    __slots__ = ["id", "status", "list"]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: ResourceStatus
    list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[ResourceStatus, str]] = ..., list: _Optional[_Iterable[str]] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ["id", "cameraId", "data", "timestamp"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CAMERAID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    cameraId: str
    data: bytes
    timestamp: int
    def __init__(self, id: _Optional[str] = ..., cameraId: _Optional[str] = ..., data: _Optional[bytes] = ..., timestamp: _Optional[int] = ...) -> None: ...

class Processor(_message.Message):
    __slots__ = ["id", "processorId", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROCESSORID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    processorId: str
    status: ResourceStatus
    def __init__(self, id: _Optional[str] = ..., processorId: _Optional[str] = ..., status: _Optional[_Union[ResourceStatus, str]] = ...) -> None: ...

class ClientResponse(_message.Message):
    __slots__ = ["command", "message"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    command: Command
    message: str
    def __init__(self, command: _Optional[_Union[Command, _Mapping]] = ..., message: _Optional[str] = ...) -> None: ...

class Command(_message.Message):
    __slots__ = ["type", "token", "cameraId", "serverUrl", "id"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    CAMERAID_FIELD_NUMBER: _ClassVar[int]
    SERVERURL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    type: CommandType
    token: str
    cameraId: str
    serverUrl: str
    id: str
    def __init__(self, type: _Optional[_Union[CommandType, str]] = ..., token: _Optional[str] = ..., cameraId: _Optional[str] = ..., serverUrl: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class DebugRequest(_message.Message):
    __slots__ = ["type", "token", "id", "cameraId", "server", "processor", "cameraLabel"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CAMERAID_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    CAMERALABEL_FIELD_NUMBER: _ClassVar[int]
    type: RequestType
    token: str
    id: str
    cameraId: str
    server: str
    processor: str
    cameraLabel: str
    def __init__(self, type: _Optional[_Union[RequestType, str]] = ..., token: _Optional[str] = ..., id: _Optional[str] = ..., cameraId: _Optional[str] = ..., server: _Optional[str] = ..., processor: _Optional[str] = ..., cameraLabel: _Optional[str] = ...) -> None: ...

class DebugResponse(_message.Message):
    __slots__ = ["message", "reader", "processor", "camera", "serverUrl"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    READER_FIELD_NUMBER: _ClassVar[int]
    PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    SERVERURL_FIELD_NUMBER: _ClassVar[int]
    message: str
    reader: _containers.RepeatedCompositeFieldContainer[ReaderWrap]
    processor: _containers.RepeatedCompositeFieldContainer[ProcessorWrap]
    camera: _containers.RepeatedScalarFieldContainer[str]
    serverUrl: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, message: _Optional[str] = ..., reader: _Optional[_Iterable[_Union[ReaderWrap, _Mapping]]] = ..., processor: _Optional[_Iterable[_Union[ProcessorWrap, _Mapping]]] = ..., camera: _Optional[_Iterable[str]] = ..., serverUrl: _Optional[_Iterable[str]] = ...) -> None: ...

class ReaderWrap(_message.Message):
    __slots__ = ["id", "endpoint", "resource", "processor"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    endpoint: str
    resource: _containers.RepeatedScalarFieldContainer[str]
    processor: str
    def __init__(self, id: _Optional[str] = ..., endpoint: _Optional[str] = ..., resource: _Optional[_Iterable[str]] = ..., processor: _Optional[str] = ...) -> None: ...

class ProcessorWrap(_message.Message):
    __slots__ = ["id", "endpoint"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    id: str
    endpoint: str
    def __init__(self, id: _Optional[str] = ..., endpoint: _Optional[str] = ...) -> None: ...
