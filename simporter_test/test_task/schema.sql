
DROP TABLE IF EXISTS data;

CREATE TABLE data(
  asin      VARCHAR(10) NOT NULL,
  brand     TEXT NOT NULL,
  id        VARCHAR(14) NOT NULL PRIMARY KEY,
  source    TEXT NOT NULL,
  stars     TINYINT  NOT NULL,
  timestamp TIMESTAMP  NOT NULL
);