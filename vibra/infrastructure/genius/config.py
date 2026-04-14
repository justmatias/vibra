import re

from requests.exceptions import RequestException

RETRY_ON = (RequestException, TimeoutError, ConnectionError)

# Compiled pattern for removing common title suffixes that hurt search accuracy
# Matches: " - Remastered...", "(Remastered...)", "[Live...]", etc.
TITLE_CLEANUP_PATTERN = re.compile(
    r"""
    (?:
        \s*-\s*(?:Remastered|Live|Mono|Stereo|Radio\sEdit|Single\sVersion).*
        | \s*\((?:[^)]*(?:Remastered|Live|Mono|Stereo|Radio\sEdit|Single\sVersion)[^)]*)\)
        | \s*\[(?:[^\]]*(?:Remastered|Live|Mono|Stereo|Radio\sEdit|Single\sVersion)[^\]]*)\]
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)
