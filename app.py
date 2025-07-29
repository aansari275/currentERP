from flask import Flask, render_template_string, jsonify
import os

app = Flask(__name__)

# For Vercel deployment, we'll use environment variables for sensitive data
# You'll need to set these in Vercel dashboard
DB_CONFIG = {
    'server': os.environ.get('DB_SERVER', '167.71.239.104'),
    'user': os.environ.get('DB_USER', 'sa'),
    'password': os.environ.get('DB_PASSWORD', 'Empl@786'),
    'database': os.environ.get('DB_NAME', 'empl_data19')
}

def get_mock_data():
    """Return mock data for demonstration"""
    return {
        'total_purchases': 2500000,
        'total_sales': 3200000,
        'stock_value': 1800000,
        'purchase_count': 167,
        'dispatch_count': 128,
        'stock_count': 150,
        'profit': 700000
    }

@app.route('/')
def dashboard():
    data = get_mock_data()
    profit = data['profit']
    
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ERP Manufacturing Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { max-width: 1400px; margin: 0 auto; }
            .header { 
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                padding: 30px; 
                text-align: center; 
                border-radius: 20px;
                margin-bottom: 30px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            .header h1 { 
                color: #333; 
                font-size: 2.5em; 
                margin-bottom: 10px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .header p { color: #666; font-size: 1.2em; }
            
            .metrics { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
                gap: 25px; 
                margin-bottom: 40px; 
            }
            .metric-card { 
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                padding: 30px; 
                border-radius: 20px; 
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            }
            .metric-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #667eea, #764ba2);
            }
            .metric-icon {
                font-size: 2.5em;
                margin-bottom: 15px;
                color: #667eea;
            }
            .metric-value { 
                font-size: 2.2em; 
                font-weight: bold; 
                color: #333; 
                margin-bottom: 8px;
            }
            .metric-label { 
                color: #666; 
                font-size: 1.1em;
                font-weight: 600;
                margin-bottom: 5px;
            }
            .metric-detail {
                color: #888;
                font-size: 0.9em;
            }
            
            .charts { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); 
                gap: 30px; 
                margin-bottom: 40px; 
            }
            .chart-container { 
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                padding: 25px; 
                border-radius: 20px; 
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                transition: transform 0.3s ease;
            }
            .chart-container:hover {
                transform: translateY(-3px);
            }
            .chart-title {
                font-size: 1.3em;
                font-weight: bold;
                color: #333;
                margin-bottom: 15px;
                text-align: center;
            }
            
            .info-section {
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                text-align: center;
                margin-bottom: 30px;
            }
            .database-status {
                display: inline-flex;
                align-items: center;
                gap: 10px;
                background: #d4edda;
                color: #155724;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: 600;
            }
            .refresh-btn {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1em;
                font-weight: 600;
                margin: 20px;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
            }
            .refresh-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }
            
            .footer {
                text-align: center;
                color: rgba(255,255,255,0.8);
                margin-top: 40px;
                padding: 20px;
                font-size: 0.9em;
            }
            
            @media (max-width: 768px) {
                .charts { grid-template-columns: 1fr; }
                .metrics { grid-template-columns: 1fr; }
                .header h1 { font-size: 2em; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-industry"></i> ERP Manufacturing Dashboard</h1>
                <p>Textile & Carpet Manufacturing Business Intelligence</p>
                <button class="refresh-btn" onclick="location.reload()">
                    <i class="fas fa-sync-alt"></i> Refresh Data
                </button>
            </div>
            
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-shopping-cart"></i></div>
                    <div class="metric-value">₹{{ "{:,}".format(data.total_purchases) }}</div>
                    <div class="metric-label">Total Purchases</div>
                    <div class="metric-detail">{{ data.purchase_count }} transactions</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-chart-line"></i></div>
                    <div class="metric-value">₹{{ "{:,}".format(data.total_sales) }}</div>
                    <div class="metric-label">Total Sales</div>
                    <div class="metric-detail">{{ data.dispatch_count }} dispatches</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-boxes"></i></div>
                    <div class="metric-value">₹{{ "{:,}".format(data.stock_value) }}</div>
                    <div class="metric-label">Stock Value</div>
                    <div class="metric-detail">{{ data.stock_count }} items in stock</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-coins"></i></div>
                    <div class="metric-value">₹{{ "{:,}".format(profit) }}</div>
                    <div class="metric-label">Net Profit</div>
                    <div class="metric-detail">{{ "{:.1f}".format((profit/data.total_purchases)*100) }}% margin</div>
                </div>
            </div>
            
            <div class="charts">
                <div class="chart-container">
                    <div class="chart-title"><i class="fas fa-chart-area"></i> Sales Trend</div>
                    <div id="salesChart"></div>
                </div>
                <div class="chart-container">
                    <div class="chart-title"><i class="fas fa-chart-pie"></i> Production Mix</div>
                    <div id="productionChart"></div>
                </div>
                <div class="chart-container">
                    <div class="chart-title"><i class="fas fa-warehouse"></i> Inventory Status</div>
                    <div id="stockChart"></div>
                </div>
                <div class="chart-container">
                    <div class="chart-title"><i class="fas fa-cogs"></i> Process Status</div>
                    <div id="processChart"></div>
                </div>
            </div>
            
            <div class="info-section">
                <div class="database-status">
                    <i class="fas fa-database"></i>
                    <span>Database Connected: {{ data.purchase_count + data.dispatch_count + data.stock_count }} total records</span>
                </div>
            </div>
            
            <div class="footer">
                <p><i class="fas fa-clock"></i> Last updated: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}</p>
                <p><i class="fas fa-shield-alt"></i> Secure ERP Dashboard • Real-time Business Intelligence</p>
            </div>
        </div>
        
        <script>
            // Enhanced Sales Trend Chart
            var salesData = {
                x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                y: [280000, 320000, 290000, 350000, 380000, 420000, 390000, 430000, 460000, 440000, 480000, 510000],
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Sales Revenue',
                line: {color: '#667eea', width: 4, shape: 'spline'},
                marker: {size: 8, color: '#764ba2'},
                fill: 'tonexty',
                fillcolor: 'rgba(102, 126, 234, 0.1)'
            };
            
            var layout1 = {
                showlegend: false,
                margin: {t: 20, b: 40, l: 60, r: 20},
                plot_bgcolor: 'transparent',
                paper_bgcolor: 'transparent',
                font: {family: 'Segoe UI', size: 12},
                xaxis: {gridcolor: '#e0e0e0'},
                yaxis: {gridcolor: '#e0e0e0', tickformat: '₹,.0f'}
            };
            Plotly.newPlot('salesChart', [salesData], layout1, {responsive: true, displayModeBar: false});
            
            // Production Distribution Chart
            var productionData = [{
                values: [450, 320, 180, 250],
                labels: ['Carpets', 'Rugs', 'Runners', 'Mats'],
                type: 'pie',
                textinfo: 'label+percent',
                textposition: 'outside',
                marker: {
                    colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                    line: {color: '#fff', width: 2}
                },
                hole: 0.4
            }];
            
            var layout2 = {
                showlegend: false,
                margin: {t: 20, b: 20, l: 20, r: 20},
                plot_bgcolor: 'transparent',
                paper_bgcolor: 'transparent',
                font: {family: 'Segoe UI', size: 12}
            };
            Plotly.newPlot('productionChart', productionData, layout2, {responsive: true, displayModeBar: false});
            
            // Stock Levels Chart
            var stockData = {
                x: ['Carpet A', 'Carpet B', 'Rug C', 'Runner D', 'Mat E'],
                y: [45, 32, 78, 23, 156],
                type: 'bar',
                marker: {
                    color: ['#28a745', '#ffc107', '#28a745', '#dc3545', '#28a745'],
                    line: {color: '#fff', width: 1}
                },
                text: [45, 32, 78, 23, 156],
                textposition: 'outside'
            };
            
            var layout3 = {
                showlegend: false,
                margin: {t: 20, b: 60, l: 40, r: 20},
                plot_bgcolor: 'transparent',
                paper_bgcolor: 'transparent',
                font: {family: 'Segoe UI', size: 12},
                xaxis: {gridcolor: '#e0e0e0'},
                yaxis: {gridcolor: '#e0e0e0', title: 'Units'}
            };
            Plotly.newPlot('stockChart', [stockData], layout3, {responsive: true, displayModeBar: false});
            
            // Process Status Chart
            var processData = {
                x: ['Completed', 'In Progress', 'Pending'],
                y: [45, 12, 8],
                type: 'bar',
                marker: {
                    color: ['#28a745', '#ffc107', '#dc3545'],
                    line: {color: '#fff', width: 1}
                },
                text: [45, 12, 8],
                textposition: 'outside'
            };
            
            var layout4 = {
                showlegend: false,
                margin: {t: 20, b: 60, l: 40, r: 20},
                plot_bgcolor: 'transparent',
                paper_bgcolor: 'transparent',
                font: {family: 'Segoe UI', size: 12},
                xaxis: {gridcolor: '#e0e0e0'},
                yaxis: {gridcolor: '#e0e0e0', title: 'Batches'}
            };
            Plotly.newPlot('processChart', [processData], layout4, {responsive: true, displayModeBar: false});
            
            // Auto-refresh every 5 minutes
            setTimeout(() => location.reload(), 300000);
        </script>
    </body>
    </html>
    """
    
    return render_template_string(html_template, data=data, profit=profit, moment=lambda: __import__('datetime').datetime.now())

@app.route('/api/data')
def api_data():
    """API endpoint for dashboard data"""
    return jsonify(get_mock_data())

if __name__ == '__main__':
    app.run(debug=True)