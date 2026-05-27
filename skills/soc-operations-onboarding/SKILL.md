---
name: soc-operations-onboarding
description: "Soc Operations Onboarding."
domain: cybersecurity
---

|
| src_addr | src_ip | Network_Traffic |
| dst_addr | dest_ip | Network_Traffic |
| dst_port | dest_port | Network_Traffic |
| fw_action | action | Network_Traffic |
| bytes_sent + bytes_recv | bytes | Network_Traffic |
| user_name | user | Authentication |
| login_result | action | Authentication |
| process_path | process | Endpoint |

### Step 4: Validate Data Quality

```spl
# Verify events are arriving
index=new_source earliest=-1h
| stats count by sourcetype, host, source

# Check field extraction quality
index=new_source earliest=-1h
| stats count(src_ip) as has_src count(dest_ip) as has_dest count(action) as has_action count by sourcetype
| eval src_coverage=round(has_src/count*100,1)
| eval dest_coverage=round(has_dest/count*100,1)
| eval action_coverage=round(has_action/count*100,1)

# Verify CIM compliance
| datamodel Network_Traffic search
| search sourcetype=new_sourcetype
| stats count by source, sourcetype

# Check for timestamp parsing issues
index=new_source earliest=-1h
| eval time_diff=abs(_time - _indextime)
| stats avg(time_diff) as avg_lag max(time_diff) as max_lag by host
| where avg_lag > 300
```

### Step 5: Enable Detection Coverage

```spl
# Verify existing correlation searches work with new source
index=new_source sourcetype=new_sourcetype
| tstats count from datamodel=Authentication by _time span=1h
| timechart span=1h count

# Create source-specific detection rule
[New Source - Authentication Anomaly]
search = index=new_source sourcetype=new_sourcetype action=failure \
| stats count by src_ip, user \
| where count > 10
```

## Onboarding Checklist

- [ ] Log source assessed and approved
- [ ] Network connectivity verified
- [ ] Collection agent/method configured
- [ ] Log forwarding confirmed
- [ ] Parser/field extraction configured
- [ ] CIM compliance validated
- [ ] Data model acceleration enabled
- [ ] Volume within license budget
- [ ] Retention policy configured
- [ ] Detection rules enabled/created
- [ ] Dashboard updated
- [ ] Documentation completed
- [ ] SOC team notified

## References

- [UK NCSC - Onboarding Systems and Log Sources](https://www.ncsc.gov.uk/collection/building-a-security-operations-centre/onboarding-systems-and-log-sources)
- [Sumo Logic - Cloud SIEM Onboarding Checklist](https://help.sumologic.com/docs/cse/get-started-with-cloud-siem/onboarding-checklist-cse/)
- [SIEM Logging Best Practices - Coralogix](https://coralogix.com/guides/siem/siem-logging/)
- [Huntress - SIEM Implementation Guide](https://www.huntress.com/siem-guide/siem-implementation-guide)
