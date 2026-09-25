# LEOXIS staged learning data
`data/staging/<customer_id>/<batch_id>/` is the controlled persistence boundary.
Only batches that pass Stage 6.1 may enter. Each batch is append-only and carries SHA-256 hashes plus an immutable manifest. Customer folders are physically separated. This is a staging layer, not yet the production multi-tenant database.
