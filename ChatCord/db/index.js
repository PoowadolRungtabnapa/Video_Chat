const pgp = require('pg-promise')()
const connectionString =
    "postgres://postgres:Mac126218@127.0.0.1:5432/WebChat"

const db = pgp(connectionString)

module.exports = db;