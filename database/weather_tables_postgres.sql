-- Postgres JSONB table for future prod (Aurora/Postgres)
CREATE TABLE weather_api_response (
  id BIGSERIAL PRIMARY KEY,
  location TEXT,
  api_type TEXT,
  request_time TIMESTAMPTZ DEFAULT now(),
  json_data JSONB
);


