# API Key Setup Guide

## Where to Put Your Perplexity API Key

The Perplexity API key should be placed in a `.env` file in the root directory of the project.

### Quick Setup Steps

1. **Create a `.env` file** in the project root directory (same level as `requirements.txt`)

2. **Add your Perplexity API key** to the `.env` file:
   ```env
   PERPLEXITY_API_KEY=pplx-your-actual-api-key-here
   ```

3. **That's it!** The application will automatically load the key when it starts.

### Detailed Instructions

#### Option 1: Create `.env` from Template (Recommended)

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# On Windows:
notepad .env

# On Mac/Linux:
nano .env
# or
vim .env
```

Then add this line to your `.env` file:
```env
PERPLEXITY_API_KEY=pplx-your-actual-api-key-here
```

#### Option 2: Create `.env` Manually

1. Create a new file named `.env` in the project root
2. Add the following line:
   ```env
   PERPLEXITY_API_KEY=pplx-your-actual-api-key-here
   ```

#### Option 3: Set Environment Variable Directly

**Windows (PowerShell):**
```powershell
$env:PERPLEXITY_API_KEY="pplx-your-actual-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set PERPLEXITY_API_KEY=pplx-your-actual-api-key-here
```

**Mac/Linux:**
```bash
export PERPLEXITY_API_KEY=pplx-your-actual-api-key-here
```

**Note**: Environment variables set this way only last for the current terminal session.

### Getting Your Perplexity API Key

1. Go to [Perplexity API](https://www.perplexity.ai/settings/api)
2. Sign up or log in
3. Navigate to API settings
4. Generate a new API key
5. Copy the key (it starts with `pplx-`)

### Example `.env` File

Here's what a complete `.env` file might look like:

```env
# Primary LLM Provider (Required)
PERPLEXITY_API_KEY=pplx-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# Optional Fallback Providers
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
ANTHROPIC_API_KEY=sk-ant-api03-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# Database (if using Docker Compose defaults)
DATABASE_URL=postgresql://ai_user:password@localhost:5432/ai_module

# Other settings...
ENV=development
LOG_LEVEL=INFO
```

### Verification

To verify your API key is loaded correctly:

```python
# Run this in Python
from src.ai.config import settings
print(f"Perplexity API Key configured: {settings.perplexity_api_key is not None}")
print(f"Key starts with 'pplx-': {settings.perplexity_api_key.startswith('pplx-') if settings.perplexity_api_key else False}")
```

### Important Notes

- ✅ The `.env` file is already in `.gitignore` - your API key will NOT be committed to git
- ✅ Never share your API key publicly
- ✅ The application will use Perplexity as the primary LLM, with OpenAI/Claude as fallbacks
- ✅ If Perplexity API key is not set, the system will try to use OpenAI or Claude (if configured)

### Troubleshooting

**"Perplexity API key not set" warning:**
- Make sure the `.env` file exists in the project root
- Check that the variable name is exactly `PERPLEXITY_API_KEY` (case-insensitive)
- Verify there are no extra spaces around the `=` sign
- Restart your application after adding the key

**"No LLM clients available" error:**
- Make sure at least one API key is configured (Perplexity, OpenAI, or Anthropic)
- Check that the API key format is correct
- Verify the `.env` file is being loaded (check application startup logs)

