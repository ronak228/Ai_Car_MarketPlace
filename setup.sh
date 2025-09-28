#!/bin/bash

echo "🔧 Setting up Car Price Predictor..."

# Create .env file for local authentication
echo "Creating .env file for local authentication..."
cat > client/.env << EOF
REACT_APP_USE_LOCAL_AUTH=true
EOF

echo "✅ Environment file created!"

# Install dependencies
echo "Installing dependencies..."
npm install

echo "Installing client dependencies..."
cd client && npm install && cd ..

echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Run: npm run run-all"
echo "2. Or run separately:"
echo "   - Backend: python application.py"
echo "   - Frontend: cd client && npm start"
echo ""
echo "For authentication, use any email and any 6-digit OTP code!"
