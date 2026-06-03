# Pattern: Monitoring Agent

## Description

Polls external sources on a schedule, detects anomalies or threshold breaches, and sends alerts. Suitable for price tracking, news alerts, portfolio monitoring, and API health checks.

## Core Loop

1. Trigger on a cron schedule (e.g. every 15 min).
2. Fetch current state from data source(s).
3. Compare against stored baseline or threshold.
4. If anomaly detected → format alert and dispatch to notification channel.
5. Update stored state.

## Recommended Tools

- HTTP request node (n8n) or `requests` (Python)
- Simple key-value store for state persistence (Redis / n8n static data)
- Notification: Telegram Bot API, Slack webhook, or email

## Typical Cost

~500–2 000 tokens per poll. Keep system prompt short.

## Known Risks

- Alert fatigue — tune thresholds carefully; add cooldown periods.
- State loss on restart — persist state externally, not in-memory.
- Missed polls — use a reliable scheduler with retry logic.
