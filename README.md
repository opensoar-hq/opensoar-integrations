# OpenSOAR Integrations

Community-contributed integration packs for the [OpenSOAR](https://github.com/opensoar-hq/opensoar) SOAR platform.

## Available Integrations

| Integration | Category | Status | Actions |
|-------------|----------|--------|---------|
| CrowdStrike Falcon | EDR | In Development | Isolate host, lookup detection, search IOCs |
| SentinelOne | EDR | In Development | Isolate endpoint, get threats, remediate |
| Jira | ITSM | In Development | Create issue, update issue, transition |
| PagerDuty | Alerting | In Development | Trigger incident, acknowledge, resolve |
| MISP | Threat Intel | In Development | Search events, add attribute, lookup IOC |

## Built-in Integrations

These integrations ship with OpenSOAR core and don't need this package:
- Elastic Security
- VirusTotal
- AbuseIPDB
- Slack
- Email (SMTP)

## Building an Integration

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

Quick start:
1. Copy `templates/integration-template/` to `integrations/your-tool/`
2. Edit `manifest.yaml` with your tool's config and actions
3. Implement the connector and actions
4. Add tests
5. Submit a PR

## Part of OpenSOAR

See the [main repo](https://github.com/opensoar-hq/opensoar) for full documentation.
