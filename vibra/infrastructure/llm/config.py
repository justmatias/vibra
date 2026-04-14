from openai import APIConnectionError, APITimeoutError

RETRY_ON = (APIConnectionError, APITimeoutError, ConnectionError, TimeoutError)
