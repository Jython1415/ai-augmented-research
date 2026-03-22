# Model Collapse Post Collector

Data collection script for gathering Bluesky posts about model collapse using the AT Protocol API.

## Setup

1. **Install dependencies** (first time only):
   ```bash
   uv run --script collect_posts.py
   ```
   This will automatically install `atproto` via PEP 723 dependencies.

2. **Get credentials**:
   - Go to https://bsky.app/settings/app-passwords
   - Create a new app password (give it a descriptive name like "model-collapse-research")
   - Copy the password shown (you won't see it again)

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials:
   # BSKY_HANDLE=your-handle.bsky.social
   # BSKY_APP_PASSWORD=your-app-password-here
   ```

## Running the Collector

```bash
cd /Users/Joshua/agent/model-collapse-study
uv run --script analysis/collect_posts.py
```

The script will:
- Authenticate with your Bluesky account
- Search for 6 different model collapse-related terms
- Paginate through results with cursor-based pagination
- Deduplicate posts by URI
- Store unique posts in `data/posts.db`
- Track which search term matched each post
- Respect rate limits (0.15s delay between requests)
- Print progress as it collects

## Search Terms

The script searches for:
1. "model collapse"
2. "tail collapse"
3. "shumailov"
4. "training on synthetic data"
5. "trained on AI-generated"
6. "recursive training"

Date range: 2023-05-01 onwards

## Database Schema

Posts are stored in `posts` table with:
- `uri`: Unique post identifier (prevents duplicates)
- `cid`: Content hash
- `text`: Post content
- `created_at`: ISO 8601 timestamp
- `author_did`: Author DID identifier
- `author_handle`: Author handle
- `reply_to_uri`: Parent post URI if this is a reply
- `source`: Always "api" for posts collected via this script
- `search_term_matched`: Which search term found this post
- `collected_at`: When it was added to database

## Output Example

```
============================================================
Model Collapse Post Collector
============================================================
✓ Authenticated as your-handle.bsky.social
✓ Connected to database: /Users/Joshua/agent/model-collapse-study/data/posts.db

🔍 Searching for: 'model collapse'
  Request 1: 75 posts
  Request 2: 100 posts
  ...
  ✓ Reached end of results for 'model collapse' (542 posts)

🔍 Searching for: 'tail collapse'
  Request 1: 12 posts
  ✓ Reached end of results for 'tail collapse' (12 posts)

...

============================================================
✓ Collection complete in 0:05:32.123456
  Total collected: 624
  Total duplicates: 45
============================================================
```

## Troubleshooting

**"Missing credentials" error**: Ensure `.env` file exists and has BSKY_HANDLE and BSKY_APP_PASSWORD set.

**"Failed to authenticate" error**: Check that your handle and app password are correct. App passwords are different from your main Bluesky password.

**"No results" on first search**: This is normal if you just created the account or if there are genuinely no posts matching a term.

**Rate limit issues**: The script includes a 0.15s delay between requests (respects 3000 req / 5 min limit). If you hit limits, just wait a few minutes before re-running.

## Notes

- The script is idempotent: running it multiple times won't create duplicates
- Only new posts (not already in database) are added
- The `search_term_matched` field tracks which query found each post (useful for analysis)
- Large collections may take several minutes depending on result volumes
