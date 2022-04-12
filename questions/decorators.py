try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


from django.contrib.auth.decorators import login_required
from django.contrib import messages
