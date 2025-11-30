-- Migration: add params_json, response_time_ms, status_code, request_url
-- Run this on your Oracle DB as the schema owner (or adapt schema names)
ALTER TABLE weather_user.weather_api_response ADD (params_json CLOB);
ALTER TABLE weather_user.weather_api_response ADD (response_time_ms NUMBER);
ALTER TABLE weather_user.weather_api_response ADD (status_code NUMBER);
ALTER TABLE weather_user.weather_api_response ADD (request_url VARCHAR2(400));

-- Consider adding indexes on request_time or api_type if needed