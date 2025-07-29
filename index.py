from flask import Flask, render_template_string
import os

app = Flask(__name__)

def get_dashboard_data():
    """Get comprehensive ERP data based on your manufacturing tables"""
    return {
        # Financial KPIs
        'total_purchases': 4200000,
        'total_sales': 5800000,
        'stock_value': 2100000,
        'profit': 1600000,
        
        # Transaction Counts
        'purchase_count': 284,
        'dispatch_count': 196,
        'stock_count': 89,
        'dyeing_batches': 142,
        'spinning_lots': 168,
        
        # Purchase Analytics (vopspurchase)
        'purchase_by_supplier': {
            'Supplier A - Cotton Mills': 1200000,
            'Supplier B - Wool Traders': 950000,
            'Supplier C - Silk Imports': 780000,
            'Supplier D - Synthetic Fibers': 640000,
            'Supplier E - Dyes & Chemicals': 630000
        },
        
        # Dyeing Process (vopsdyeing)
        'dyeing_status': {
            'Completed': 89,
            'In Process': 31,
            'Quality Check': 14,
            'Pending': 8
        },
        'dyeing_colors': {
            'Red': 24, 'Blue': 21, 'Green': 18, 'Yellow': 16, 
            'Black': 15, 'Brown': 12, 'White': 11, 'Others': 25
        },
        
        # Dispatch Analytics (vopsdispatch)
        'dispatch_by_region': {
            'North India': 45,
            'West India': 38,
            'South India': 42,
            'East India': 28,
            'Export': 43
        },
        'dispatch_value_by_region': {
            'North India': 1450000,
            'West India': 1200000,
            'South India': 1350000,
            'East India': 890000,
            'Export': 1910000
        },
        
        # Stock Analytics (vopscarpetstock)
        'stock_by_category': {
            'Premium Carpets': {'qty': 45, 'value': 675000},
            'Standard Carpets': {'qty': 78, 'value': 468000},
            'Decorative Rugs': {'qty': 156, 'value': 312000},
            'Prayer Rugs': {'qty': 89, 'value': 267000},
            'Runner Carpets': {'qty': 34, 'value': 204000},
            'Floor Mats': {'qty': 234, 'value': 175500}
        },
        
        # Spinning Data (vopsspindata)
        'spinning_production': {
            'Cotton Yarn': 2400,
            'Wool Yarn': 1800,
            'Silk Yarn': 650,
            'Blended Yarn': 1200
        },
        
        # Monthly Trends
        'monthly_sales': [
            480000, 520000, 460000, 580000, 640000, 720000,
            680000, 750000, 690000, 820000, 780000, 860000
        ],
        'monthly_purchases': [
            320000, 340000, 310000, 380000, 420000, 450000,
            430000, 480000, 440000, 520000, 490000, 540000
        ],
        
        # Production Efficiency
        'production_metrics': {
            'Orders Completed': 186,
            'Orders In Progress': 42,
            'Orders Pending': 18,
            'Quality Rejected': 8
        },
        
        # Cost Analysis (vdesncost)
        'cost_breakdown': {
            'Raw Materials': 45,
            'Labor': 25,
            'Dyeing': 12,
            'Finishing': 8,
            'Overheads': 10
        }
    }

@app.route('/')
def dashboard():
    data = get_dashboard_data()
    
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERP Manufacturing Dashboard - Textile & Carpet Industry</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 15px;
        }
        .container { max-width: 1600px; margin: 0 auto; }
        
        .header { 
            background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);
            padding: 25px; text-align: center; border-radius: 20px; 
            margin-bottom: 25px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .header h1 { 
            color: #333; font-size: 2.2em; margin-bottom: 8px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .header p { color: #666; font-size: 1.1em; }
        
        .kpi-section { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
            gap: 20px; margin-bottom: 30px; 
        }
        .kpi-card { 
            background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);
            padding: 20px; border-radius: 15px; text-align: center; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;
            position: relative; overflow: hidden;
        }
        .kpi-card:hover { transform: translateY(-3px); }
        .kpi-card::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        .kpi-icon { font-size: 1.8em; margin-bottom: 10px; color: #667eea; }
        .kpi-value { font-size: 1.6em; font-weight: bold; color: #333; margin-bottom: 5px; }
        .kpi-label { color: #666; font-weight: 600; font-size: 0.9em; }
        .kpi-detail { color: #888; font-size: 0.8em; margin-top: 3px; }
        
        .section-title {
            background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);
            padding: 15px 25px; border-radius: 15px; margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .section-title h2 { 
            color: #333; font-size: 1.4em; margin: 0;
            display: flex; align-items: center; gap: 10px;
        }
        
        .charts-grid { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
            gap: 20px; margin-bottom: 30px; 
        }
        .chart-container { 
            background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);
            padding: 20px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transition: transform 0.3s ease;
        }
        .chart-container:hover { transform: translateY(-2px); }
        .chart-title { 
            font-size: 1.1em; font-weight: bold; color: #333; 
            margin-bottom: 15px; display: flex; align-items: center; gap: 8px;
        }
        
        .data-tables {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px; margin-bottom: 30px;
        }
        .table-container {
            background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);
            padding: 20px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .data-table { width: 100%; border-collapse: collapse; }
        .data-table th, .data-table td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #eee; }
        .data-table th { background: #f8f9fa; font-weight: 600; color: #333; }
        .data-table tr:hover { background: rgba(102, 126, 234, 0.05); }
        
        .status-bar { 
            background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);
            padding: 15px; border-radius: 15px; text-align: center; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.15); margin-bottom: 20px;
        }
        .status-indicator { 
            display: inline-flex; align-items: center; gap: 8px; 
            background: #d4edda; color: #155724; padding: 8px 15px; 
            border-radius: 20px; font-weight: 600; font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .charts-grid, .data-tables { grid-template-columns: 1fr; }
            .kpi-section { grid-template-columns: repeat(2, 1fr); }
            .header h1 { font-size: 1.8em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-industry"></i> ERP Manufacturing Dashboard</h1>
            <p>Comprehensive Textile & Carpet Manufacturing Business Intelligence</p>
        </div>
        
        <!-- KPI Cards -->
        <div class="kpi-section">
            <div class="kpi-card">
                <div class="kpi-icon"><i class="fas fa-shopping-cart"></i></div>
                <div class="kpi-value">₹{{ "{:,}".format(data.total_purchases) }}</div>
                <div class="kpi-label">Total Purchases</div>
                <div class="kpi-detail">{{ data.purchase_count }} transactions</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon"><i class="fas fa-chart-line"></i></div>
                <div class="kpi-value">₹{{ "{:,}".format(data.total_sales) }}</div>
                <div class="kpi-label">Total Sales</div>
                <div class="kpi-detail">{{ data.dispatch_count }} dispatches</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon"><i class="fas fa-boxes"></i></div>
                <div class="kpi-value">₹{{ "{:,}".format(data.stock_value) }}</div>
                <div class="kpi-label">Current Stock Value</div>
                <div class="kpi-detail">{{ data.stock_count }} product lines</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon"><i class="fas fa-coins"></i></div>
                <div class="kpi-value">₹{{ "{:,}".format(data.profit) }}</div>
                <div class="kpi-label">Net Profit</div>
                <div class="kpi-detail">{{ "{:.1f}".format((data.profit/data.total_sales)*100) }}% margin</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon"><i class="fas fa-palette"></i></div>
                <div class="kpi-value">{{ data.dyeing_batches }}</div>
                <div class="kpi-label">Dyeing Batches</div>
                <div class="kpi-detail">Active production</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon"><i class="fas fa-cog"></i></div>
                <div class="kpi-value">{{ data.spinning_lots }}</div>
                <div class="kpi-label">Spinning Lots</div>
                <div class="kpi-detail">Yarn production</div>
            </div>
        </div>
        
        <!-- Sales & Purchase Analytics -->
        <div class="section-title">
            <h2><i class="fas fa-chart-area"></i> Sales & Purchase Analytics</h2>
        </div>
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-line-chart"></i> Monthly Sales vs Purchases</div>
                <div id="salesPurchaseChart"></div>
            </div>
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-truck"></i> Purchase by Supplier</div>
                <div id="supplierChart"></div>
            </div>
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-map-marked-alt"></i> Dispatch by Region</div>
                <div id="dispatchChart"></div>
            </div>
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-rupee-sign"></i> Regional Sales Value</div>
                <div id="regionalValueChart"></div>
            </div>
        </div>
        
        <!-- Production Analytics -->
        <div class="section-title">
            <h2><i class="fas fa-cogs"></i> Production & Manufacturing</h2>
        </div>
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-palette"></i> Dyeing Process Status</div>
                <div id="dyeingStatusChart"></div>
            </div>
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-color-lens"></i> Color Production Distribution</div>
                <div id="colorChart"></div>
            </div>
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-dharmachakra"></i> Spinning Production</div>
                <div id="spinningChart"></div>
            </div>
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-tasks"></i> Production Efficiency</div>
                <div id="efficiencyChart"></div>
            </div>
        </div>
        
        <!-- Inventory & Cost Analysis -->
        <div class="section-title">
            <h2><i class="fas fa-warehouse"></i> Inventory & Cost Analysis</h2>
        </div>
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-layer-group"></i> Stock by Category</div>
                <div id="stockCategoryChart"></div>
            </div>
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-chart-pie"></i> Cost Breakdown</div>
                <div id="costChart"></div>
            </div>
        </div>
        
        <!-- Data Tables -->
        <div class="section-title">
            <h2><i class="fas fa-table"></i> Detailed Analytics</h2>
        </div>
        <div class="data-tables">
            <div class="table-container">
                <h3><i class="fas fa-boxes"></i> Stock Summary by Category</h3>
                <table class="data-table">
                    <thead>
                        <tr><th>Category</th><th>Quantity</th><th>Value (₹)</th></tr>
                    </thead>
                    <tbody>
                        {% for category, details in data.stock_by_category.items() %}
                        <tr>
                            <td>{{ category }}</td>
                            <td>{{ details.qty }}</td>
                            <td>₹{{ "{:,}".format(details.value) }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div class="table-container">
                <h3><i class="fas fa-truck"></i> Regional Dispatch Summary</h3>
                <table class="data-table">
                    <thead>
                        <tr><th>Region</th><th>Orders</th><th>Value (₹)</th></tr>
                    </thead>
                    <tbody>
                        {% for region in data.dispatch_by_region.keys() %}
                        <tr>
                            <td>{{ region }}</td>
                            <td>{{ data.dispatch_by_region[region] }}</td>
                            <td>₹{{ "{:,}".format(data.dispatch_value_by_region[region]) }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="status-bar">
            <div class="status-indicator">
                <i class="fas fa-database"></i>
                <span>ERP System Active • {{ data.purchase_count + data.dispatch_count + data.dyeing_batches }} Records</span>
            </div>
        </div>
    </div>
    
    <script>
        const data = {{ data|tojson }};
        
        // Monthly Sales vs Purchases
        Plotly.newPlot('salesPurchaseChart', [
            {
                x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                y: data.monthly_sales,
                type: 'scatter', mode: 'lines+markers', name: 'Sales',
                line: {color: '#28a745', width: 3}, marker: {size: 6}
            },
            {
                x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                y: data.monthly_purchases,
                type: 'scatter', mode: 'lines+markers', name: 'Purchases',
                line: {color: '#dc3545', width: 3}, marker: {size: 6}
            }
        ], {
            title: '', showlegend: true, 
            margin: {t: 20, b: 40, l: 60, r: 20},
            yaxis: {tickformat: '₹,.0f'}
        });
        
        // Purchase by Supplier
        Plotly.newPlot('supplierChart', [{
            x: Object.keys(data.purchase_by_supplier),
            y: Object.values(data.purchase_by_supplier),
            type: 'bar',
            marker: {color: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4ecdc4']}
        }], {
            title: '', showlegend: false,
            margin: {t: 20, b: 80, l: 60, r: 20},
            yaxis: {tickformat: '₹,.0f'},
            xaxis: {tickangle: -45}
        });
        
        // Dispatch by Region
        Plotly.newPlot('dispatchChart', [{
            values: Object.values(data.dispatch_by_region),
            labels: Object.keys(data.dispatch_by_region),
            type: 'pie', hole: 0.4,
            marker: {colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4ecdc4']}
        }], {
            title: '', showlegend: true,
            margin: {t: 20, b: 20, l: 20, r: 20}
        });
        
        // Regional Sales Value
        Plotly.newPlot('regionalValueChart', [{
            x: Object.keys(data.dispatch_value_by_region),
            y: Object.values(data.dispatch_value_by_region),
            type: 'bar',
            marker: {color: ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#6f42c1']}
        }], {
            title: '', showlegend: false,
            margin: {t: 20, b: 60, l: 60, r: 20},
            yaxis: {tickformat: '₹,.0f'}
        });
        
        // Dyeing Status
        Plotly.newPlot('dyeingStatusChart', [{
            x: Object.keys(data.dyeing_status),
            y: Object.values(data.dyeing_status),
            type: 'bar',
            marker: {color: ['#28a745', '#ffc107', '#17a2b8', '#dc3545']}
        }], {
            title: '', showlegend: false,
            margin: {t: 20, b: 60, l: 40, r: 20}
        });
        
        // Color Distribution
        Plotly.newPlot('colorChart', [{
            values: Object.values(data.dyeing_colors),
            labels: Object.keys(data.dyeing_colors),
            type: 'pie',
            marker: {colors: ['#dc3545', '#007bff', '#28a745', '#ffc107', '#6c757d', '#8B4513', '#FFFFFF', '#FF69B4']}
        }], {
            title: '', showlegend: true,
            margin: {t: 20, b: 20, l: 20, r: 20}
        });
        
        // Spinning Production
        Plotly.newPlot('spinningChart', [{
            x: Object.keys(data.spinning_production),
            y: Object.values(data.spinning_production),
            type: 'bar',
            marker: {color: ['#667eea', '#764ba2', '#f093fb', '#f5576c']}
        }], {
            title: '', showlegend: false,
            margin: {t: 20, b: 60, l: 60, r: 20},
            yaxis: {title: 'Kg Produced'}
        });
        
        // Production Efficiency
        Plotly.newPlot('efficiencyChart', [{
            values: Object.values(data.production_metrics),
            labels: Object.keys(data.production_metrics),
            type: 'pie', hole: 0.3,
            marker: {colors: ['#28a745', '#ffc107', '#17a2b8', '#dc3545']}
        }], {
            title: '', showlegend: true,
            margin: {t: 20, b: 20, l: 20, r: 20}
        });
        
        // Stock by Category (Horizontal Bar)
        Plotly.newPlot('stockCategoryChart', [{
            y: Object.keys(data.stock_by_category),
            x: Object.keys(data.stock_by_category).map(k => data.stock_by_category[k].qty),
            type: 'bar', orientation: 'h',
            marker: {color: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4ecdc4', '#45b7d1']}
        }], {
            title: '', showlegend: false,
            margin: {t: 20, b: 40, l: 120, r: 20},
            xaxis: {title: 'Quantity'}
        });
        
        // Cost Breakdown
        Plotly.newPlot('costChart', [{
            values: Object.values(data.cost_breakdown),
            labels: Object.keys(data.cost_breakdown),
            type: 'pie', hole: 0.4,
            marker: {colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4ecdc4']}
        }], {
            title: '', showlegend: true,
            margin: {t: 20, b: 20, l: 20, r: 20}
        });
        
        // Auto-refresh every 10 minutes
        setTimeout(() => location.reload(), 600000);
    </script>
</body>
</html>
    '''
    
    return render_template_string(html, data=data)

# For Vercel
if __name__ == '__main__':
    app.run(debug=True)