# Rate Limiting Configuration

## Free Tier Limits

The UpHere Space API free tier allows **1 request per second** maximum.

## Current Implementation

The API client automatically enforces rate limiting:

- **Default rate limit**: 1 request per second (1.0 second minimum interval)
- **Automatic spacing**: Requests are automatically spaced to respect the limit
- **Retry logic**: On 429 (rate limit) errors, the client will retry up to 3 times with exponential backoff
- **Request tracking**: All requests are tracked with timestamps

## Usage

### Default (Free Tier - 1 req/sec)

```python
from src.api import UpHereClient

client = UpHereClient()  # Default: 1 request per second
```

### Upgraded Subscription

If you upgrade your subscription and get a higher rate limit, you can configure it:

```python
from src.api import UpHereClient

client = UpHereClient()

# For example, if your tier allows 10 requests per second:
client.set_rate_limit(10.0)  # 10 requests per second
```

### Check Rate Limit Status

```python
stats = client.get_request_stats()
print(f"Rate limit: {stats['rate_limit']}")
print(f"Can make request now: {stats['can_make_request_now']}")
```

## How It Works

1. **Automatic Spacing**: Before each request, the client checks how much time has passed since the last request. If less than the minimum interval has passed, it waits.

2. **429 Error Handling**: If you receive a 429 (rate limit exceeded) error:
   - The client automatically retries up to 3 times
   - Each retry waits longer (exponential backoff: 1s, 2s, 3s)
   - If all retries fail, a clear error message is shown

3. **Request Tracking**: The client tracks:
   - Total number of requests made
   - Time of last request
   - Current rate limit configuration

## Best Practices

- **Batch Operations**: When fetching multiple satellites, consider fetching in batches with delays
- **Caching**: Cache API responses to avoid unnecessary requests
- **Monitor Usage**: Check `get_request_stats()` to monitor your request patterns

## Example: Fetching Multiple Pages

```python
from src.api import UpHereClient
import time

client = UpHereClient()

# Fetch multiple pages (rate limiting is automatic)
for page in range(1, 6):
    satellites = client.get_satellite_list(page=page)
    print(f"Page {page}: {len(satellites)} satellites")
    # No need to manually sleep - rate limiting is automatic!
```

