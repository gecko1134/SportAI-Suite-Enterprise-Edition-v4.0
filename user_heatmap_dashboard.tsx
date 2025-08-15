import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, HeatMapGrid } from 'recharts';

const UserHeatmapDashboard = () => {
  const [selectedFacility, setSelectedFacility] = useState('all');
  const [selectedTimeframe, setSelectedTimeframe] = useState('week');
  const [selectedMemberTier, setSelectedMemberTier] = useState('all');

  // Generate realistic heatmap data
  const generateHeatmapData = () => {
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const hours = Array.from({length: 17}, (_, i) => i + 6); // 6 AM to 10 PM
    const facilities = ['Basketball Courts', 'Soccer Fields', 'Volleyball Courts', 'Player Lab', 'Fitness Center'];
    const memberTiers = ['Venture North Club', 'All-Access', 'Family Plan', 'Basic Member'];

    const data = [];
    
    days.forEach((day, dayIndex) => {
      hours.forEach(hour => {
        facilities.forEach(facility => {
          memberTiers.forEach(tier => {
            let baseUsage = 20;
            
            // Prime time adjustments (6-9 PM, 7-10 AM)
            if ((hour >= 18 && hour <= 21) || (hour >= 7 && hour <= 10)) {
              baseUsage += 40;
            }
            
            // Weekend adjustments
            if (dayIndex >= 5) {
              baseUsage += 20;
            }
            
            // Facility-specific patterns
            if (facility === 'Basketball Courts' && (hour >= 18 && hour <= 21)) {
              baseUsage += 25;
            }
            if (facility === 'Fitness Center' && (hour >= 6 && hour <= 9)) {
              baseUsage += 30;
            }
            if (facility === 'Player Lab' && tier === 'Venture North Club') {
              baseUsage += 35;
            }
            
            // Member tier adjustments
            const tierMultipliers = {
              'Venture North Club': 1.4,
              'All-Access': 1.1,
              'Family Plan': 0.9,
              'Basic Member': 0.7
            };
            
            baseUsage *= tierMultipliers[tier];
            
            // Add some randomness
            const usage = Math.max(5, Math.min(100, baseUsage + (Math.random() - 0.5) * 20));
            
            data.push({
              day,
              dayIndex,
              hour: hour,
              hourDisplay: `${hour}:00`,
              facility,
              memberTier: tier,
              usage: Math.round(usage),
              isPrimeTime: (hour >= 18 && hour <= 21) || (hour >= 7 && hour <= 10),
              isWeekend: dayIndex >= 5
            });
          });
        });
      });
    });
    
    return data;
  };

  const [heatmapData, setHeatmapData] = useState([]);

  useEffect(() => {
    setHeatmapData(generateHeatmapData());
  }, []);

  // Filter data based on selections
  const filteredData = heatmapData.filter(item => {
    if (selectedFacility !== 'all' && item.facility !== selectedFacility) return false;
    if (selectedMemberTier !== 'all' && item.memberTier !== selectedMemberTier) return false;
    return true;
  });

  // Create hourly usage summary
  const hourlyUsage = Array.from({length: 17}, (_, i) => {
    const hour = i + 6;
    const hourData = filteredData.filter(item => item.hour === hour);
    const avgUsage = hourData.reduce((sum, item) => sum + item.usage, 0) / Math.max(hourData.length, 1);
    const isPrimeTime = (hour >= 18 && hour <= 21) || (hour >= 7 && hour <= 10);
    
    return {
      hour: `${hour}:00`,
      usage: Math.round(avgUsage),
      isPrimeTime,
      primeTimeLabel: isPrimeTime ? 'Prime Time' : 'Off-Peak'
    };
  });

  // Create daily usage summary
  const dailyUsage = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].map((day, index) => {
    const dayData = filteredData.filter(item => item.day === day);
    const avgUsage = dayData.reduce((sum, item) => sum + item.usage, 0) / Math.max(dayData.length, 1);
    
    return {
      day: day.substring(0, 3),
      usage: Math.round(avgUsage),
      isWeekend: index >= 5,
      weekendLabel: index >= 5 ? 'Weekend' : 'Weekday'
    };
  });

  // Create facility comparison
  const facilityUsage = ['Basketball Courts', 'Soccer Fields', 'Volleyball Courts', 'Player Lab', 'Fitness Center'].map(facility => {
    const facilityData = filteredData.filter(item => item.facility === facility);
    const avgUsage = facilityData.reduce((sum, item) => sum + item.usage, 0) / Math.max(facilityData.length, 1);
    const primeTimeData = facilityData.filter(item => item.isPrimeTime);
    const primeTimeUsage = primeTimeData.reduce((sum, item) => sum + item.usage, 0) / Math.max(primeTimeData.length, 1);
    const offPeakData = facilityData.filter(item => !item.isPrimeTime);
    const offPeakUsage = offPeakData.reduce((sum, item) => sum + item.usage, 0) / Math.max(offPeakData.length, 1);
    
    return {
      facility: facility.replace(' ', '\n'),
      avgUsage: Math.round(avgUsage),
      primeTime: Math.round(primeTimeUsage),
      offPeak: Math.round(offPeakUsage)
    };
  });

  // Create member tier analysis
  const tierUsage = ['Venture North Club', 'All-Access', 'Family Plan', 'Basic Member'].map(tier => {
    const tierData = filteredData.filter(item => item.memberTier === tier);
    const avgUsage = tierData.reduce((sum, item) => sum + item.usage, 0) / Math.max(tierData.length, 1);
    const primeTimeData = tierData.filter(item => item.isPrimeTime);
    const primeTimeUsage = primeTimeData.reduce((sum, item) => sum + item.usage, 0) / Math.max(primeTimeData.length, 1);
    
    return {
      tier: tier.replace(' ', '\n'),
      avgUsage: Math.round(avgUsage),
      primeTimeUsage: Math.round(primeTimeUsage),
      memberCount: tier === 'Venture North Club' ? 147 : 
                  tier === 'All-Access' ? 743 :
                  tier === 'Family Plan' ? 312 : 587
    };
  });

  // Heatmap grid data for visual heatmap
  const createHeatmapGrid = () => {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const hours = Array.from({length: 17}, (_, i) => i + 6);
    
    return days.map(day => {
      return hours.map(hour => {
        const cellData = filteredData.filter(item => 
          item.day.startsWith(day) && item.hour === hour
        );
        const avgUsage = cellData.reduce((sum, item) => sum + item.usage, 0) / Math.max(cellData.length, 1);
        const isPrimeTime = (hour >= 18 && hour <= 21) || (hour >= 7 && hour <= 10);
        
        return {
          day,
          hour,
          usage: Math.round(avgUsage),
          isPrimeTime
        };
      });
    }).flat();
  };

  const heatmapGrid = createHeatmapGrid();

  const getUsageColor = (usage) => {
    if (usage >= 80) return '#d73027'; // High usage - Red
    if (usage >= 60) return '#fc8d59'; // Medium-high - Orange
    if (usage >= 40) return '#fee08b'; // Medium - Yellow
    if (usage >= 20) return '#e0f3db'; // Low-medium - Light green
    return '#f7f7f7'; // Very low - Light gray
  };

  const getPrimeTimeColor = (isPrime) => {
    return isPrime ? '#1f77b4' : '#aec7e8';
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">🔥 User Usage Heatmap Dashboard</h1>
        <p className="text-gray-600">Real-time facility usage patterns, prime time analysis, and member behavior insights</p>
      </div>

      {/* Filter Controls */}
      <div className="bg-white p-4 rounded-lg shadow-sm mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Facility</label>
            <select 
              value={selectedFacility}
              onChange={(e) => setSelectedFacility(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="all">All Facilities</option>
              <option value="Basketball Courts">Basketball Courts</option>
              <option value="Soccer Fields">Soccer Fields</option>
              <option value="Volleyball Courts">Volleyball Courts</option>
              <option value="Player Lab">Player Lab</option>
              <option value="Fitness Center">Fitness Center</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Member Tier</label>
            <select 
              value={selectedMemberTier}
              onChange={(e) => setSelectedMemberTier(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="all">All Member Tiers</option>
              <option value="Venture North Club">Venture North Club</option>
              <option value="All-Access">All-Access Member</option>
              <option value="Family Plan">Family Plan</option>
              <option value="Basic Member">Basic Member</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Timeframe</label>
            <select 
              value={selectedTimeframe}
              onChange={(e) => setSelectedTimeframe(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="week">This Week</option>
              <option value="month">This Month</option>
              <option value="quarter">This Quarter</option>
            </select>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <div className="text-2xl font-bold text-blue-600">89%</div>
          <div className="text-sm text-gray-600">Peak Hour Utilization</div>
          <div className="text-xs text-green-600">+12% vs last week</div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <div className="text-2xl font-bold text-orange-600">6-9 PM</div>
          <div className="text-sm text-gray-600">Highest Usage Window</div>
          <div className="text-xs text-blue-600">Prime time slot</div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <div className="text-2xl font-bold text-green-600">342</div>
          <div className="text-sm text-gray-600">Active Users Today</div>
          <div className="text-xs text-green-600">+8 vs yesterday</div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <div className="text-2xl font-bold text-purple-600">67%</div>
          <div className="text-sm text-gray-600">Weekend vs Weekday</div>
          <div className="text-xs text-orange-600">Higher weekend usage</div>
        </div>
      </div>

      {/* Visual Heatmap Grid */}
      <div className="bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 className="text-xl font-semibold mb-4">📊 Usage Intensity Heatmap</h2>
        <div className="overflow-x-auto">
          <div className="inline-block min-w-full">
            <div className="grid grid-cols-8 gap-1 text-xs">
              {/* Header row */}
              <div className="p-2 font-medium"></div>
              {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(day => (
                <div key={day} className="p-2 text-center font-medium">{day}</div>
              ))}
              
              {/* Hour rows */}
              {Array.from({length: 17}, (_, i) => i + 6).map(hour => (
                <React.Fragment key={hour}>
                  <div className="p-2 text-right font-medium">{hour}:00</div>
                  {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(day => {
                    const cellData = heatmapGrid.find(item => item.day === day && item.hour === hour);
                    return (
                      <div 
                        key={`${day}-${hour}`}
                        className="p-2 text-center text-xs font-medium border border-gray-200 rounded"
                        style={{ 
                          backgroundColor: getUsageColor(cellData?.usage || 0),
                          color: cellData?.usage >= 60 ? 'white' : 'black'
                        }}
                        title={`${day} ${hour}:00 - ${cellData?.usage || 0}% usage${cellData?.isPrimeTime ? ' (Prime Time)' : ''}`}
                      >
                        {cellData?.usage || 0}%
                      </div>
                    );
                  })}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
        
        {/* Legend */}
        <div className="flex items-center justify-center mt-4 space-x-4">
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium">Usage Intensity:</span>
            <div className="flex space-x-1">
              <div className="w-4 h-4 rounded" style={{backgroundColor: '#f7f7f7'}}></div>
              <span className="text-xs">Low</span>
            </div>
            <div className="flex space-x-1">
              <div className="w-4 h-4 rounded" style={{backgroundColor: '#fee08b'}}></div>
              <span className="text-xs">Medium</span>
            </div>
            <div className="flex space-x-1">
              <div className="w-4 h-4 rounded" style={{backgroundColor: '#fc8d59'}}></div>
              <span className="text-xs">High</span>
            </div>
            <div className="flex space-x-1">
              <div className="w-4 h-4 rounded" style={{backgroundColor: '#d73027'}}></div>
              <span className="text-xs">Peak</span>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Hourly Usage Pattern */}
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold mb-4">⏰ Hourly Usage Patterns</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={hourlyUsage}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hour" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [`${value}%`, 'Usage']}
                labelFormatter={(label) => `Time: ${label}`}
              />
              <Bar 
                dataKey="usage" 
                fill="#1f77b4"
                name="Usage %"
              />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-2 text-sm text-gray-600">
            Prime Time: 6-9 PM, 7-10 AM | Peak usage typically occurs during evening hours
          </div>
        </div>

        {/* Daily Usage Pattern */}
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold mb-4">📅 Daily Usage Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dailyUsage}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [`${value}%`, 'Usage']}
                labelFormatter={(label) => `${label}`}
              />
              <Bar 
                dataKey="usage" 
                fill={(entry) => entry?.isWeekend ? '#ff7f0e' : '#1f77b4'}
                name="Usage %"
              />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-2 text-sm text-gray-600">
            Weekend usage typically 20-30% higher than weekdays
          </div>
        </div>
      </div>

      {/* Prime Time vs Off-Peak Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Facility Comparison */}
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold mb-4">🏟️ Prime Time vs Off-Peak by Facility</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={facilityUsage}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="facility" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="primeTime" fill="#1f77b4" name="Prime Time" />
              <Bar dataKey="offPeak" fill="#aec7e8" name="Off-Peak" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Member Tier Analysis */}
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold mb-4">👥 Usage by Member Tier</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={tierUsage}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="tier" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [`${value}%`, name]}
              />
              <Legend />
              <Bar dataKey="avgUsage" fill="#2ca02c" name="Avg Usage" />
              <Bar dataKey="primeTimeUsage" fill="#d62728" name="Prime Time Usage" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Usage Insights */}
      <div className="bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold mb-4">💡 Usage Pattern Insights</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold text-blue-900">Peak Hours Identified</h3>
            <p className="text-sm text-blue-700 mt-1">
              6-9 PM shows 89% utilization across all facilities. Consider dynamic pricing during peak hours.
            </p>
          </div>
          
          <div className="p-4 bg-green-50 rounded-lg">
            <h3 className="font-semibold text-green-900">Weekend Opportunity</h3>
            <p className="text-sm text-green-700 mt-1">
              Saturday and Sunday show 67% higher usage. Expand weekend programming and events.
            </p>
          </div>
          
          <div className="p-4 bg-orange-50 rounded-lg">
            <h3 className="font-semibold text-orange-900">Off-Peak Optimization</h3>
            <p className="text-sm text-orange-700 mt-1">
              10 AM - 2 PM weekdays underutilized. Target corporate wellness programs and senior activities.
            </p>
          </div>
          
          <div className="p-4 bg-purple-50 rounded-lg">
            <h3 className="font-semibold text-purple-900">VIP Member Behavior</h3>
            <p className="text-sm text-purple-700 mt-1">
              Venture North Club members show 40% higher prime time usage. Premium scheduling working effectively.
            </p>
          </div>
          
          <div className="p-4 bg-red-50 rounded-lg">
            <h3 className="font-semibold text-red-900">Family Plan Patterns</h3>
            <p className="text-sm text-red-700 mt-1">
              Family Plan members peak 3-6 PM on weekends. Align youth programs with these patterns.
            </p>
          </div>
          
          <div className="p-4 bg-yellow-50 rounded-lg">
            <h3 className="font-semibold text-yellow-900">Player Lab Premium</h3>
            <p className="text-sm text-yellow-700 mt-1">
              Player Lab shows highest revenue per hour during prime time. Consider expanding elite training slots.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserHeatmapDashboard;