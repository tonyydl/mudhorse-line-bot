import time

_sessions = {}  # user_id -> {step, location, kind, expires}


def get_session(user_id):
    """Return active session dict or None if missing/expired."""
    entry = _sessions.get(user_id)
    if entry is None:
        return None
    if time.time() > entry['expires']:
        del _sessions[user_id]
        return None
    return entry


def set_session(user_id, data):
    """Create or overwrite session, resetting the 10-minute TTL."""
    _sessions[user_id] = {**data, 'expires': time.time() + 600}


def clear_session(user_id):
    """Remove session (no-op if absent)."""
    _sessions.pop(user_id, None)
