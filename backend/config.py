"""
Configuration Manager
Centralized configuration management using environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config :
    """Application configuration from environment variables."""

    # =====================================================
    # OpenAI Configuration
    # =====================================================
    OPENAI_API_KEY: Optional[str] = os.getenv( "OPENAI_API_KEY" )
    OPENAI_MODEL: str = os.getenv( "OPENAI_MODEL", "gpt-3.5-turbo" )
    OPENAI_ORG_ID: Optional[str] = os.getenv( "OPENAI_ORG_ID" )

    # =====================================================
    # Server Configuration
    # =====================================================
    HOST: str = os.getenv( "HOST", "0.0.0.0" )
    PORT: int = int( os.getenv( "PORT", "8000" ) )
    STREAMLIT_PORT: int = int( os.getenv( "STREAMLIT_PORT", "8501" ) )

    # =====================================================
    # Security Configuration
    # =====================================================
    SECRET_KEY: str = os.getenv( "SECRET_KEY", "change-this-secret-key-in-production" )
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501"
    ).split( "," )

    # =====================================================
    # File Upload Configuration
    # =====================================================
    MAX_UPLOAD_SIZE: int = int( os.getenv( "MAX_UPLOAD_SIZE", "10" ) )  # MB
    ALLOWED_CERT_EXTENSIONS: list = os.getenv(
        "ALLOWED_CERT_EXTENSIONS",
        ".pdf,.jpg,.jpeg,.png"
    ).split( "," )
    ALLOWED_RESUME_EXTENSIONS: list = os.getenv(
        "ALLOWED_RESUME_EXTENSIONS",
        ".pdf,.docx,.txt"
    ).split( "," )

    # =====================================================
    # LaTeX Configuration
    # =====================================================
    PDFLATEX_PATH: Optional[str] = os.getenv(
        "PDFLATEX_PATH"
    ) or r"C:\Users\somas\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"
    LATEX_TIMEOUT: int = int( os.getenv( "LATEX_TIMEOUT", "30" ) )

    # =====================================================
    # Logging Configuration
    # =====================================================
    LOG_LEVEL: str = os.getenv( "LOG_LEVEL", "INFO" )
    LOG_FILE: Optional[str] = os.getenv( "LOG_FILE" ) or None

    # =====================================================
    # Feature Flags
    # =====================================================
    ENABLE_AI_EXTRACTION: bool = os.getenv( "ENABLE_AI_EXTRACTION", "true" ).lower() == "true"
    ENABLE_PDF_COMPILATION: bool = os.getenv( "ENABLE_PDF_COMPILATION", "true" ).lower() == "true"
    ENABLE_SUGGESTIONS: bool = os.getenv( "ENABLE_SUGGESTIONS", "true" ).lower() == "true"

    # =====================================================
    # Development Configuration
    # =====================================================
    DEBUG: bool = os.getenv( "DEBUG", "false" ).lower() == "true"
    AUTO_RELOAD: bool = os.getenv( "AUTO_RELOAD", "true" ).lower() == "true"

    # =====================================================
    # Rate Limiting
    # =====================================================
    RATE_LIMIT: int = int( os.getenv( "RATE_LIMIT", "60" ) )  # requests per minute

    @classmethod
    def validate ( cls ) -> dict :
        """
        Validate configuration and return status.

        Returns:
            Dictionary with validation results
        """
        issues = []
        warnings = []

        # Check OpenAI configuration
        if not cls.OPENAI_API_KEY :
            warnings.append( "OPENAI_API_KEY not set - AI features will be limited" )
        elif not cls.OPENAI_API_KEY.startswith( "sk-" ) :
            issues.append( "OPENAI_API_KEY appears to be invalid (should start with 'sk-')" )

        # Check secret key
        if cls.SECRET_KEY == "change-this-secret-key-in-production" :
            warnings.append( "SECRET_KEY is using default value - change in production" )

        # Check port conflicts
        if cls.PORT == cls.STREAMLIT_PORT :
            issues.append( f"PORT and STREAMLIT_PORT cannot be the same ({cls.PORT})" )

        # Check file size
        if cls.MAX_UPLOAD_SIZE > 100 :
            warnings.append( f"MAX_UPLOAD_SIZE is very large ({cls.MAX_UPLOAD_SIZE}MB)" )

        # Check LaTeX
        if cls.ENABLE_PDF_COMPILATION :
            import shutil
            from pathlib import Path

            # Check if custom path exists
            if cls.PDFLATEX_PATH and Path(cls.PDFLATEX_PATH).exists():
                pass  # Custom path is valid
            elif shutil.which( "pdflatex" ):
                pass  # System pdflatex found
            else:
                warnings.append( "pdflatex not found - PDF compilation will fail" )

        return {
            "valid" : len( issues ) == 0,
            "issues" : issues,
            "warnings" : warnings
        }

    @classmethod
    def get_info ( cls ) -> dict :
        """
        Get configuration information (safe to display).

        Returns:
            Dictionary with configuration info
        """
        return {
            "openai" : {
                "configured" : bool( cls.OPENAI_API_KEY ),
                "model" : cls.OPENAI_MODEL,
                "has_org_id" : bool( cls.OPENAI_ORG_ID )
            },
            "server" : {
                "host" : cls.HOST,
                "port" : cls.PORT,
                "streamlit_port" : cls.STREAMLIT_PORT
            },
            "features" : {
                "ai_extraction" : cls.ENABLE_AI_EXTRACTION,
                "pdf_compilation" : cls.ENABLE_PDF_COMPILATION,
                "suggestions" : cls.ENABLE_SUGGESTIONS
            },
            "uploads" : {
                "max_size_mb" : cls.MAX_UPLOAD_SIZE,
                "allowed_cert_types" : cls.ALLOWED_CERT_EXTENSIONS,
                "allowed_resume_types" : cls.ALLOWED_RESUME_EXTENSIONS
            },
            "development" : {
                "debug" : cls.DEBUG,
                "auto_reload" : cls.AUTO_RELOAD
            }
        }

    @classmethod
    def print_status ( cls ) :
        """Print configuration status to console."""
        print( "\n" + "=" * 60 )
        print( "🔧 Configuration Status" )
        print( "=" * 60 )

        # Validate configuration
        validation = cls.validate()

        if validation["valid"] :
            print( "✅ Configuration is valid" )
        else :
            print( "❌ Configuration has issues:" )
            for issue in validation["issues"] :
                print( f"   ❌ {issue}" )

        if validation["warnings"] :
            print( "\n⚠️  Warnings:" )
            for warning in validation["warnings"] :
                print( f"   ⚠️  {warning}" )

        # Print feature status
        print( "\n📊 Features:" )
        print( f"   OpenAI API: {'✅ Configured' if cls.OPENAI_API_KEY else '❌ Not configured'}" )
        print( f"   AI Extraction: {'✅ Enabled' if cls.ENABLE_AI_EXTRACTION else '❌ Disabled'}" )
        print( f"   PDF Compilation: {'✅ Enabled' if cls.ENABLE_PDF_COMPILATION else '❌ Disabled'}" )
        print( f"   Suggestions: {'✅ Enabled' if cls.ENABLE_SUGGESTIONS else '❌ Disabled'}" )

        print( "\n🌐 Server:" )
        print( f"   Backend: http://{cls.HOST}:{cls.PORT}" )
        print( f"   Frontend: http://localhost:{cls.STREAMLIT_PORT}" )

        print( "\n" + "=" * 60 + "\n" )


# Create a global config instance
config = Config()

# Validate on import
if __name__ != "__main__" :
    validation = config.validate()
    if not validation["valid"] :
        print( "⚠️  Configuration issues detected:" )
        for issue in validation["issues"] :
            print( f"   ❌ {issue}" )

if __name__ == "__main__" :
    # If run directly, print full status
    config.print_status()

    import json

    print( "📋 Full Configuration Info:" )
    print( json.dumps( config.get_info(), indent=2 ) )