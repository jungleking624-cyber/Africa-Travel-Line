import app from "./app.js";
import pool from "./config/database.js";

const PORT = process.env.PORT || 5000;

// Connect to database
pool.connect();

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || "development"}`);
});
