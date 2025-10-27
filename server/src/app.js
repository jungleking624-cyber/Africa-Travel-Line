import express from "express";
import cors from "cors";
import axios from "axios";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import bodyParser from "body-parser";
import { v4 as uuidv4 } from "uuid";
import "dotenv/config";

import authRoutes from "./routes/auth.js";
// import userRoutes from "./routes/users.js";
// import bookingRoutes from "./routes/bookings.js";

// import { errorHandler } from "./middleware/errorHandler.js";
// import { notFound } from "./middleware/notFound.js";

const app = express();

// Middleware
app.use(helmet());
app.use(
  cors({
    origin: process.env.CLIENT_URL || "http://localhost:5173",
    credentials: true,
  })
);
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true }));
app.use(bodyParser.urlencoded({ extended: true }));
// app.use(bodyParser.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Routes;
app.use("/api/auth", authRoutes);
// app.use("/api/users", userRoutes);
// app.use("/api/bookings", bookingRoutes);

const AGENT_ADDRESS =
  process.env.AGENT_ADDRESS ||
  "agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy";
const AGENTVERSE_URL = process.env.AGENTVERSE_URL || "https://agentverse.ai";
const AGENTVERSE_API_KEY = process.env.AGENTVERSE_API_KEY;

// Session storage (use Redis in production)
const sessions = new Map();

// Add this route
app.get("/api/quicktest", (req, res) => {
  res.json({
    message: "Backend is working!",
    timestamp: new Date().toISOString(),
  });
});

// Health check
// app.get("/api/health", (req, res) => {
//   res.json({ status: "OK", timestamp: new Date().toISOString() });
// });
// Health check endpoint
app.get("/api/health", (req, res) => {
  res.json({
    status: "OK",
    message: "Backend is running!",
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || "development",
  });
});

// Helper to create chat protocol message envelope
function createChatEnvelope(agentAddress, message, sessionId) {
  return {
    version: 1,
    sender: "agent1test000000000000000000000000000000000000000000000000000", // Your frontend user agent
    target: agentAddress,
    session: sessionId,
    schema_digest:
      "d3ee07331fddb29c33e955df9349ab9f7c15bf1447a555460094e17e1f07c550", // Chat protocol digest
    protocol_digest:
      "d3ee07331fddb29c33e955df9349ab9f7c15bf1447a555460094e17e1f07c550",
    payload: JSON.stringify({
      timestamp: new Date().toISOString(),
      msg_id: uuidv4(),
      content: [
        {
          type: "text",
          text: message,
        },
      ],
    }),
  };
}

// Chat endpoint
app.post("/api/chat", async (req, res) => {
  try {
    const { message, sessionId } = req.body;

    if (!message || !message.trim()) {
      return res.status(400).json({
        error: "Message is required",
        success: false,
      });
    }

    console.log(`📨 Sending message to agent ${AGENT_ADDRESS}`);
    console.log(`Session: ${sessionId}`);
    console.log(`Message: ${message}`);

    // Get or create session
    let session = sessions.get(sessionId);
    if (!session) {
      session = {
        id: sessionId,
        messages: [],
        createdAt: Date.now(),
      };
      sessions.set(sessionId, session);
    }

    // Add user message to history
    session.messages.push({
      role: "user",
      content: message,
      timestamp: Date.now(),
    });

    // Prepare the envelope for agent communication
    const envelope = {
      version: 1,
      sender: `user_${sessionId}`, // Simulated user address
      target: AGENT_ADDRESS,
      session: sessionId,
      schema_digest: "model", // For text messages
      protocol_digest: "chat_protocol",
      payload: JSON.stringify({
        type: "text",
        text: message,
      }),
    };

    console.log("📤 Sending envelope to agent...");

    // Send to Agentverse Mailbox API
    const response = await axios.post(`${AGENTVERSE_URL}/v1/submit`, envelope, {
      headers: {
        "Content-Type": "application/json",
      },
      timeout: 30000,
    });

    console.log("✅ Message sent successfully");

    // For mailbox agents, we don't get immediate response
    // Instead, tell frontend to poll or use websockets
    res.json({
      success: true,
      message: "Message sent to agent. The agent will respond via mailbox.",
      sessionId: sessionId,
      envelope_id: response.data.envelope_id || null,
      // For demo: return a placeholder
      agentResponse:
        "Your message has been sent to the travel assistant. Please check Agentverse Chat for the response, or use the Agentverse Chat UI directly at https://agentverse.ai",
    });
  } catch (error) {
    console.error("❌ Error sending message:", error.message);
    console.error("Error details:", error.response?.data || error);

    res.status(500).json({
      success: false,
      error: "Failed to send message to agent",
      message:
        "Sorry, I encountered an error. Please try using the Agentverse Chat UI directly.",
      details: error.response?.data || error.message,
    });
  }
});

// Add endpoint to create session
app.post("/api/chat/session", async (req, res) => {
  try {
    const { agentAddress } = req.body;

    // Try different methods to create session
    const methods = [
      {
        method: "POST",
        url: `https://chat.agentverse.ai/api/sessions`,
        data: { agent_address: agentAddress },
      },
      {
        method: "GET",
        url: `https://chat.agentverse.ai/api/sessions/new?agent=${agentAddress}`,
      },
      {
        method: "POST",
        url: `https://chat.agentverse.ai/api/agents/${agentAddress}/sessions`,
        data: {},
      },
    ];

    for (const config of methods) {
      try {
        console.log(`Trying: ${config.method} ${config.url}`);
        const response = await axios({
          method: config.method,
          url: config.url,
          data: config.data,
          headers: {
            Authorization: `Bearer ${AGENTVERSE_API_KEY}`,
            "Content-Type": "application/json",
          },
        });

        console.log("✅ Session created:", response.data);
        return res.json(response.data);
      } catch (err) {
        console.log(`❌ Failed: ${err.response?.status}`);
        continue;
      }
    }

    res.status(500).json({ error: "Could not create session" });
  } catch (error) {
    console.error("Session creation error:", error.message);
    res.status(500).json({
      error: "Failed to create session",
      details: error.message,
    });
  }
});

//Registering user routes
// app.post("/register", async (req, res) => {
//   const { email, password } = req.body;

//   // Input validation
//   if (!email || !password) {
//     return res.status(400).json({
//       error: "Email and password are required"
//     });
//   }

//   // Email format validation
//   const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//   if (!emailRegex.test(email)) {
//     return res.status(400).json({
//       error: "Invalid email format"
//     });
//   }

//   // Password strength validation
//   if (password.length < 8) {
//     return res.status(400).json({
//       error: "Password must be at least 8 characters long"
//     });
//   }

//   try {
//     // Check if user already exists
//     const checkResult = await db.query(
//       "SELECT id FROM users WHERE email = $1",
//       [email.toLowerCase().trim()]
//     );

//     if (checkResult.rows.length > 0) {
//       return res.status(409).json({
//         error: "Email already exists. Try logging in."
//       });
//     }

//     // Hash password before storing
//     const saltRounds = 10;
//     const hashedPassword = await bcrypt.hash(password, saltRounds);

//     // Insert new user
//     const result = await db.query(
//       "INSERT INTO users (email, password) VALUES ($1, $2) RETURNING id, email",
//       [email.toLowerCase().trim(), hashedPassword]
//     );

//     // Generate JWT token for immediate login
//     const token = jwt.sign(
//       { userId: result.rows[0].id, email: result.rows[0].email },
//       process.env.JWT_SECRET,
//       { expiresIn: '24h' }
//     );

//     // Return success response
//     res.status(201).json({
//       message: "User registered successfully",
//       user: {
//         id: result.rows[0].id,
//         email: result.rows[0].email
//       },
//       token
//     });

//   } catch (err) {
//     console.error("Registration error:", err);
//     res.status(500).json({
//       error: "Internal server error. Please try again later."
//     });
//   }
// });

// Error handling
// app.use(notFound);
// app.use(errorHandler);

export default app;
