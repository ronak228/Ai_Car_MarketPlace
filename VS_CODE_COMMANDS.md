# 🚀 VS Code Commands for Car Price Predictor

## 📋 Quick Start Commands

### **1. Initial Setup (First Time Only)**
```bash
# Install all dependencies
npm run setup
```

### **2. Easy Run Commands**

#### **Option A: Run Everything (Recommended)**
```bash
# Run both Flask (ML) and Express (React) servers
npm run run-mern
```

#### **Option B: Run Separately**
```bash
# Terminal 1: Run Flask ML Server
npm run run-flask

# Terminal 2: Run Express React Server  
npm run start
```

#### **Option C: Development Mode**
```bash
# Run React in development mode with hot reload
npm run client
```

### **3. Individual Server Commands**

#### **Flask Server (ML Model)**
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Run Flask server
python application.py
```

#### **Express Server (React App)**
```bash
# Run Express server
npm run start

# Or with nodemon (auto-restart)
npm run dev
```

#### **React Development Server**
```bash
# Run React in development mode
cd client
npm start
```

## 🎯 **Recommended VS Code Setup**

### **1. Open VS Code Terminal**
- Press `Ctrl + `` (backtick)
- Or go to `Terminal → New Terminal`

### **2. Split Terminal (Recommended)**
- Right-click terminal tab → `Split Terminal`
- Now you have 2 terminals side by side

### **3. Run Commands in Split Terminals**

**Terminal 1 (Flask ML Server):**
```bash
.venv\Scripts\Activate.ps1
python application.py
```

**Terminal 2 (Express React Server):**
```bash
npm run start
```

## 🌐 **Access Your Application**

- **Main Website:** http://localhost:4000
- **Flask API:** http://localhost:5000
- **React Dev Server:** http://localhost:3000 (if using `npm run client`)

## 🔧 **Troubleshooting Commands**

### **If Port is Busy:**
```bash
# Kill all Node processes
taskkill /F /IM node.exe

# Kill all Python processes
taskkill /F /IM python.exe
```

### **If Dependencies Missing:**
```bash
# Reinstall all dependencies
npm run setup
```

### **If Build Fails:**
```bash
# Rebuild React app
npm run build
```

## 📝 **VS Code Extensions (Recommended)**

1. **Python** - For Flask development
2. **ES7+ React/Redux/React-Native snippets** - For React development
3. **Auto Rename Tag** - For JSX editing
4. **Bracket Pair Colorizer** - For better code readability
5. **GitLens** - For Git integration

## 🚀 **One-Command Setup (Ultimate)**

```bash
# This will install everything and run both servers
npm run quick-start
```

## 📊 **Project Structure**
```
car_price_predictor-master/
├── application.py          # Flask ML Server
├── server.js              # Express React Server
├── client/                # React App
│   ├── src/
│   │   ├── components/
│   │   │   ├── CarPricePredictor.js
│   │   │   ├── Home.js
│   │   │   ├── SignIn.js
│   │   │   └── Dashboard.js
│   │   └── App.js
│   └── package.json
├── package.json           # Main project
└── VS_CODE_COMMANDS.md   # This file
```

## 🎯 **Quick Reference**

| Command | Description |
|---------|-------------|
| `npm run setup` | Install all dependencies |
| `npm run run-mern` | Run both servers |
| `npm run run-flask` | Run Flask ML server only |
| `npm run start` | Run Express React server only |
| `npm run client` | Run React dev server |
| `npm run build` | Build React for production |

## ⚡ **Pro Tips for VS Code**

1. **Use Integrated Terminal:** `Ctrl + `` 
2. **Split Terminal:** Right-click → Split Terminal
3. **Quick Open:** `Ctrl + P` to open files
4. **Command Palette:** `Ctrl + Shift + P` for commands
5. **Multi-cursor:** `Alt + Click` for multiple cursors

## 🎉 **You're Ready!**

After running the commands, visit:
- **http://localhost:4000** - Your main application
- **http://localhost:5000** - Flask ML API

**Happy Coding! 🚗💻** 