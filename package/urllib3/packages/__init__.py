from __future__ import absolute_import
try:
	from . import ssl_match_hostname
except ImportError:
	from package import ssl_match_hostname

__all__ = ('ssl_match_hostname', )
