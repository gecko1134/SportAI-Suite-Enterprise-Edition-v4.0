# =============================================================================
# REACT COMPONENT INTEGRATION INTO STREAMLIT
# =============================================================================

"""
Step 1: Install Required Dependencies
pip install streamlit-components-v1
"""

import streamlit.components.v1 as components
import os
import json

# =============================================================================
# METHOD 1: EMBED REACT COMPONENT DIRECTLY
# =============================================================================

def create_react_heatmap_component():
    """Create a custom React component for the heatmap"""
    
    # Define the React component as an HTML string with embedded JavaScript
    react_heatmap_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        <script src="https://unpkg.com/recharts@2.5.0/umd/Recharts.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <style>
            body { margin: 0; padding: 20px; font-family: Arial, sans-serif; }
            .heatmap-container { width: 100%; height: 600px; }
            .filter-controls { margin-bottom: 20px; display: flex; gap: 10px; }
            .filter-select { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
            .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
            .metric-card { background: white; padding: 16px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .heatmap-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 2px; }
            .heatmap-cell { padding: 8px; text-align: center; border-radius: 4px; font-size: 12px; font-weight: bold; }
            .legend { display: flex; justify-content: center; gap: 20px; margin-top: 20px; }
            .legend-item { display: flex; align-items: center; gap: 8px; }
            .legend-color { width: 20px; height: 20px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div id="react-heatmap"></div>
        
        <script type="text/babel">
            const { useState, useEffect } = React;
            const { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } = Recharts;
            
            const UserHeatmapDashboard = () => {
                const [selectedFacility, setSelectedFacility] = useState('all');
                const [selectedTier, setSelectedTier] = useState('all');
                const [heatmapData, setHeatmapData] = useState([]);
                
                // Generate sample data
                useEffect(() => {
                    const generateData = () => {
                        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
                        const hours = Array.from({length: 17}, (_, i) => i + 6);
                        const data = [];
                        
                        days.forEach((day, dayIndex) => {
                            hours.forEach(hour => {
                                let usage = 30 + Math.random() * 40;
                                if ((hour >= 18 && hour <= 21) || (hour >= 7 && hour <= 10)) usage += 20;
                                if (dayIndex >= 5) usage += 15;
                                data.push({ day, hour, usage: Math.round(usage) });
                            });
                        });
                        setHeatmapData(data);
                    };
                    generateData();
                }, []);
                
                const getUsageColor = (usage) => {
                    if (usage >= 80) return '#d73027';
                    if (usage >= 60) return '#fc8d59';
                    if (usage >= 40) return '#fee08b';
                    if (usage >= 20) return '#e0f3db';
                    return '#f7f7f7';
                };
                
                return (
                    <div>
                        <h1>🔥 User Usage Heatmap Dashboard</h1>
                        
                        <div className="filter-controls">
                            <select 
                                className="filter-select"
                                value={selectedFacility}
                                onChange={(e) => setSelectedFacility(e.target.value)}
                            >
                                <option value="all">All Facilities</option>
                                <option value="Basketball">Basketball Courts</option>
                                <option value="Soccer">Soccer Fields</option>
                                <option value="Volleyball">Volleyball Courts</option>
                            </select>
                            
                            <select 
                                className="filter-select"
                                value={selectedTier}
                                onChange={(e) => setSelectedTier(e.target.value)}
                            >
                                <option value="all">All Member Tiers</option>
                                <option value="VIP">Venture North Club</option>
                                <option value="Premium">All-Access</option>
                                <option value="Family">Family Plan</option>
                            </select>
                        </div>
                        
                        <div className="metrics-grid">
                            <div className="metric-card">
                                <h3>89%</h3>
                                <p>Peak Hour Utilization</p>
                            </div>
                            <div className="metric-card">
                                <h3>6-9 PM</h3>
                                <p>Prime Time Window</p>
                            </div>
                            <div className="metric-card">
                                <h3>342</h3>
                                <p>Active Users Today</p>
                            </div>
                            <div className="metric-card">
                                <h3>+67%</h3>
                                <p>Weekend Usage Boost</p>
                            </div>
                        </div>
                        
                        <div className="heatmap-grid">
                            <div style={{padding: '8px', fontWeight: 'bold'}}></div>
                            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(day => (
                                <div key={day} style={{padding: '8px', fontWeight: 'bold', textAlign: 'center'}}>{day}</div>
                            ))}
                            
                            {Array.from({length: 17}, (_, i) => i + 6).map(hour => (
                                <React.Fragment key={hour}>
                                    <div style={{padding: '8px', fontWeight: 'bold', textAlign: 'right'}}>{hour}:00</div>
                                    {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(day => {
                                        const cellData = heatmapData.find(d => d.day === day && d.hour === hour);
                                        const usage = cellData ? cellData.usage : 0;
                                        return (
                                            <div 
                                                key={`${day}-${hour}`}
                                                className="heatmap-cell"
                                                style={{
                                                    backgroundColor: getUsageColor(usage),
                                                    color: usage >= 60 ? 'white' : 'black'
                                                }}
                                                title={`${day} ${hour}:00 - ${usage}% usage`}
                                            >
                                                {usage}%
                                            </div>
                                        );
                                    })}
                                </React.Fragment>
                            ))}
                        </div>
                        
                        <div className="legend">
                            <div className="legend-item">
                                <div className="legend-color" style={{backgroundColor: '#f7f7f7'}}></div>
                                <span>Low (0-20%)</span>
                            </div>
                            <div className="legend-item">
                                <div className="legend-color" style={{backgroundColor: '#fee08b'}}></div>
                                <span>Medium (20-60%)</span>
                            </div>
                            <div className="legend-item">
                                <div className="legend-color" style={{backgroundColor: '#fc8d59'}}></div>
                                <span>High (60-80%)</span>
                            </div>
                            <div className="legend-item">
                                <div className="legend-color" style={{backgroundColor: '#d73027'}}></div>
                                <span>Peak (80%+)</span>
                            </div>
                        </div>
                    </div>
                );
            };
            
            ReactDOM.render(<UserHeatmapDashboard />, document.getElementById('react-heatmap'));
        </script>
    </body>
    </html>
    """
    
    return react_heatmap_html

# =============================================================================
# METHOD 2: STREAMLIT COMPONENT WRAPPER
# =============================================================================

def render_react_heatmap(data=None, height=800):
    """Render the React heatmap component in Streamlit"""
    
    # Pass data to React component
    component_data = {
        "heatmap_data": data or [],
        "facilities": ["Basketball Courts", "Soccer Fields", "Volleyball Courts",