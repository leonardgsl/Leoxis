from pathlib import Path
api=Path('api/site-intelligence.js').read_text()
ui=Path('index.html').read_text()
assert 'LEOXIS_GIS_PROVIDER_DIAGNOSTICS_V270' in api
assert 'LEOXIS_GIS_FOURSQUARE_DIAGNOSTIC' in api
assert 'Bearer [REDACTED]' in api
assert "SUPPORTED_SITE_INTELLIGENCE_COUNTRIES=['Malaysia','Philippines']" in api
assert 'supportedCountries:SUPPORTED_SITE_INTELLIGENCE_COUNTRIES' in api
assert 'LEOXIS_GIS_COVERAGE_UI_V270' in ui
assert 'Malaysia · Philippines' in ui
assert 'LEOXIS_GIS_COVERAGE_RUNTIME_V270' in ui
assert 'LEOXIS_GIS_CANDIDATE_GENERATION_V269' in api
assert 'LEOXIS_GIS_ENTITY_INTEGRITY_V267' in api
assert 'LEOXIS_NAVIGATION_EVENT_V3' in ui
assert 'LEOXIS_GUARDRAIL_CENTRAL_FLOW_V6' in ui
assert 'LEOXIS_VNEXT_NULLSAFE_V6' in ui
print('PASS: GIS diagnostics + coverage v2.7.0')
