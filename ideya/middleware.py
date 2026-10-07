"""Security headers Django does not set itself.

The CSP restricts only what costs nothing: plugins, <base> hijacking, forms
posting elsewhere, framing. It deliberately leaves scripts alone: Alpine needs
eval, and Cloudflare injects its own bot-detection and analytics scripts.
"""

CSP = "object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
PERMISSIONS = "camera=(), microphone=(), geolocation=(), payment=(), usb=()"


def security_headers(get_response):
    def middleware(request):
        response = get_response(request)
        response.headers.setdefault("Content-Security-Policy", CSP)
        response.headers.setdefault("Permissions-Policy", PERMISSIONS)
        return response

    return middleware
