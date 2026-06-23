DELETE FROM "ir_module" WHERE name = 'google_maps';
DELETE FROM "ir_module" WHERE name IN ('account_es', 'account_es_sii') AND state != 'activated';
DELETE FROM "ir_module" WHERE name = 'account_de_skr03' AND state != 'activated';
