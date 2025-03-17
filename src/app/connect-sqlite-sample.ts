// import sqlite3 from 'sqlite3';

// // Open a SQLite database
// const db = new sqlite3.Database('./database.sqlite', (err) => {
//   if (err) {
//     console.error('Error opening database:', err.message);
//   } else {
//     console.log('Connected to SQLite database.');
//   }
// });

// // Initialize the database (create the table if it doesn't exist)
// db.serialize(() => {
//   db.run(
//     `CREATE TABLE IF NOT EXISTS users (
//       id INTEGER PRIMARY KEY AUTOINCREMENT,
//       name TEXT NOT NULL,
//       email TEXT NOT NULL UNIQUE
//     );`
//   );
// });

// export default db;