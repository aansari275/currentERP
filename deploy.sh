#!/bin/bash

echo "🚀 ERP Dashboard Deployment Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Make sure you're in the erp-dashboard-vercel directory"
    exit 1
fi

echo "📁 Current files:"
ls -la

echo -e "\n🔍 Testing local deployment..."
python3 app.py &
SERVER_PID=$!
sleep 3

# Test if server is running
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Local server running successfully"
    kill $SERVER_PID
else
    echo "❌ Local server failed to start"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo -e "\n📦 Ready for Vercel deployment!"
echo -e "\nNext steps:"
echo "1. Initialize git repository:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial ERP Dashboard'"
echo ""
echo "2. Push to GitHub:"
echo "   git remote add origin https://github.com/yourusername/erp-dashboard.git"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Vercel:"
echo "   - Go to vercel.com"
echo "   - Click 'New Project'"
echo "   - Import your GitHub repo"
echo "   - Add environment variables:"
echo "     DB_SERVER=167.71.239.104"
echo "     DB_USER=sa"
echo "     DB_PASSWORD=Empl@786"
echo "     DB_NAME=empl_data19"
echo "   - Click Deploy!"
echo ""
echo "🎉 Your dashboard will be live at: https://your-project.vercel.app"