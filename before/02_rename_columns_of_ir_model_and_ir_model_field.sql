ALTER TABLE IF EXISTS "ir_model" RENAME COLUMN "name" TO "string";
ALTER TABLE IF EXISTS "ir_model" RENAME COLUMN "model" TO "name";
ALTER TABLE IF EXISTS "ir_model_field" RENAME COLUMN "field_description" TO "string";