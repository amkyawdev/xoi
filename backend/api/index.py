# Vercel Serverless Function Entry Point
try:
    from vercel_fastapi import Vercel
    from app.main import app as fastapi_app
    
    app = Vercel(fastapi_app)
except ImportError:
    # Fallback for local development
    from app.main import app
    
    # Vercel handler
    def handler(request, context=None):
        return app(request, context)
