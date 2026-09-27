from pathlib import Path
s=Path('api/site-intelligence.js').read_text()
h=Path('index.html').read_text()
assert 'LEOXIS_GIS_SUPPORTED_COUNTRY_SEARCH_V271' in s
assert "SEARCH_COUNTRY_CODES=['my','ph']" in s
assert "countrycodes',allowedCountryCodes.join(',')" in s
assert "filter(x=>allowedCountryCodes.includes(norm(x.address?.country_code||'')))" in s
assert "supportedCountries:['Malaysia','Philippines']" in s
assert "engine:'LEOXIS_GIS_SUPPORTED_COUNTRY_SEARCH_V271'" in s
assert 'LEOXIS_GIS_PROVIDER_DIAGNOSTICS_V270' in s
assert 'LEOXIS_GIS_ENTITY_INTEGRITY_V267' in s
assert 'LEOXIS_GIS_VENUE_INTENT_V268' in s
assert 'LEOXIS_GIS_COVERAGE_UI_V270' in h
assert 'LEOXIS_NAVIGATION_EVENT_V3' in h
assert 'LEOXIS_GUARDRAIL_CENTRAL_FLOW_V6' in h
assert 'LEOXIS_VNEXT_NULLSAFE_V6' in h
print('PASS: supported-country-only GIS search v2.7.1')
