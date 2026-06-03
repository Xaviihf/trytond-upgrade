DELETE FROM "ir_model_button" WHERE "name" = 'open_lines' AND "model"::text IN ('product.price_list', (SELECT "id"::text FROM "ir_model" WHERE "model" = 'product.price_list'));
