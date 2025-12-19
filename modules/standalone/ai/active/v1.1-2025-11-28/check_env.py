#!/usr/bin/env python3
"""Check if .env is properly configured for AI module"""

from src.ai.config import settings

print("")
print("=" * 60)
print("ENVIRONMENT CONFIGURATION CHECK")
print("=" * 60)
print("")

# Check LLM providers
has_openai = bool(settings.openai_api_key)
has_anthropic = bool(settings.anthropic_api_key)

print("🔑 LLM API Keys:")
print(f"   OpenAI:    {'✅ CONFIGURED' if has_openai else '❌ MISSING'}")
print(f"   Anthropic: {'✅ CONFIGURED' if has_anthropic else '⚠️  Not set (optional fallback)'}")
print("")

print("🗄️  Service URLs:")
print(f"   Database:  {settings.database_url}")
print(f"   Qdrant:    {settings.qdrant_url}")
print(f"   RabbitMQ:  {settings.rabbitmq_url}")
print("")

print("⚙️  Configuration:")
print(f"   Environment:      {settings.env}")
print(f"   Log Level:        {settings.log_level}")
print(f"   Embeddings:       {settings.embedding_dimensions} dimensions")
print(f"   Confidence (Med): {settings.medium_confidence_threshold}")
print(f"   Confidence (High): {settings.high_confidence_threshold}")
print("")

print("=" * 60)
print("🎯 ASSESSMENT:")
print("=" * 60)

if has_openai or has_anthropic:
    print("")
    print("✅ YOUR .ENV IS PROPERLY CONFIGURED!")
    print("")
    print("   You have at least one LLM provider configured.")
    print("   The AI module will work for:")
    print("   • Entity extraction ✅")
    print("   • Relationship mapping ✅")
    print("   • Knowledge graph construction ✅")
    print("   • Vector similarity search ✅")
    print("")
    if has_openai and has_anthropic:
        print("   🌟 BONUS: You have both OpenAI and Anthropic!")
        print("      The system will use OpenAI primarily and")
        print("      fall back to Claude if OpenAI fails.")
    print("")
else:
    print("")
    print("❌ MISSING LLM API KEY!")
    print("")
    print("   Your .env needs at least one of these:")
    print("   • OPENAI_API_KEY=sk-proj-your-key-here")
    print("   • ANTHROPIC_API_KEY=sk-ant-your-key-here")
    print("")
    print("   Without an LLM key, entity extraction won't work.")
    print("   The API will start but extraction requests will fail.")
    print("")

print("=" * 60)
print("")

print("📝 To update your .env:")
print("   1. Open .env in a text editor")
print("   2. Add: OPENAI_API_KEY=sk-your-key-here")
print("   3. Save and restart the API")
print("")

print("🚀 To start the full system:")
print("   1. docker-compose up -d")
print("   2. alembic upgrade head")
print("   3. uvicorn src.ai.api.main:app --reload")
print("   4. Open: http://localhost:8000/docs")
print("")

