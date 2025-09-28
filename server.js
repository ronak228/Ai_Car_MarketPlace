const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from React build
app.use(express.static(path.join(__dirname, 'client/build')));

// Basic routes for car rental website
app.get('/api/health', (req, res) => {
  res.json({ message: 'Car Rental API is running' });
});

// Authentication routes (placeholder for now)
app.post('/api/auth/signin', (req, res) => {
  // Placeholder authentication logic
  const { email, password } = req.body;
  
  if (email === 'admin@example.com' && password === 'password') {
    res.json({
      success: true,
      token: 'dummy-jwt-token',
      user: {
        id: 1,
        name: 'Admin User',
        email: email
      }
    });
  } else {
    res.status(401).json({
      success: false,
      message: 'Invalid credentials'
    });
  }
});

app.post('/api/auth/signup', (req, res) => {
  // Placeholder signup logic
  const { name, email, password } = req.body;
  
  res.json({
    success: true,
    message: 'User registered successfully',
    user: {
      id: 2,
      name: name,
      email: email
    }
  });
});

// Car rental API routes (placeholder)
app.get('/api/cars', (req, res) => {
  // Placeholder car data
  const cars = [
    {
      id: 1,
      name: 'Toyota Camry',
      company: 'Toyota',
      year: 2022,
      price: 50,
      image: 'https://via.placeholder.com/300x200?text=Toyota+Camry',
      available: true
    },
    {
      id: 2,
      name: 'Honda Civic',
      company: 'Honda',
      year: 2021,
      price: 45,
      image: 'https://via.placeholder.com/300x200?text=Honda+Civic',
      available: true
    },
    {
      id: 3,
      name: 'BMW 3 Series',
      company: 'BMW',
      year: 2023,
      price: 80,
      image: 'https://via.placeholder.com/300x200?text=BMW+3+Series',
      available: true
    }
  ];
  
  res.json(cars);
});

// Catch all handler for React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
});

const PORT = process.env.PORT || 4000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Car Rental API: http://localhost:${PORT}/api`);
  console.log(`React App: http://localhost:${PORT}`);
}); 