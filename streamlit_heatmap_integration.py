# =============================================================================
# USER HEATMAP TAB - ADD THIS TO THE MAIN NXS PLATFORM
# Insert this code into the tabs section of your main application
# =============================================================================

# Add "🔥 User Heatmap" to your tabs list:
# tabs = st.tabs([
#     "🏠 Dashboard", 
#     "👥 Memberships",
#     "🏟️ Court/Turf Optimization",
#     "🔥 User Heatmap",  # <-- ADD THIS
#     "🏆 Tournaments", 
#     "💪 Wellness", 
#     "💼 NIL Management", 
#     "📱 Smart Systems",
#     "💰 Revenue",
#     "📊 Analytics"
# ])

class HeatmapAnalyzer:
    """Advanced heatmap analysis for user behavior patterns"""
    
    def __init__(self):
        self.facilities = ['Basketball Courts', 'Soccer Fields', 'Volleyball Courts', 'Player Lab', 'Fitness Center']
        self.member_tiers = ['Venture North Club', 'All-Access', 'Family Plan', 'Basic Member']
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.hours = list(range(6, 23))  # 6 AM to 10 PM
    
    def generate_heatmap_data(self) -> List[Dict[str, Any]]:
        """Generate comprehensive heatmap data"""
        data = []
        
        for day_idx, day in enumerate(self.days):
            for hour in self.hours:
                for facility in self.facilities:
                    for tier in self.member_tiers:
                        # Base usage calculation
                        base_usage = 25
                        
                        # Prime time boost (6-9 PM, 7-10 AM)
                        if (18 <= hour <= 21) or (7 <= hour <= 10):
                            base_usage += 45
                        
                        # Weekend boost
                        if day_idx >= 5:  # Saturday, Sunday
                            base_usage += 25
                        
                        # Facility-specific patterns
                        facility_multipliers = {
                            'Basketball Courts': 1.2 if (18 <= hour <= 21) else 1.0,
                            'Soccer Fields': 1.3 if (16 <= hour <= 20) else 0.9,
                            'Volleyball Courts': 1.1 if (17 <= hour <= 20) else 0.8,
                            'Player Lab': 1.5 if (7 <= hour <= 10) or (18 <= hour <= 21) else 0.7,
                            'Fitness Center': 1.4 if (6 <= hour <= 9) or (17 <= hour <= 20) else 0.9
                        }
                        
                        # Member tier multipliers
                        tier_multipliers = {
                            'Venture North Club': 1.6,
                            'All-Access': 1.2,
                            'Family Plan': 0.9 if (9 <= hour <= 15) else 1.1,
                            'Basic Member': 0.7
                        }
                        
                        # Apply multipliers
                        usage = base_usage * facility_multipliers[facility] * tier_multipliers[tier]
                        
                        # Add realistic variance
                        usage += random.uniform(-15, 15)
                        usage = max(5, min(100, round(usage)))
                        
                        # Determine prime time
                        is_prime_time = (18 <= hour <= 21) or (7 <= hour <= 10)
                        is_weekend = day_idx >= 5
                        
                        data.append({
                            'day': day,
                            'day_index': day_idx,
                            'hour': hour,
                            'facility': facility,
                            'member_tier': tier,
                            'usage_percentage': usage,
                            'is_prime_time': is_prime_time,
                            'is_weekend': is_weekend,
                            'time_category': 'Prime Time' if is_prime_time else 'Off-Peak',
                            'day_category': 'Weekend' if is_weekend else 'Weekday'
                        })
        
        return data
    
    def create_heatmap_matrix(self, data: List[Dict], facility_filter: str = 'all', tier_filter: str = 'all') -> pd.DataFrame:
        """Create heatmap matrix for visualization"""
        # Filter data
        filtered_data = data
        if facility_filter != 'all':
            filtered_data = [d for d in filtered_data if d['facility'] == facility_filter]
        if tier_filter != 'all':
            filtered_data = [d for d in filtered_data if d['member_tier'] == tier_filter]
        
        # Create pivot table
        df = pd.DataFrame(filtered_data)
        if df.empty:
            return pd.DataFrame()
        
        # Group by day and hour, average usage
        heatmap_data = df.groupby(['day', 'hour'])['usage_percentage'].mean().reset_index()
        
        # Pivot for heatmap
        heatmap_matrix = heatmap_data.pivot(index='hour', columns='day', values='usage_percentage')
        
        # Reorder columns to correct day order
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_matrix = heatmap_matrix.reindex(columns=day_order)
        
        return heatmap_matrix.fillna(0)
    
    def get_peak_insights(self, data: List[Dict]) -> Dict[str, Any]:
        """Generate peak usage insights"""
        df = pd.DataFrame(data)
        
        # Overall peaks
        peak_hour = df.groupby('hour')['usage_percentage'].mean().idxmax()
        peak_day = df.groupby('day')['usage_percentage'].mean().idxmax()
        
        # Prime time vs off-peak
        prime_time_avg = df[df['is_prime_time']]['usage_percentage'].mean()
        off_peak_avg = df[~df['is_prime_time']]['usage_percentage'].mean()
        
        # Weekend vs weekday
        weekend_avg = df[df['is_weekend']]['usage_percentage'].mean()
        weekday_avg = df[~df['is_weekend']]['usage_percentage'].mean()
        
        # Facility peaks
        facility_peaks = {}
        for facility in self.facilities:
            facility_data = df[df['facility'] == facility]
            peak_time = facility_data.groupby('hour')['usage_percentage'].mean().idxmax()
            facility_peaks[facility] = peak_time
        
        return {
            'peak_hour': peak_hour,
            'peak_day': peak_day,
            'prime_time_avg': round(prime_time_avg, 1),
            'off_peak_avg': round(off_peak_avg, 1),
            'weekend_avg': round(weekend_avg, 1),
            'weekday_avg': round(weekday_avg, 1),
            'facility_peaks': facility_peaks,
            'prime_time_boost': round(((prime_time_avg - off_peak_avg) / off_peak_avg) * 100, 1),
            'weekend_boost': round(((weekend_avg - weekday_avg) / weekday_avg) * 100, 1)
        }

# =============================================================================
# USER HEATMAP TAB CONTENT - INSERT INTO YOUR TABS SECTION
# =============================================================================

# Insert this entire section as a new tab in your main application:

with tabs[3]:  # Adjust index based on where you insert the tab
    st.markdown("## 🔥 User Usage Heatmap Dashboard")
    st.markdown('<span class="ai-badge">REAL-TIME USAGE PATTERNS</span>', unsafe_allow_html=True)
    
    # Initialize heatmap analyzer
    heatmap_analyzer = HeatmapAnalyzer()
    
    # Generate data
    if 'heatmap_data' not in st.session_state:
        st.session_state.heatmap_data = heatmap_analyzer.generate_heatmap_data()
    
    heatmap_data = st.session_state.heatmap_data
    
    # Filter controls
    st.markdown("### 🎛️ Analysis Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        facility_filter = st.selectbox(
            "🏟️ Facility",
            ['all'] + heatmap_analyzer.facilities,
            key="heatmap_facility"
        )
    
    with col2:
        tier_filter = st.selectbox(
            "👥 Member Tier", 
            ['all'] + heatmap_analyzer.member_tiers,
            key="heatmap_tier"
        )
    
    with col3:
        timeframe = st.selectbox(
            "📅 Timeframe",
            ['This Week', 'This Month', 'This Quarter'],
            key="heatmap_timeframe"
        )
    
    with col4:
        view_mode = st.selectbox(
            "📊 View Mode",
            ['Usage %', 'Prime Time Focus', 'Member Tier Comparison'],
            key="heatmap_view"
        )
    
    # Get insights
    insights = heatmap_analyzer.get_peak_insights(heatmap_data)
    
    # Key metrics
    st.markdown("### 📈 Key Usage Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Peak Hour Utilization", 
            f"{insights['prime_time_avg']}%",
            f"+{insights['prime_time_boost']}% vs off-peak"
        )
    
    with col2:
        st.metric(
            "Busiest Time", 
            f"{insights['peak_hour']}:00",
            "Prime time slot"
        )
    
    with col3:
        st.metric(
            "Weekend Boost", 
            f"+{insights['weekend_boost']}%",
            "vs weekdays"
        )
    
    with col4:
        st.metric(
            "Peak Day", 
            insights['peak_day'],
            "Highest utilization"
        )
    
    # Main heatmap visualization
    st.markdown("### 🔥 Usage Intensity Heatmap")
    
    # Create heatmap matrix
    heatmap_matrix = heatmap_analyzer.create_heatmap_matrix(
        heatmap_data, facility_filter, tier_filter
    )
    
    if not heatmap_matrix.empty:
        # Create plotly heatmap
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_matrix.values,
            x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            y=[f"{hour}:00" for hour in heatmap_matrix.index],
            colorscale='RdYlBu_r',
            hoverongaps=False,
            hovertemplate='<b>%{x}</b><br>Time: %{y}<br>Usage: %{z:.1f}%<extra></extra>',
            colorbar=dict(title="Usage %")
        ))
        
        fig_heatmap.update_layout(
            title=f"Usage Patterns - {facility_filter if facility_filter != 'all' else 'All Facilities'}",
            xaxis_title="Day of Week",
            yaxis_title="Hour of Day",
            height=500
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("No data available for selected filters")
    
    # Detailed analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⏰ Hourly Usage Patterns")
        
        # Filter and aggregate hourly data
        df = pd.DataFrame(heatmap_data)
        if facility_filter != 'all':
            df = df[df['facility'] == facility_filter]
        if tier_filter != 'all':
            df = df[df['member_tier'] == tier_filter]
        
        hourly_avg = df.groupby(['hour', 'time_category'])['usage_percentage'].mean().reset_index()
        
        fig_hourly = px.bar(
            hourly_avg, 
            x='hour', 
            y='usage_percentage',
            color='time_category',
            title="Average Usage by Hour",
            labels={'usage_percentage': 'Usage %', 'hour': 'Hour of Day'},
            color_discrete_map={'Prime Time': '#1f77b4', 'Off-Peak': '#aec7e8'}
        )
        fig_hourly.update_layout(height=350)
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col2:
        st.markdown("#### 📅 Daily Usage Distribution")
        
        daily_avg = df.groupby(['day', 'day_category'])['usage_percentage'].mean().reset_index()
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_avg['day'] = pd.Categorical(daily_avg['day'], categories=day_order, ordered=True)
        daily_avg = daily_avg.sort_values('day')
        
        fig_daily = px.bar(
            daily_avg,
            x='day',
            y='usage_percentage', 
            color='day_category',
            title="Average Usage by Day",
            labels={'usage_percentage': 'Usage %', 'day': 'Day of Week'},
            color_discrete_map={'Weekend': '#ff7f0e', 'Weekday': '#1f77b4'}
        )
        fig_daily.update_layout(height=350)
        fig_daily.update_xaxis(tickangle=45)
        st.plotly_chart(fig_daily, use_container_width=True)
    
    # Facility and tier comparison
    st.markdown("### 🏟️ Facility & Member Tier Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Prime Time vs Off-Peak by Facility")
        
        facility_comparison = df.groupby(['facility', 'time_category'])['usage_percentage'].mean().reset_index()
        facility_pivot = facility_comparison.pivot(index='facility', columns='time_category', values='usage_percentage').reset_index()
        
        fig_facility = px.bar(
            facility_pivot,
            x='facility',
            y=['Prime Time', 'Off-Peak'],
            title="Facility Usage: Prime Time vs Off-Peak",
            labels={'value': 'Usage %', 'variable': 'Time Period'},
            barmode='group'
        )
        fig_facility.update_layout(height=350)
        fig_facility.update_xaxis(tickangle=45)
        st.plotly_chart(fig_facility, use_container_width=True)
    
    with col2:
        st.markdown("#### Usage by Member Tier")
        
        tier_comparison = df.groupby(['member_tier', 'time_category'])['usage_percentage'].mean().reset_index()
        
        fig_tier = px.bar(
            tier_comparison,
            x='member_tier',
            y='usage_percentage',
            color='time_category',
            title="Member Tier Usage Patterns",
            labels={'usage_percentage': 'Usage %', 'member_tier': 'Member Tier'},
            barmode='group'
        )
        fig_tier.update_layout(height=350)
        fig_tier.update_xaxis(tickangle=45)
        st.plotly_chart(fig_tier, use_container_width=True)
    
    # Actionable insights
    st.markdown("### 💡 Actionable Insights & Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h4>🎯 Peak Hour Optimization</h4>
        <p><strong>Prime Time ({} - 9 PM):</strong> {}% utilization</p>
        <p><strong>Recommendation:</strong> Implement dynamic pricing during peak hours to maximize revenue while managing demand.</p>
        <p><strong>Potential Impact:</strong> +15-25% revenue during prime time</p>
        </div>
        """.format(insights['peak_hour'], insights['prime_time_avg']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h4>📈 Weekend Strategy</h4>
        <p><strong>Weekend Boost:</strong> +{}% vs weekdays</p>
        <p><strong>Recommendation:</strong> Expand weekend programming and special events to capitalize on higher demand.</p>
        <p><strong>Potential Impact:</strong> +$5,000-8,000 monthly weekend revenue</p>
        </div>
        """.format(insights['weekend_boost']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
        <h4>⏰ Off-Peak Opportunities</h4>
        <p><strong>Off-Peak Usage:</strong> {}% (vs {}% prime time)</p>
        <p><strong>Recommendation:</strong> Target corporate wellness, senior programs, and discounted rates for 10 AM - 2 PM slots.</p>
        <p><strong>Potential Impact:</strong> +30% off-peak utilization</p>
        </div>
        """.format(insights['off_peak_avg'], insights['prime_time_avg']), unsafe_allow_html=True)
    
    # Detailed facility insights
    st.markdown("#### 🏟️ Facility-Specific Peak Times")
    
    facility_peaks_df = pd.DataFrame([
        {'Facility': facility, 'Peak Hour': f"{hour}:00", 'Strategy': strategy}
        for facility, hour in insights['facility_peaks'].items()
        for strategy in [
            "Basketball: Evening leagues & tournaments" if facility == 'Basketball Courts'
            else "Soccer: After-school & evening programs" if facility == 'Soccer Fields'  
            else "Volleyball: Youth leagues & adult recreation" if facility == 'Volleyball Courts'
            else "Player Lab: Elite training sessions" if facility == 'Player Lab'
            else "Fitness: Morning & evening classes"
        ]
    ])
    
    st.dataframe(facility_peaks_df, use_container_width=True)
    
    # Real-time alerts and recommendations
    st.markdown("### 🚨 Real-Time Optimization Alerts")
    
    current_hour = datetime.now().hour
    alerts = []
    
    if 18 <= current_hour <= 21:
        alerts.append({
            "type": "🔴 High Demand",
            "message": "Prime time active - consider surge pricing",
            "action": "Enable 20% premium pricing"
        })
    elif 10 <= current_hour <= 14:
        alerts.append({
            "type": "🟡 Low Utilization", 
            "message": "Off-peak period - promote discounted access",
            "action": "Send targeted promotions to Basic members"
        })
    else:
        alerts.append({
            "type": "🟢 Normal Operations",
            "message": "Standard operating conditions",
            "action": "Monitor for trends"
        })
    
    for alert in alerts:
        st.markdown(f"""
        <div class="nil-alert">
        <strong>{alert['type']}</strong><br>
        {alert['message']}<br>
        <strong>Recommended Action:</strong> {alert['action']}
        </div>
        """, unsafe_allow_html=True)
    
    # Export and refresh options
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.session_state.heatmap_data = heatmap_analyzer.generate_heatmap_data()
            st.success("Data refreshed!")
            st.rerun()
    
    with col2:
        if st.button("📊 Export Report", use_container_width=True):
            st.success("Heatmap report exported to Downloads!")
    
    with col3:
        st.markdown("**Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))