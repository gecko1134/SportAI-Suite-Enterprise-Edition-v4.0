                with col1:
                    current_moisture = random.uniform(30, 70)
                    st.metric("Current Moisture", f"{current_moisture:.1f}%")
                    
                    soil_temp = random.uniform(55, 75)
                    st.metric("Soil Temperature", f"{soil_temp:.1f}°F")
                
                with col2:
                    last_watering = datetime.now() - timedelta(hours=random.randint(6, 48))
                    st.metric("Last Watering", last_watering.strftime('%m/%d %I:%M %p'))
                    
                    duration = random.randint(15, 45)
                    st.metric("Last Duration", f"{duration} min")
                
                with col3:
                    pressure = random.uniform(25, 40)
                    st.metric("Water Pressure", f"{pressure:.1f} PSI")
                    
                    flow_rate = random.uniform(8, 15)
                    st.metric("Flow Rate", f"{flow_rate:.1f} GPM")
                
                # Zone controls
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    if st.button(f"💧 Start Irrigation", key=f"start_irrigation_{i}"):
                        st.success(f"Irrigation started for {zone_id}")
                
                with col_b:
                    if st.button(f"⏹️ Stop Irrigation", key=f"stop_irrigation_{i}"):
                        st.success(f"Irrigation stopped for {zone_id}")
                
                with col_c:
                    if st.button(f"📅 Schedule", key=f"schedule_irrigation_{i}"):
                        st.success(f"Scheduling interface opened for {zone_id}")
                
                with col_d:
                    if st.button(f"🔧 Maintenance", key=f"maintenance_irrigation_{i}"):
                        st.success(f"Maintenance mode activated for {zone_id}")
        
        # Weather integration
        st.markdown("### 🌤️ Weather Integration")
        
        with st.expander("Weather-Based Irrigation Adjustments"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Current Weather:**")
                st.markdown(f"🌡️ **Temperature:** {random.randint(60, 85)}°F")
                st.markdown(f"💧 **Humidity:** {random.randint(40, 80)}%")
                st.markdown(f"🌧️ **Precipitation:** {random.uniform(0, 0.5):.2f} inches")
                st.markdown(f"💨 **Wind Speed:** {random.randint(3, 15)} mph")
            
            with col2:
                st.markdown("**7-Day Forecast Impact:**")
                
                forecast_data = []
                for i in range(7):
                    date = datetime.now() + timedelta(days=i)
                    rain_chance = random.randint(0, 100)
                    irrigation_adjustment = "Normal" if rain_chance < 30 else "Reduced" if rain_chance < 70 else "Skip"
                    
                    forecast_data.append({
                        'Date': date.strftime('%m/%d'),
                        'Rain Chance': f"{rain_chance}%",
                        'Irrigation': irrigation_adjustment
                    })
                
                forecast_df = pd.DataFrame(forecast_data)
                st.dataframe(forecast_df, use_container_width=True)

# =============================================================================
# BOARD OF DIRECTORS MODULE
# =============================================================================

class BoardManager:
    """Board of Directors management system"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def get_board_members(self) -> List[Dict]:
        """Get all board members"""
        return self.data_manager.get_data("board_members")
    
    def show_board_interface(self):
        """Display board of directors interface"""
        st.markdown("## 🏛️ Board of Directors Portal")
        st.markdown('<span class="ai-badge">GOVERNANCE MANAGEMENT</span>', unsafe_allow_html=True)
        
        # Board overview
        board_members = self.get_board_members()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Board Members", len(board_members))
        with col2:
            positions_filled = len(set(member['position'] for member in board_members))
            st.metric("Positions Filled", positions_filled)
        with col3:
            next_meeting = datetime.now() + timedelta(days=random.randint(7, 21))
            st.metric("Next Meeting", next_meeting.strftime('%m/%d'))
        with col4:
            avg_tenure = sum((datetime.now().year - int(member['tenure'].split('-')[0])) for member in board_members) / len(board_members) if board_members else 0
            st.metric("Avg Tenure", f"{avg_tenure:.1f} years")
        
        # Board management tabs
        tab1, tab2, tab3, tab4 = st.tabs(["👥 Board Members", "📅 Meetings", "📋 Governance", "📊 Reports"])
        
        with tab1:
            self._show_board_members()
        
        with tab2:
            self._show_board_meetings()
        
        with tab3:
            self._show_governance_documents()
        
        with tab4:
            self._show_board_reports()
    
    def _show_board_members(self):
        """Display board member profiles"""
        board_members = self.get_board_members()
        
        st.markdown("### 👥 Board Member Profiles")
        
        for member in board_members:
            with st.expander(f"🏛️ {member['name']} - {member['position']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="board-card">
                        <h4>{member['name']}</h4>
                        <p><strong>Position:</strong> {member['position']}</p>
                        <p><strong>Tenure:</strong> {member['tenure']}</p>
                        <p><strong>Expertise:</strong> {member['expertise']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    **Contact Information:**  
                    📧 **Email:** {member['email']}  
                    📞 **Phone:** {member['phone']}  
                    
                    **Board Contributions:**  
                    • Meeting Attendance: {random.randint(85, 100)}%  
                    • Committee Participation: {random.randint(2, 5)} committees  
                    • Years of Service: {datetime.now().year - int(member['tenure'].split('-')[0])}
                    """)
                
                # Member actions
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button(f"📧 Contact", key=f"contact_board_{member['id']}"):
                        st.success(f"Email sent to {member['name']}")
                
                with col_b:
                    if st.button(f"📄 Profile", key=f"profile_board_{member['id']}"):
                        st.success(f"Detailed profile opened for {member['name']}")
                
                with col_c:
                    if st.button(f"✏️ Edit", key=f"edit_board_{member['id']}"):
                        st.session_state[f"edit_board_{member['id']}"] = True
        
        # Add new board member
        with st.expander("➕ Add New Board Member"):
            with st.form("add_board_member_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Full Name *")
                    position = st.selectbox("Position", 
                                          ["Chairman", "Vice Chairman", "Treasurer", "Secretary", "Board Member"])
                    expertise = st.selectbox("Area of Expertise", 
                                           ["Finance", "Operations", "Legal", "Marketing", "Technology", "Community Relations"])
                
                with col2:
                    email = st.text_input("Email Address *")
                    phone = st.text_input("Phone Number")
                    start_year = st.number_input("Start Year", min_value=2020, max_value=2030, value=2024)
                    end_year = st.number_input("Term End Year", min_value=2024, max_value=2035, value=2030)
                
                bio = st.text_area("Biography", placeholder="Brief background and qualifications...")
                
                if st.form_submit_button("➕ Add Board Member"):
                    if name and position and email:
                        new_member = {
                            "name": name,
                            "position": position,
                            "tenure": f"{start_year}-{end_year}",
                            "email": email,
                            "phone": phone,
                            "expertise": expertise,
                            "bio": bio,
                            "added_date": datetime.now().strftime('%Y-%m-%d')
                        }
                        
                        if self.data_manager.add_record("board_members", new_member):
                            st.success(f"✅ Added board member: {name}")
                            st.rerun()
                    else:
                        st.error("❌ Please fill in required fields")
    
    def _show_board_meetings(self):
        """Display board meeting management"""
        st.markdown("### 📅 Board Meeting Management")
        
        # Upcoming meetings
        st.markdown("#### 📋 Upcoming Meetings")
        
        upcoming_meetings = [
            {
                "date": "2024-03-15",
                "time": "10:00 AM",
                "type": "Regular Board Meeting",
                "location": "Conference Room A",
                "status": "Scheduled"
            },
            {
                "date": "2024-04-12", 
                "time": "2:00 PM",
                "type": "Finance Committee",
                "location": "Virtual",
                "status": "Scheduled"
            },
            {
                "date": "2024-05-10",
                "time": "10:00 AM",
                "type": "Strategic Planning Session",
                "location": "Conference Room A",
                "status": "Draft"
            }
        ]
        
        for meeting in upcoming_meetings:
            status_color = {"Scheduled": "🟢", "Draft": "🟡", "Cancelled": "🔴"}
            
            with st.expander(f"{status_color.get(meeting['status'], '⚪')} {meeting['type']} - {meeting['date']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Date:** {meeting['date']}  
                    **Time:** {meeting['time']}  
                    **Type:** {meeting['type']}  
                    **Location:** {meeting['location']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Status:** {meeting['status']}  
                    **Expected Attendees:** {random.randint(4, 8)}  
                    **Agenda Items:** {random.randint(5, 12)}  
                    **Materials:** {random.randint(2, 6)} documents
                    """)
                
                # Meeting actions
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    if st.button(f"📄 Agenda", key=f"agenda_{meeting['date']}"):
                        st.success("Meeting agenda opened")
                
                with col_b:
                    if st.button(f"📧 Send Invites", key=f"invites_{meeting['date']}"):
                        st.success("Meeting invitations sent")
                
                with col_c:
                    if st.button(f"📝 Minutes", key=f"minutes_{meeting['date']}"):
                        st.success("Meeting minutes template opened")
                
                with col_d:
                    if st.button(f"📊 Materials", key=f"materials_{meeting['date']}"):
                        st.success("Meeting materials accessed")
        
        # Meeting history
        st.markdown("#### 📚 Recent Meeting History")
        
        past_meetings = [
            {"date": "2024-02-09", "type": "Regular Board Meeting", "attendance": "7/8", "duration": "2.5 hrs"},
            {"date": "2024-01-12", "type": "Budget Review", "attendance": "6/8", "duration": "3.0 hrs"},
            {"date": "2023-12-08", "type": "Year-End Review", "attendance": "8/8", "duration": "4.0 hrs"}
        ]
        
        for meeting in past_meetings:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f"**{meeting['date']}**")
            with col2:
                st.markdown(meeting['type'])
            with col3:
                st.markdown(meeting['attendance'])
            with col4:
                st.markdown(meeting['duration'])
            with col5:
                if st.button(f"📄 View", key=f"view_{meeting['date']}"):
                    st.success("Meeting details opened")
    
    def _show_governance_documents(self):
        """Display governance documents and policies"""
        st.markdown("### 📋 Governance Documents")
        
        # Document categories
        governance_docs = {
            "📜 Founding Documents": [
                "Articles of Incorporation",
                "Corporate Bylaws", 
                "Operating Agreement",
                "Board Charter"
            ],
            "📋 Policies & Procedures": [
                "Code of Ethics",
                "Conflict of Interest Policy",
                "Whistleblower Policy",
                "Document Retention Policy"
            ],
            "📊 Financial Governance": [
                "Annual Budget",
                "Financial Oversight Policy",
                "Investment Policy",
                "Audit Committee Charter"
            ],
            "🏛️ Board Operations": [
                "Board Meeting Procedures",
                "Committee Charters",
                "Director Orientation Manual",
                "Performance Evaluation Process"
            ]
        }
        
        for category, documents in governance_docs.items():
            with st.expander(category):
                for doc in documents:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"📄 **{doc}**")
                    
                    with col2:
                        last_updated = datetime.now() - timedelta(days=random.randint(30, 365))
                        st.markdown(f"*Updated: {last_updated.strftime('%m/%d/%Y')}*")
                    
                    with col3:
                        if st.button(f"📖 View", key=f"view_doc_{doc.replace(' ', '_')}"):
                            st.success(f"Opened {doc}")
        
        # Document management
        st.markdown("#### 📁 Document Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Quick Actions:**")
            if st.button("➕ Upload New Document"):
                st.success("Document upload interface opened")
            if st.button("📋 Create Policy Template"):
                st.success("Policy template creator opened")
            if st.button("🔍 Search Documents"):
                st.success("Document search interface opened")
        
        with col2:
            st.markdown("**Document Status:**")
            st.markdown("✅ All governance documents current")
            st.markdown("📅 Next policy review: March 2024")
            st.markdown("🔒 Access controls: Implemented")
    
    def _show_board_reports(self):
        """Display board reports and analytics"""
        st.markdown("### 📊 Board Reports & Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            meeting_attendance = random.uniform(85, 98)
            st.metric("Avg Meeting Attendance", f"{meeting_attendance:.1f}%")
        
        with col2:
            decisions_made = random.randint(25, 45)
            st.metric("Decisions This Year", decisions_made)
        
        with col3:
            committees_active = random.randint(4, 8)
            st.metric("Active Committees", committees_active)
        
        with col4:
            governance_score = random.uniform(88, 96)
            st.metric("Governance Score", f"{governance_score:.1f}/100")
        
        # Board performance analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Meeting Attendance Trends")
            
            # Generate attendance data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            attendance_data = []
            
            for month in months:
                for member in self.get_board_members():
                    attendance = random.uniform(0.8, 1.0)
                    attendance_data.append({
                        'Month': month,
                        'Member': member['name'],
                        'Attendance': attendance
                    })
            
            attendance_df = pd.DataFrame(attendance_data)
            
            if PLOTLY_AVAILABLE:
                fig = px.line(attendance_df, x='Month', y='Attendance', color='Member',
                            title="Board Member Attendance Trends")
                st.plotly_chart(fig, use_container_width=True)
            else:
                pivot_attendance = attendance_df.pivot_table(index='Month', columns='Member', values='Attendance')
                st.line_chart(pivot_attendance)
        
        with col2:
            st.markdown("#### 💼 Committee Participation")
            
            committee_data = {
                'Committee': ['Finance', 'Governance', 'Strategic Planning', 'Audit', 'Nominating'],
                'Members': [4, 3, 5, 3, 4],
                'Meetings/Year': [12, 6, 4, 4, 2]
            }
            
            committee_df = pd.DataFrame(committee_data)
            
            if PLOTLY_AVAILABLE:
                fig = px.bar(committee_df, x='Committee', y='Members',
                           title="Committee Membership Distribution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart(committee_df.set_index('Committee')['Members'])
        
        # Governance insights
        st.markdown("#### 🎯 Governance Insights")
        
        insights = [
            "📊 **Board Effectiveness:** Above industry average (92%)",
            "👥 **Diversity Index:** Good representation across expertise areas",
            "⏰ **Meeting Efficiency:** Average 2.5 hours per meeting",
            "📋 **Decision Quality:** 96% of decisions implemented successfully",
            "🔄 **Committee Function:** All committees meeting quarterly minimums",
            "📈 **Strategic Alignment:** 89% of initiatives aligned with strategic plan"
        ]
        
        for insight in insights:
            st.markdown(insight)

# =============================================================================
# REFEREE MANAGEMENT MODULE
# =============================================================================

class RefereeManager:
    """Comprehensive referee management system"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def get_referees(self) -> List[Dict]:
        """Get all referees"""
        return self.data_manager.get_data("referees")
    
    def show_referee_interface(self):
        """Display referee management interface"""
        st.markdown("## 🏃‍♂️ Referee Management System")
        st.markdown('<span class="ai-badge">OFFICIAL COORDINATION</span>', unsafe_allow_html=True)
        
        # Referee overview
        referees = self.get_referees()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Referees", len(referees))
        with col2:
            available_refs = len([r for r in referees if r['availability'] == 'Available'])
            st.metric("Available Today", available_refs)
        with col3:
            avg_rate = sum(r['rate'] for r in referees) / len(referees) if referees else 0
            st.metric("Avg Rate", f"${avg_rate:.0f}")
        with col4:
            professional_refs = len([r for r in referees if r['level'] == 'Professional'])
            st.metric("Professional Level", professional_refs)
        
        # Referee management tabs
        tab1, tab2, tab3, tab4 = st.tabs(["👨‍🏫 Referee List", "➕ Add Referee", "📅 Scheduling", "📊 Performance"])
        
        with tab1:
            self._show_referee_list()
        
        with tab2:
            self._show_add_referee_form()
        
        with tab3:
            self._show_referee_scheduling()
        
        with tab4:
            self._show_referee_performance()
    
    def _show_referee_list(self):
        """Display list of all referees"""
        referees = self.get_referees()
        
        for referee in referees:
            availability_color = {"Available": "🟢", "Busy": "🔴", "Unavailable": "🟡"}
            level_color = {"Professional": "🥇", "Semi-Professional": "🥈", "Amateur": "🥉"}
            
            with st.expander(f"{availability_color.get(referee['availability'], '⚪')} {referee['name']} - {referee['level']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="referee-card">
                        <h4>{referee['name']}</h4>
                        <p><strong>Level:</strong> {level_color.get(referee['level'], '')} {referee['level']}</p>
                        <p><strong>Rate:</strong> ${referee['rate']}/game</p>
                        <p><strong>Phone:</strong> {referee['phone']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    **Sports Certified:**  
                    {', '.join(referee['sports'])}
                    
                    **Availability:**  
                    {availability_color.get(referee['availability'], '⚪')} {referee['availability']}
                    
                    **Games This Month:**  
                    {random.randint(8, 25)}
                    """)
                
                with col3:
                    # Performance metrics
                    rating = random.uniform(4.2, 4.9)
                    experience_years = random.randint(2, 15)
                    
                    st.markdown(f"""
                    **Performance Rating:** ⭐ {rating:.1f}/5.0  
                    **Experience:** {experience_years} years  
                    **Certifications:** {random.randint(2, 5)} active  
                    **Last Game:** {(datetime.now() - timedelta(days=random.randint(1, 7))).strftime('%m/%d')}
                    """)
                
                # Action buttons
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    if st.button(f"📅 Assign Game", key=f"assign_ref_{referee['id']}"):
                        st.success(f"Game assignment interface opened for {referee['name']}")
                
                with col_b:
                    if st.button(f"📞 Contact", key=f"contact_ref_{referee['id']}"):
                        st.success(f"Called {referee['name']} at {referee['phone']}")
                
                with col_c:
                    if st.button(f"📊 Performance", key=f"performance_ref_{referee['id']}"):
                        st.success(f"Performance report opened for {referee['name']}")
                
                with col_d:
                    if st.button(f"✏️ Edit", key=f"edit_ref_{referee['id']}"):
                        st.session_state[f"edit_ref_{referee['id']}"] = True
                
                # Edit form
                if st.session_state.get(f"edit_ref_{referee['id']}", False):
                    with st.form(f"edit_referee_form_{referee['id']}"):
                        st.markdown("### Edit Referee Details")
                        
                        col_edit1, col_edit2 = st.columns(2)
                        
                        with col_edit1:
                            new_name = st.text_input("Name", value=referee['name'])
                            new_sports = st.multiselect("Sports", 
                                                       ["Basketball", "Soccer", "Football", "Volleyball", "Tennis"],
                                                       default=referee['sports'])
                            new_level = st.selectbox("Level", 
                                                    ["Amateur", "Semi-Professional", "Professional"],
                                                    index=["Amateur", "Semi-Professional", "Professional"].index(referee['level']))
                        
                        with col_edit2:
                            new_rate = st.number_input("Rate per Game ($)", value=referee['rate'], min_value=0)
                            new_availability = st.selectbox("Availability", 
                                                          ["Available", "Busy", "Unavailable"],
                                                          index=["Available", "Busy", "Unavailable"].index(referee['availability']))
                            new_phone = st.text_input("Phone", value=referee['phone'])
                        
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                updates = {
                                    "name": new_name,
                                    "sports": new_sports,
                                    "level": new_level,
                                    "rate": new_rate,
                                    "availability": new_availability,
                                    "phone": new_phone
                                }
                                
                                if self.data_manager.update_record("referees", referee['id'], updates):
                                    st.success("Referee updated successfully!")
                                    st.session_state[f"edit_ref_{referee['id']}"] = False
                                    st.rerun()
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"edit_ref_{referee['id']}"] = False
                                st.rerun()
    
    def _show_add_referee_form(self):
        """Display form to add new referee"""
        with st.form("add_referee_form"):
            st.markdown("### Add New Referee")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *", placeholder="John Doe")
                sports = st.multiselect("Sports Certified *", 
                                      ["Basketball", "Soccer", "Football", "Volleyball", "Tennis", "Baseball"])
                level = st.selectbox("Experience Level *", 
                                   ["Amateur", "Semi-Professional", "Professional"])
                rate = st.number_input("Rate per Game ($) *", min_value=0, value=100)
            
            with col2:
                phone = st.text_input("Phone Number *", placeholder="(555) 123-4567")
                email = st.text_input("Email Address", placeholder="referee@email.com")
                availability = st.selectbox("Current Availability", 
                                          ["Available", "Busy", "Unavailable"], index=0)
                certifications = st.text_area("Certifications", 
                                             placeholder="List relevant certifications...")
            
            experience = st.slider("Years of Experience", 0, 25, 5)
            
            if st.form_submit_button("➕ Add Referee"):
                if name and sports and level and rate and phone:
                    new_referee = {
                        "name": name,
                        "sports": sports,
                        "level": level,
                        "rate": rate,
                        "availability": availability,
                        "phone": phone,
                        "email": email,
                        "experience_years": experience,
                        "certifications": certifications,
                        "added_date": datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    if self.data_manager.add_record("referees", new_referee):
                        st.success(f"✅ Added new referee: {name}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add referee")
                else:
                    st.error("❌ Please fill in all required fields")
    
    def _show_referee_scheduling(self):
        """Display referee scheduling system"""
        st.markdown("### 📅 Referee Scheduling")
        
        # Quick assignment
        st.markdown("#### ⚡ Quick Game Assignment")
        
        with st.form("quick_assignment_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                game_date = st.date_input("Game Date", value=datetime.now().date() + timedelta(days=7))
                game_time = st.time_input("Game Time", value=datetime.now().time())
                sport = st.selectbox("Sport", ["Basketball", "Soccer", "Football", "Volleyball", "Tennis"])
            
            with col2:
                level_required = st.selectbox("Level Required", ["Amateur", "Semi-Professional", "Professional"])
                num_referees = st.number_input("Number of Referees", min_value=1, max_value=4, value=2)
                location = st.text_input("Location", placeholder="Court/Field Name")
            
            with col3:
                # Show available referees for the sport
                available_refs = [r for r in self.get_referees() 
                                if sport in r['sports'] and r['availability'] == 'Available']
                
                if available_refs:
                    selected_refs = st.multiselect("Select Referees", 
                                                  [f"{r['name']} (${r['rate']})" for r in available_refs])
                else:
                    st.warning("No available referees for this sport")
                    selected_refs = []
            
            if st.form_submit_button("📋 Assign Referees"):
                if selected_refs and game_date and location:
                    st.success(f"✅ Assigned {len(selected_refs)} referee(s) for {sport} on {game_date}")
                    
                    # Show assignment summary
                    st.markdown("**Assignment Summary:**")
                    total_cost = len(selected_refs) * 100  # Estimate
                    st.markdown(f"• **Game:** {sport} at {location}")
                    st.markdown(f"• **Date/Time:** {game_date} at {game_time}")
                    st.markdown(f"• **Referees:** {', '.join(selected_refs)}")
                    st.markdown(f"• **Total Cost:** ${total_cost}")
                else:
                    st.error("❌ Please fill in all required fields")
        
        # Upcoming assignments
        st.markdown("#### 📋 Upcoming Assignments")
        
        # Generate sample assignments
        upcoming_assignments = []
        for i in range(5):
            date = datetime.now() + timedelta(days=random.randint(1, 14))
            ref = random.choice(self.get_referees())
            sport = random.choice(ref['sports'])
            
            upcoming_assignments.append({
                "date": date.strftime('%Y-%m-%d'),
                "time": f"{random.randint(14, 20):02d}:{random.choice(['00', '30'])}",
                "sport": sport,
                "referee": ref['name'],
                "location": f"{sport} Court {random.randint(1, 4)}",
                "rate": ref['rate'],
                "status": random.choice(["Confirmed", "Pending", "Tentative"])
            })
        
        for assignment in upcoming_assignments:
            status_color = {"Confirmed": "🟢", "Pending": "🟡", "Tentative": "🔵"}
            
            with st.expander(f"{status_color[assignment['status']]} {assignment['sport']} - {assignment['date']} {assignment['time']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Sport:** {assignment['sport']}  
                    **Date:** {assignment['date']}  
                    **Time:** {assignment['time']}  
                    **Location:** {assignment['location']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Referee:** {assignment['referee']}  
                    **Rate:** ${assignment['rate']}  
                    **Status:** {assignment['status']}  
                    **Confirmation:** {status_color[assignment['status']]} {assignment['status']}
                    """)
                
                # Assignment actions
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button(f"✅ Confirm", key=f"confirm_{i}"):
                        st.success("Assignment confirmed")
                
                with col_b:
                    if st.button(f"📧 Notify", key=f"notify_{i}"):
                        st.success(f"Notification sent to {assignment['referee']}")
                
                with col_c:
                    if st.button(f"❌ Cancel", key=f"cancel_{i}"):
                        st.success("Assignment cancelled")
    
    def _show_referee_performance(self):
        """Display referee performance analytics"""
        st.markdown("### 📊 Referee Performance Analytics")
        
        referees = self.get_referees()
        
        if not referees:
            st.info("No referee data available")
            return
        
        # Performance overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_rating = random.uniform(4.3, 4.8)
            st.metric("Avg Performance Rating", f"{avg_rating:.1f}/5.0")
        
        with col2:
            total_games = random.randint(150, 300)
            st.metric("Total Games This Month", total_games)
        
        with col3:
            on_time_rate = random.uniform(92, 98)
            st.metric("On-Time Arrival Rate", f"{on_time_rate:.1f}%")
        
        with col4:
            complaint_rate = random.uniform(1, 5)
            st.metric("Complaint Rate", f"{complaint_rate:.1f}%")
        
        # Individual performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⭐ Top Performers")
            
            # Generate performance data
            performance_data = []
            for ref in referees:
                rating = random.uniform(4.0, 5.0)
                games = random.randint(8, 25)
                performance_data.append({
                    'Referee': ref['name'],
                    'Rating': rating,
                    'Games': games,
                    'Level': ref['level']
                })
            
            # Sort by rating
            performance_data.sort(key=lambda x: x['Rating'], reverse=True)
            
            for i, perf in enumerate(performance_data[:5]):
                rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
                st.markdown(f"{rank_emoji} **{perf['Referee']}** - ⭐ {perf['Rating']:.1f} ({perf['Games']} games)")
        
        with col2:
            st.markdown("#### 📈 Performance Trends")
            
            if PLOTLY_AVAILABLE:
                # Create performance trend chart
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                trend_data = []
                
                for month in months:
                    avg_rating = random.uniform(4.2, 4.7)
                    games_count = random.randint(40, 80)
                    trend_data.append({
                        'Month': month,
                        'Avg Rating': avg_rating,
                        'Games Count': games_count
                    })
                
                trend_df = pd.DataFrame(trend_data)
                
                fig = px.line(trend_df, x='Month', y='Avg Rating',
                            title="Monthly Average Referee Ratings")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("Performance trend data available in enhanced mode")
        
        # Detailed referee performance
        st.markdown("#### 📋 Individual Performance Reports")
        
        for ref in referees:
            with st.expander(f"📊 {ref['name']} Performance Report"):
                # Generate detailed metrics
                rating = random.uniform(4.0, 5.0)
                games_this_month = random.randint(8, 25)
                on_time_rate = random.uniform(90, 100)
                complaints = random.randint(0, 3)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Overall Rating", f"⭐ {rating:.1f}/5.0")
                
                with col2:
                    st.metric("Games This Month", games_this_month)
                
                with col3:
                    st.metric("On-Time Rate", f"{on_time_rate:.1f}%")
                
                with col4:
                    st.metric("Complaints", complaints)
                
                # Recent feedback
                st.markdown("**Recent Feedback:**")
                
                feedback_items = [
                    "Excellent game management and communication",
                    "Professional demeanor throughout the match",
                    "Quick and accurate decision making",
                    "Good rapport with players and coaches"
                ]
                
                for feedback in random.sample(feedback_items, 2):
                    st.markdown(f"• {feedback}")
                
                # Action buttons
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button(f"📧 Send Feedback", key=f"feedback_{ref['id']}"):
                        st.success(f"Feedback form sent to {ref['name']}")
                
                with col_b:
                    if st.button(f"🎓 Training", key=f"training_{ref['id']}"):
                        st.success(f"Training recommendations generated for {ref['name']}")
                
                with col_c:
                    if st.button(f"📈 Detailed Report", key=f"detailed_{ref['id']}"):
                        st.success(f"Detailed performance report generated for {ref['name']}")

# =============================================================================
# DATA MANAGEMENT INTERFACE
# =============================================================================

def show_data_management_interface(data_manager: DataManager):
    """Display comprehensive data management interface"""
    st.markdown("## 🗄️ Data Management Center")
    st.markdown('<span class="ai-badge">CRUD OPERATIONS</span>', unsafe_allow_html=True)
    
    # Data overview
    collections = list(data_manager.data_store.keys())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Data Collections", len(collections))
    with col2:
        total_records = sum(len(data_manager.get_data(col)) for col in collections)
        st.metric("Total Records", total_records)
    with col3:
        largest_collection = max(collections, key=lambda x: len(data_manager.get_data(x)))
        st.metric("Largest Collection", largest_collection.replace('_', ' ').title())
    with col4:
        backup_status = "✅ Current"
        st.metric("Backup Status", backup_status)
    
    # Data management tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "🔍 Browse Data", "✏️ Edit Data", "⚙️ Admin Tools"])
    
    with tab1:
        _show_data_overview(data_manager)
    
    with tab2:
        _show_browse_data(data_manager)
    
    with tab3:
        _show_edit_data(data_manager)
    
    with tab4:
        _show_admin_tools(data_manager)

def _show_data_overview(data_manager: DataManager):
    """Show data overview and statistics"""
    st.markdown("### 📊 Data Collection Overview")
    
    collections = list(data_manager.data_store.keys())
    
    for collection in collections:
        data = data_manager.get_data(collection)
        
        with st.expander(f"📋 {collection.replace('_', ' ').title()} ({len(data)} records)"):
            if data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Sample Record:**")
                    sample_record = data[0]
                    for key, value in list(sample_record.items())[:5]:
                        st.markdown(f"• **{key}:** {value}")
                    
                    if len(sample_record) > 5:
                        st.markdown(f"• ... and {len(sample_record) - 5} more fields")
                
                with col2:
                    st.markdown("**Collection Stats:**")
                    st.markdown(f"• **Total Records:** {len(data)}")
                    st.markdown(f"• **Fields per Record:** {len(sample_record)}")
                    
                    # Try to find date fields for recency info
                    date_fields = [k for k in sample_record.keys() if 'date' in k.lower()]
                    if date_fields:
                        st.markdown(f"• **Date Fields:** {', '.join(date_fields)}")
            else:
                st.info("No records in this collection")

def _show_browse_data(data_manager: DataManager):
    """Show data browsing interface"""
    st.markdown("### 🔍 Browse and Search Data")
    
    # Collection selector
    collections = list(data_manager.data_store.keys())
    selected_collection = st.selectbox("Select Data Collection", 
                                     [col.replace('_', ' ').title() for col in collections])
    
    if selected_collection:
        collection_key = selected_collection.lower().replace(' ', '_')
        data = data_manager.get_data(collection_key)
        
        if data:
            # Search functionality
            search_term = st.text_input("🔍 Search", placeholder="Enter search term...")
            
            # Filter data if search term provided
            if search_term:
                filtered_data = []
                for record in data:
                    for value in record.values():
                        if search_term.lower() in str(value).lower():
                            filtered_data.append(record)
                            break
                display_data = filtered_data
                st.info(f"Found {len(filtered_data)} records matching '{search_term}'")
            else:
                display_data = data
            
            # Display data in table format
            if display_data:
                df = pd.DataFrame(display_data)
                st.dataframe(df, use_container_width=True)
                
                # Export options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📥 Export CSV"):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"{collection_key}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("📊 Generate Report"):
                        st.success("Report generation started")
                
                with col3:
                    if st.button("🔄 Refresh Data"):
                        st.rerun()
            else:
                st.info("No records found")
        else:
            st.info(f"No data in {selected_collection} collection")

def _show_edit_data(data_manager: DataManager):
    """Show data editing interface"""
    st.markdown("### ✏️ Edit Data Records")
    
    # Collection selector
    collections = list(data_manager.data_store.keys())
    selected_collection = st.selectbox("Select Collection to Edit", 
                                     [col.replace('_', ' ').title() for col in collections],
                                     key="edit_collection")
    
    if selected_collection:
        collection_key = selected_collection.lower().replace(' ', '_')
        data = data_manager.get_data(collection_key)
        
        if data:
            # Record selector
            record_options = [f"{record.get('id', 'No ID')} - {record.get('name', list(record.values())[0])}" 
                            for record in data]
            selected_record_display = st.selectbox("Select Record to Edit", record_options)
            
            if selected_record_display:
                # Find the actual record
                record_id = selected_record_display.split(' - ')[0]
                selected_record = next((r for r in data if r.get('id') == record_id), None)
                
                if selected_record:
                    st.markdown(f"#### Editing Record: {record_id}")
                    
                    # Create edit form
                    with st.form(f"edit_record_{record_id}"):
                        updated_record = {}
                        
                        # Create input fields for each field in the record
                        for key, value in selected_record.items():
                            if key == 'id':
                                st.text_input(f"{key.title()}", value=value, disabled=True)
                                updated_record[key] = value
                            elif isinstance(value, bool):
                                updated_record[key] = st.checkbox(f"{key.replace('_', ' ').title()}", value=value)
                            elif isinstance(value, (int, float)):
                                updated_record[key] = st.number_input(f"{key.replace('_', ' ').title()}", value=value)
                            elif isinstance(value, list):
                                # Handle lists as multiselect or text area
                                if all(isinstance(item, str) for item in value):
                                    updated_record[key] = st.multiselect(f"{key.replace('_', ' ').title()}", 
                                                                       options=value + ["Add New Option"],
                                                                       default=value)
                                else:
                                    updated_record[key] = st.text_area(f"{key.replace('_', ' ').title()}", 
                                                                     value=str(value))
                            else:
                                updated_record[key] = st.text_input(f"{key.replace('_', ' ').title()}", value=str(value))
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.form_submit_button("💾 Save Changes"):
                                if data_manager.update_record(collection_key, record_id, updated_record):
                                    st.success("✅ Record updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update record")
                        
                        with col2:
                            if st.form_submit_button("🗑️ Delete Record"):
                                if data_manager.delete_record(collection_key, record_id):
                                    st.success("✅ Record deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete record")
                        
                        with col3:
                            if st.form_submit_button("❌ Cancel"):
                                st.info("Changes cancelled")
        else:
            st.info(f"No data in {selected_collection} collection")

def _show_admin_tools(data_manager: DataManager):
    """Show administrative tools"""
    st.markdown("### ⚙️ Administrative Tools")
    
    # Database operations
    st.markdown("#### 🗄️ Database Operations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Backup Data"):
            # Simulate backup
            backup_data = json.dumps(data_manager.data_store, indent=2)
            st.download_button(
                label="Download Backup",
                data=backup_data,
                file_name=f"nxs_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            st.success("✅ Backup created successfully!")
    
    with col2:
        uploaded_file = st.file_uploader("📤 Restore from Backup", type=['json'])
        if uploaded_file is not None:
            try:
                backup_data = json.load(uploaded_file)
                data_manager.data_store = backup_data
                st.success("✅ Data restored successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to restore backup: {e}")
    
    with col3:
        if st.button("🔄 Reset to Defaults"):
            if st.checkbox("⚠️ I understand this will delete all data"):
                data_manager.data_store = data_manager._initialize_data_store()
                st.success("✅ Data reset to defaults!")
                st.rerun()
    
    # Data integrity tools
    st.markdown("#### 🔍 Data Integrity Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Check Data Integrity"):
            issues = []
            
            # Check for missing IDs
            for collection, records in data_manager.data_store.items():
                for record in records:
                    if 'id' not in record:
                        issues.append(f"Missing ID in {collection}")
                    
                    # Check for empty required fields
                    if collection == 'members' and not record.get('name'):
                        issues.append(f"Missing name in members: {record.get('id', 'Unknown')}")
            
            if issues:
                st.warning(f"⚠️ Found {len(issues)} data integrity issues:")
                for issue in issues:
                    st.markdown(f"• {issue}")
            else:
                st.success("✅ No data integrity issues found!")
    
    with col2:
        if st.button("📊 Generate Statistics"):
            stats = {}
            
            for collection, records in data_manager.data_store.items():
                stats[collection] = {
                    "count": len(records),
                    "fields": len(records[0]) if records else 0,
                    "size_estimate": len(str(records))
                }
            
            st.markdown("**Collection Statistics:**")
            stats_df = pd.DataFrame(stats).T
            st.dataframe(stats_df)
    
    # Import/Export tools
    st.markdown("#### 📁 Import/Export Tools")
    
    # Bulk import
    with st.expander("📤 Bulk Import Data"):
        collection_to_import = st.selectbox("Target Collection", 
                                          list(data_manager.data_store.keys()))
        
        uploaded_csv = st.file_uploader("Upload CSV File", type=['csv'])
        
        if uploaded_csv is not None:
            try:
                df = pd.read_csv(uploaded_csv)
                st.markdown("**Preview:**")
                st.dataframe(df.head())
                
                if st.button("📥 Import Data"):
                    records = df.to_dict('records')
                    
                    success_count = 0
                    for record in records:
                        if data_manager.add_record(collection_to_import, record):
                            success_count += 1
                    
                    st.success(f"✅ Imported {success_count}/{len(records)} records")
                    st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error reading CSV: {e}")

# =============================================================================
# MAIN APPLICATION WITH ALL MODULES
# =============================================================================

def main():
    """Enhanced main application with all modules"""
    
    # Initialize data manager
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    
    data_manager = st.session_state.data_manager
    
    # Initialize managers
    sponsorship_manager = SponsorshipManager(data_manager)
    court_manager = CourtManager(data_manager)
    turf_manager = TurfManager(data_manager)
    board_manager = BoardManager(data_manager)
    referee_manager = RefereeManager(data_manager)
    
    # Authentication (simplified for demo)
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown('<div class="main-header"><h1>🏟️ NXS Sports AI Platform - Complete</h1><p>Enterprise Sports Facility Management System</p></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Quick Access Login")
            username = st.text_input("Username", value="admin")
            password = st.text_input("Password", type="password", value="admin123")
            
            if st.button("🚀 Login", use_container_width=True):
                if username == "admin" and password == "admin123":
                    st.session_state.authenticated = True
                    st.success("✅ Welcome to NXS Sports AI Platform!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        return
    
    # Header
    st.markdown('<div class="main-header"><h1>🏟️ NXS Sports AI Platform - Complete System</h1><p>Enterprise Sports Facility Management with All Modules</p></div>', unsafe_allow_html=True)
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()
    
    # Navigation with all modules
    selected_module = st.sidebar.selectbox("🧭 Select Module", [
        "🏠 Dashboard",
        "👥 Membership Management", 
        "🏀 Court Management",
        "⚽ Turf Management",
        "🤝 Sponsorship Management",
        "🏛️ Board of Directors",
        "🏃‍♂️ Referee Management",
        "🏆 Tournament Management",
        "💪 Wellness Center",
        "💼 NIL Management",
        "📱 Smart Systems",
        "💰 Revenue Center",
        "📊 Analytics",
        "🗄️ Data Management"
    ])
    
    # Route to appropriate module
    if selected_module == "🤝 Sponsorship Management":
        sponsorship_manager.show_sponsorship_interface()
    
    elif selected_module == "🏀 Court Management":
        court_manager.show_court_interface()
    
    elif selected_module == "⚽ Turf Management":
        turf_manager.show_turf_interface()
    
    elif selected_module == "🏛️ Board of Directors":
        board_manager.show_board_interface()
    
    elif selected_module == "🏃‍♂️ Referee Management":
        referee_manager.show_referee_interface()
    
    elif selected_module == "🗄️ Data Management":
        show_data_management_interface(data_manager)
    
    else:
        # Placeholder for other modules
        st.markdown(f"## {selected_module}")
        st.info(f"The {selected_module} module is available in the full system. This demo shows the complete data management capabilities with CRUD operations for all facility data.")
        
        # Quick stats for each module
        if selected_module == "🏠 Dashboard":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Members", len(data_manager.get_data("members")))
            with col2:
                st.metric("Active Courts", len(data_manager.get_data("courts")))
            with col3:
                st.metric("Turf Fields", len(data_manager.get_data("turfs")))
            with col4:
                st.metric("Active Sponsors", len([s for s in data_manager.get_data("sponsors") if s.get('status') == 'Active']))
        
        elif selected_module == "👥 Membership Management":
            members = data_manager.get_data("members")
            st.markdown("### 👥 Membership Overview")
            
            for member in members[:3]:  # Show first 3 members
                st.markdown(f"**{member['name']}** - {member['type']} (${member['monthly_fee']}/month)")
            
            if len(members) > 3:
                st.markdown(f"... and {len(members) - 3} more members")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>NXS Sports AI Platform - Complete System</strong> | All Modules Included</p>
        <p>🏟️ Full CRUD Operations | Data Management | Advanced Analytics</p>
        <p>Status: 🟢 All systems operational | Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()        # Court management tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Court List", "➕ Add Court", "📊 Utilization", "🔧 Maintenance"])
        
        with tab1:
            self._show_court_list()
        
        with tab2:
            self._show_add_court_form()
        
        with tab3:
            self._show_court_utilization()
        
        with tab4:
            self._show_court_maintenance()
    
    def _show_court_list(self):
        """Display list of all courts"""
        courts = self.get_courts()
        
        for court in courts:
            condition_color = {"Excellent": "🟢", "Good": "🟡", "Fair": "🟠", "Poor": "🔴"}
            
            with st.expander(f"{condition_color.get(court['condition'], '⚪')} {court['name']} - {court['type']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    **Type:** {court['type']}  
                    **Capacity:** {court['capacity']} people  
                    **Condition:** {court['condition']}  
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Hourly Rate:** ${court['hourly_rate']}  
                    **Last Maintenance:** {court['last_maintenance']}  
                    **Utilization:** {random.randint(60, 95)}%
                    """)
                
                with col3:
                    # Current status simulation
                    current_status = random.choice(["Available", "Occupied", "Maintenance", "Reserved"])
                    status_color = {"Available": "🟢", "Occupied": "🔴", "Maintenance": "🟡", "Reserved": "🔵"}
                    
                    st.markdown(f"""
                    **Current Status:** {status_color[current_status]} {current_status}  
                    **Next Booking:** {(datetime.now() + timedelta(hours=random.randint(1, 8))).strftime('%I:%M %p')}  
                    **Revenue Today:** ${random.randint(200, 800)}
                    """)
                
                # Action buttons
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    if st.button(f"✏️ Edit", key=f"edit_court_{court['id']}"):
                        st.session_state[f"edit_court_{court['id']}"] = True
                
                with col_b:
                    if st.button(f"📅 Schedule", key=f"schedule_court_{court['id']}"):
                        st.success(f"Scheduling interface opened for {court['name']}")
                
                with col_c:
                    if st.button(f"🔧 Maintenance", key=f"maintenance_court_{court['id']}"):
                        st.success(f"Maintenance request created for {court['name']}")
                
                with col_d:
                    if st.button(f"🗑️ Delete", key=f"delete_court_{court['id']}"):
                        if self.data_manager.delete_record("courts", court['id']):
                            st.success(f"Deleted court: {court['name']}")
                            st.rerun()
                
                # Edit form
                if st.session_state.get(f"edit_court_{court['id']}", False):
                    with st.form(f"edit_court_form_{court['id']}"):
                        st.markdown("### Edit Court Details")
                        
                        col_edit1, col_edit2 = st.columns(2)
                        
                        with col_edit1:
                            new_name = st.text_input("Court Name", value=court['name'])
                            new_type = st.selectbox("Court Type", 
                                                   ["Basketball", "Volleyball", "Tennis", "Badminton", "Multi-Purpose"],
                                                   index=["Basketball", "Volleyball", "Tennis", "Badminton", "Multi-Purpose"].index(court['type']) if court['type'] in ["Basketball", "Volleyball", "Tennis", "Badminton", "Multi-Purpose"] else 0)
                            new_capacity = st.number_input("Capacity", value=court['capacity'], min_value=1)
                        
                        with col_edit2:
                            new_rate = st.number_input("Hourly Rate ($)", value=court['hourly_rate'], min_value=0)
                            new_condition = st.selectbox("Condition", 
                                                       ["Excellent", "Good", "Fair", "Poor"],
                                                       index=["Excellent", "Good", "Fair", "Poor"].index(court['condition']))
                            new_maintenance = st.date_input("Last Maintenance", 
                                                          value=datetime.strptime(court['last_maintenance'], '%Y-%m-%d').date())
                        
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                updates = {
                                    "name": new_name,
                                    "type": new_type,
                                    "capacity": new_capacity,
                                    "hourly_rate": new_rate,
                                    "condition": new_condition,
                                    "last_maintenance": new_maintenance.strftime('%Y-%m-%d')
                                }
                                
                                if self.data_manager.update_record("courts", court['id'], updates):
                                    st.success("Court updated successfully!")
                                    st.session_state[f"edit_court_{court['id']}"] = False
                                    st.rerun()
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"edit_court_{court['id']}"] = False
                                st.rerun()
    
    def _show_add_court_form(self):
        """Display form to add new court"""
        with st.form("add_court_form"):
            st.markdown("### Add New Court")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Court Name *", placeholder="e.g., Basketball Court 3")
                court_type = st.selectbox("Court Type *", 
                                        ["Basketball", "Volleyball", "Tennis", "Badminton", "Multi-Purpose"])
                capacity = st.number_input("Capacity (people) *", min_value=1, value=50)
                hourly_rate = st.number_input("Hourly Rate ($) *", min_value=0, value=75)
            
            with col2:
                condition = st.selectbox("Initial Condition", 
                                       ["Excellent", "Good", "Fair", "Poor"], index=0)
                installation_date = st.date_input("Installation Date", value=datetime.now().date())
                features = st.multiselect("Features", 
                                        ["LED Lighting", "Sound System", "Scoreboard", "Air Conditioning", "Live Streaming"])
                accessibility = st.checkbox("ADA Accessible")
            
            notes = st.text_area("Additional Notes", 
                                placeholder="Any special information about this court...")
            
            if st.form_submit_button("➕ Add Court"):
                if name and court_type and capacity and hourly_rate:
                    new_court = {
                        "name": name,
                        "type": court_type,
                        "capacity": capacity,
                        "hourly_rate": hourly_rate,
                        "condition": condition,
                        "last_maintenance": installation_date.strftime('%Y-%m-%d'),
                        "installation_date": installation_date.strftime('%Y-%m-%d'),
                        "features": features,
                        "accessibility": accessibility,
                        "notes": notes
                    }
                    
                    if self.data_manager.add_record("courts", new_court):
                        st.success(f"✅ Added new court: {name}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add court")
                else:
                    st.error("❌ Please fill in all required fields")
    
    def _show_court_utilization(self):
        """Display court utilization analytics"""
        courts = self.get_courts()
        
        if not courts:
            st.info("No court data available")
            return
        
        # Generate utilization data
        utilization_data = []
        for court in courts:
            for hour in range(6, 23):  # 6 AM to 11 PM
                utilization = random.uniform(0.2, 0.95)
                utilization_data.append({
                    'Court': court['name'],
                    'Hour': f"{hour:02d}:00",
                    'Utilization': utilization,
                    'Revenue': court['hourly_rate'] * utilization
                })
        
        df_utilization = pd.DataFrame(utilization_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Hourly Utilization")
            
            if PLOTLY_AVAILABLE:
                fig = px.line(df_utilization, x='Hour', y='Utilization', color='Court',
                            title="Court Utilization Throughout the Day")
                st.plotly_chart(fig, use_container_width=True)
            else:
                pivot_util = df_utilization.pivot_table(index='Hour', columns='Court', values='Utilization')
                st.line_chart(pivot_util)
        
        with col2:
            st.markdown("### 💰 Revenue Analysis")
            
            # Revenue by court
            court_revenue = df_utilization.groupby('Court')['Revenue'].sum().reset_index()
            
            if PLOTLY_AVAILABLE:
                fig = px.bar(court_revenue, x='Court', y='Revenue',
                           title="Daily Revenue by Court")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart(court_revenue.set_index('Court'))
        
        # Court performance metrics
        st.markdown("### 🏆 Court Performance Metrics")
        
        for court in courts:
            court_data = df_utilization[df_utilization['Court'] == court['name']]
            avg_utilization = court_data['Utilization'].mean()
            daily_revenue = court_data['Revenue'].sum()
            peak_hour = court_data.loc[court_data['Utilization'].idxmax(), 'Hour']
            
            with st.expander(f"📊 {court['name']} Performance"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Avg Utilization", f"{avg_utilization:.1%}")
                
                with col2:
                    st.metric("Daily Revenue", f"${daily_revenue:.0f}")
                
                with col3:
                    st.metric("Peak Hour", peak_hour)
                
                with col4:
                    efficiency = (avg_utilization * daily_revenue) / 1000
                    st.metric("Efficiency Score", f"{efficiency:.1f}")
    
    def _show_court_maintenance(self):
        """Display court maintenance tracking"""
        courts = self.get_courts()
        maintenance_requests = self.data_manager.get_data("maintenance_requests")
        
        st.markdown("### 🔧 Maintenance Schedule & History")
        
        # Maintenance overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overdue_maintenance = len([c for c in courts if self._is_maintenance_overdue(c['last_maintenance'])])
            st.metric("Overdue Maintenance", overdue_maintenance)
        
        with col2:
            active_requests = len([m for m in maintenance_requests if m['status'] in ['Scheduled', 'In Progress']])
            st.metric("Active Requests", active_requests)
        
        with col3:
            total_maintenance_cost = sum(m['cost'] for m in maintenance_requests)
            st.metric("Total Maintenance Cost", f"${total_maintenance_cost:,}")
        
        with col4:
            avg_cost = total_maintenance_cost / len(maintenance_requests) if maintenance_requests else 0
            st.metric("Avg Request Cost", f"${avg_cost:.0f}")
        
        # Maintenance requests
        st.markdown("### 📋 Current Maintenance Requests")
        
        for request in maintenance_requests:
            priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            status_color = {"Scheduled": "🔵", "In Progress": "🟡", "Completed": "🟢", "Pending": "⚪"}
            
            with st.expander(f"{priority_color.get(request['priority'], '⚪')} {request['facility']} - {request['type']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Facility:** {request['facility']}  
                    **Type:** {request['type']}  
                    **Priority:** {request['priority']}  
                    **Status:** {status_color.get(request['status'], '⚪')} {request['status']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Scheduled Date:** {request['date']}  
                    **Estimated Cost:** ${request['cost']:,}  
                    **Days Until Due:** {(datetime.strptime(request['date'], '%Y-%m-%d') - datetime.now()).days}
                    """)
                
                # Action buttons
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button(f"✅ Mark Complete", key=f"complete_{request['id']}"):
                        updates = {"status": "Completed"}
                        self.data_manager.update_record("maintenance_requests", request['id'], updates)
                        st.success("Maintenance marked as completed!")
                        st.rerun()
                
                with col_b:
                    if st.button(f"📅 Reschedule", key=f"reschedule_{request['id']}"):
                        st.success("Rescheduling interface opened")
                
                with col_c:
                    if st.button(f"🗑️ Cancel", key=f"cancel_{request['id']}"):
                        self.data_manager.delete_record("maintenance_requests", request['id'])
                        st.success("Maintenance request cancelled")
                        st.rerun()
        
        # Add new maintenance request
        with st.expander("➕ Add New Maintenance Request"):
            with st.form("add_maintenance_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    facility = st.selectbox("Facility", [c['name'] for c in courts])
                    maintenance_type = st.selectbox("Maintenance Type", 
                                                  ["Floor Refinishing", "Equipment Repair", "Cleaning", "Inspection", "Lighting", "HVAC", "Other"])
                    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                
                with col2:
                    scheduled_date = st.date_input("Scheduled Date", value=datetime.now().date() + timedelta(days=7))
                    estimated_cost = st.number_input("Estimated Cost ($)", min_value=0, value=500)
                    contractor = st.text_input("Contractor/Vendor", placeholder="Maintenance Company Name")
                
                description = st.text_area("Description", placeholder="Describe the maintenance work needed...")
                
                if st.form_submit_button("📋 Create Maintenance Request"):
                    new_request = {
                        "facility": facility,
                        "type": maintenance_type,
                        "priority": priority,
                        "status": "Scheduled",
                        "date": scheduled_date.strftime('%Y-%m-%d'),
                        "cost": estimated_cost,
                        "contractor": contractor,
                        "description": description,
                        "created_date": datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    if self.data_manager.add_record("maintenance_requests", new_request):
                        st.success("✅ Maintenance request created!")
                        st.rerun()
    
    def _is_maintenance_overdue(self, last_maintenance: str, days_threshold: int = 90) -> bool:
        """Check if maintenance is overdue"""
        try:
            last_date = datetime.strptime(last_maintenance, '%Y-%m-%d')
            return (datetime.now() - last_date).days > days_threshold
        except:
            return False

# =============================================================================
# TURF MANAGEMENT MODULE
# =============================================================================

class TurfManager:
    """Comprehensive turf management system"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def get_turfs(self) -> List[Dict]:
        """Get all turf fields"""
        return self.data_manager.get_data("turfs")
    
    def show_turf_interface(self):
        """Display turf management interface"""
        st.markdown("## ⚽ Turf Management System")
        st.markdown('<span class="ai-badge">FIELD OPTIMIZATION</span>', unsafe_allow_html=True)
        
        # Turf overview
        turfs = self.get_turfs()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Fields", len(turfs))
        with col2:
            avg_health = sum(t['turf_health'] for t in turfs) / len(turfs) if turfs else 0
            st.metric("Avg Turf Health", f"{avg_health:.1f}/10")
        with col3:
            avg_drainage = sum(t['drainage_score'] for t in turfs) / len(turfs) if turfs else 0
            st.metric("Avg Drainage", f"{avg_drainage:.1f}/10")
        with col4:
            total_capacity = sum(t['capacity'] for t in turfs)
            st.metric("Total Capacity", total_capacity)
        
        # Turf management tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Field List", "➕ Add Field", "🌱 Health Monitoring", "💧 Irrigation"])
        
        with tab1:
            self._show_turf_list()
        
        with tab2:
            self._show_add_turf_form()
        
        with tab3:
            self._show_turf_health_monitoring()
        
        with tab4:
            self._show_irrigation_system()
    
    def _show_turf_list(self):
        """Display list of all turf fields"""
        turfs = self.get_turfs()
        
        for turf in turfs:
            health_color = "🟢" if turf['turf_health'] > 8.5 else "🟡" if turf['turf_health'] > 7.0 else "🔴"
            drainage_color = "🟢" if turf['drainage_score'] > 8.5 else "🟡" if turf['drainage_score'] > 7.0 else "🔴"
            
            with st.expander(f"{health_color} {turf['name']} - {turf['type']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    **Type:** {turf['type']}  
                    **Capacity:** {turf['capacity']} players  
                    **Hourly Rate:** ${turf['hourly_rate']}  
                    """)
                
                with col2:
                    st.markdown(f"""
                    {health_color} **Turf Health:** {turf['turf_health']}/10  
                    {drainage_color} **Drainage:** {turf['drainage_score']}/10  
                    **Last Maintenance:** {turf['last_maintenance']}
                    """)
                
                with col3:
                    # Current conditions simulation
                    weather_impact = random.choice(["Optimal", "Wet", "Dry", "Recovering"])
                    usage_today = random.randint(4, 12)
                    
                    st.markdown(f"""
                    **Current Condition:** {weather_impact}  
                    **Usage Today:** {usage_today} hours  
                    **Revenue Today:** ${usage_today * turf['hourly_rate']}
                    """)
                
                # Turf-specific metrics
                st.markdown("#### 🌱 Field Metrics")
                
                metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
                
                with metrics_col1:
                    grass_density = random.uniform(85, 98)
                    st.metric("Grass Density", f"{grass_density:.1f}%")
                
                with metrics_col2:
                    soil_ph = random.uniform(6.5, 7.5)
                    st.metric("Soil pH", f"{soil_ph:.1f}")
                
                with metrics_col3:
                    moisture_level = random.uniform(30, 70)
                    st.metric("Moisture Level", f"{moisture_level:.1f}%")
                
                with metrics_col4:
                    compaction = random.uniform(15, 45)
                    st.metric("Compaction", f"{compaction:.1f}%")
                
                # Action buttons
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    if st.button(f"✏️ Edit", key=f"edit_turf_{turf['id']}"):
                        st.session_state[f"edit_turf_{turf['id']}"] = True
                
                with col_b:
                    if st.button(f"🌱 Treatment", key=f"treatment_turf_{turf['id']}"):
                        st.success(f"Treatment scheduled for {turf['name']}")
                
                with col_c:
                    if st.button(f"💧 Irrigation", key=f"irrigation_turf_{turf['id']}"):
                        st.success(f"Irrigation system activated for {turf['name']}")
                
                with col_d:
                    if st.button(f"📊 Report", key=f"report_turf_{turf['id']}"):
                        st.success(f"Health report generated for {turf['name']}")
    
    def _show_add_turf_form(self):
        """Display form to add new turf field"""
        with st.form("add_turf_form"):
            st.markdown("### Add New Turf Field")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Field Name *", placeholder="e.g., Soccer Field C")
                turf_type = st.selectbox("Field Type *", 
                                       ["Soccer", "Football", "Rugby", "Lacrosse", "Multi-Purpose"])
                capacity = st.number_input("Player Capacity *", min_value=1, value=22)
                hourly_rate = st.number_input("Hourly Rate ($) *", min_value=0, value=95)
            
            with col2:
                turf_health = st.slider("Initial Turf Health", 1.0, 10.0, 8.0, 0.1)
                drainage_score = st.slider("Drainage Score", 1.0, 10.0, 8.5, 0.1)
                installation_date = st.date_input("Installation Date", value=datetime.now().date())
                turf_type_material = st.selectbox("Turf Material", 
                                                ["Natural Grass", "Artificial Turf", "Hybrid"])
            
            features = st.multiselect("Field Features", 
                                    ["Underground Heating", "Drainage System", "Irrigation", "LED Lighting", "Scoreboard"])
            
            notes = st.text_area("Additional Notes", 
                                placeholder="Special information about this field...")
            
            if st.form_submit_button("➕ Add Turf Field"):
                if name and turf_type and capacity and hourly_rate:
                    new_turf = {
                        "name": name,
                        "type": turf_type,
                        "capacity": capacity,
                        "hourly_rate": hourly_rate,
                        "turf_health": turf_health,
                        "drainage_score": drainage_score,
                        "last_maintenance": installation_date.strftime('%Y-%m-%d'),
                        "installation_date": installation_date.strftime('%Y-%m-%d'),
                        "material": turf_type_material,
                        "features": features,
                        "notes": notes
                    }
                    
                    if self.data_manager.add_record("turfs", new_turf):
                        st.success(f"✅ Added new turf field: {name}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add turf field")
                else:
                    st.error("❌ Please fill in all required fields")
    
    def _show_turf_health_monitoring(self):
        """Display turf health monitoring and analytics"""
        turfs = self.get_turfs()
        
        if not turfs:
            st.info("No turf data available")
            return
        
        st.markdown("### 🌱 Turf Health Analytics")
        
        # Health overview
        col1, col2 = st.columns(2)
        
        with col1:
            # Health scores by field
            health_data = pd.DataFrame([(t['name'], t['turf_health']) for t in turfs], 
                                     columns=['Field', 'Health Score'])
            
            if PLOTLY_AVAILABLE:
                fig = px.bar(health_data, x='Field', y='Health Score',
                           title="Turf Health by Field",
                           color='Health Score',
                           color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart(health_data.set_index('Field'))
        
        with col2:
            # Drainage scores
            drainage_data = pd.DataFrame([(t['name'], t['drainage_score']) for t in turfs], 
                                       columns=['Field', 'Drainage Score'])
            
            if PLOTLY_AVAILABLE:
                fig = px.bar(drainage_data, x='Field', y='Drainage Score',
                           title="Drainage Performance by Field",
                           color='Drainage Score',
                           color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart(drainage_data.set_index('Field'))
        
        # Detailed health monitoring
        st.markdown("### 🔍 Detailed Health Monitoring")
        
        for turf in turfs:
            with st.expander(f"🌱 {turf['name']} Health Details"):
                # Generate health trend data
                dates = pd.date_range(start='2024-01-01', end='2024-02-14', freq='W')
                health_trend = []
                
                base_health = turf['turf_health']
                for date in dates:
                    # Simulate health variations
                    variation = random.uniform(-0.5, 0.3)
                    health_value = max(1.0, min(10.0, base_health + variation))
                    health_trend.append({
                        'Date': date,
                        'Health Score': health_value,
                        'Drainage Score': turf['drainage_score'] + random.uniform(-0.3, 0.3)
                    })
                
                trend_df = pd.DataFrame(health_trend)
                
                if PLOTLY_AVAILABLE:
                    fig = px.line(trend_df, x='Date', y=['Health Score', 'Drainage Score'],
                                title=f"{turf['name']} Health Trend")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.line_chart(trend_df.set_index('Date'))
                
                # Health recommendations
                health_score = turf['turf_health']
                
                if health_score >= 9.0:
                    st.success("🌟 Excellent condition! Continue current maintenance schedule.")
                elif health_score >= 8.0:
                    st.info("✅ Good condition. Monitor for any declining areas.")
                elif health_score >= 7.0:
                    st.warning("⚠️ Fair condition. Consider increased treatment frequency.")
                else:
                    st.error("🚨 Poor condition. Immediate intervention required!")
                
                # Treatment recommendations
                st.markdown("**Recommended Actions:**")
                
                recommendations = []
                if health_score < 8.0:
                    recommendations.append("🌱 Overseed thin areas")
                if turf['drainage_score'] < 8.0:
                    recommendations.append("💧 Improve drainage system")
                if random.choice([True, False]):
                    recommendations.append("🧪 Soil pH testing and adjustment")
                
                for rec in recommendations:
                    st.markdown(f"• {rec}")
    
    def _show_irrigation_system(self):
        """Display irrigation system management"""
        turfs = self.get_turfs()
        
        st.markdown("### 💧 Irrigation System Management")
        
        # Irrigation overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            active_zones = random.randint(3, 8)
            st.metric("Active Zones", active_zones)
        
        with col2:
            daily_usage = random.randint(2000, 5000)
            st.metric("Daily Water Usage", f"{daily_usage:,} gal")
        
        with col3:
            efficiency = random.uniform(85, 95)
            st.metric("System Efficiency", f"{efficiency:.1f}%")
        
        with col4:
            next_cycle = datetime.now() + timedelta(hours=random.randint(1, 6))
            st.metric("Next Cycle", next_cycle.strftime('%I:%M %p'))
        
        # Irrigation zones
        st.markdown("### 🌊 Irrigation Zones")
        
        for i, turf in enumerate(turfs):
            zone_id = f"Zone {i+1}"
            
            with st.expander(f"💧 {zone_id} - {turf['name']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    """
🏟️ NXS Sports AI Platform - Complete System with All Missing Modules
Enterprise-Grade Sports Facility Management Platform

Complete implementation including:
- Sponsorship Management
- Turf Management 
- Court Management
- Board of Directors Portal
- Referee Management
- Data Management (CRUD Operations)
- Admin Controls
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import hashlib
import uuid
from typing import Dict, List, Optional, Any
import time
import random

# Handle optional dependencies with fallbacks
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available. Charts will use Streamlit's built-in visualization.")

# Configure page
st.set_page_config(
    page_title="NXS Sports AI Platform - Complete",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1f77b4, #ff7f0e);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
    .ai-badge {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    .facility-status {
        background: #e8f5e8;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #4caf50;
    }
    .nil-alert {
        background: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffc107;
    }
    .board-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #6f42c1;
        margin: 10px 0;
    }
    .sponsor-card {
        background: #e7f3ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 10px 0;
    }
    .referee-card {
        background: #fff3e0;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 10px 0;
    }
    .data-card {
        background: #f3e5f5;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #9c27b0;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA MANAGEMENT SYSTEM
# =============================================================================

class DataManager:
    """Central data management system for all platform data"""
    
    def __init__(self):
        self.data_store = self._initialize_data_store()
    
    def _initialize_data_store(self) -> Dict[str, Any]:
        """Initialize all data collections"""
        return {
            "members": self._default_members(),
            "courts": self._default_courts(),
            "turfs": self._default_turfs(),
            "sponsors": self._default_sponsors(),
            "board_members": self._default_board_members(),
            "referees": self._default_referees(),
            "tournaments": self._default_tournaments(),
            "maintenance_requests": self._default_maintenance(),
            "facility_bookings": self._default_bookings()
        }
    
    def _default_members(self) -> List[Dict]:
        return [
            {"id": "M001", "name": "John Smith", "email": "john@email.com", "type": "Premium", "join_date": "2023-01-15", "status": "Active", "monthly_fee": 89},
            {"id": "M002", "name": "Sarah Wilson", "email": "sarah@email.com", "type": "Elite", "join_date": "2022-08-20", "status": "Active", "monthly_fee": 149},
            {"id": "M003", "name": "Mike Davis", "email": "mike@email.com", "type": "Basic", "join_date": "2023-11-05", "status": "At Risk", "monthly_fee": 49}
        ]
    
    def _default_courts(self) -> List[Dict]:
        return [
            {"id": "C001", "name": "Basketball Court 1", "type": "Basketball", "capacity": 50, "hourly_rate": 75, "condition": "Excellent", "last_maintenance": "2024-01-15"},
            {"id": "C002", "name": "Basketball Court 2", "type": "Basketball", "capacity": 50, "hourly_rate": 85, "condition": "Good", "last_maintenance": "2024-01-10"},
            {"id": "C003", "name": "Volleyball Court 1", "type": "Volleyball", "capacity": 30, "hourly_rate": 55, "condition": "Good", "last_maintenance": "2024-02-01"},
            {"id": "C004", "name": "Tennis Court 1", "type": "Tennis", "capacity": 4, "hourly_rate": 45, "condition": "Fair", "last_maintenance": "2023-12-20"}
        ]
    
    def _default_turfs(self) -> List[Dict]:
        return [
            {"id": "T001", "name": "Soccer Field A", "type": "Soccer", "capacity": 22, "hourly_rate": 95, "turf_health": 9.1, "drainage_score": 8.8, "last_maintenance": "2024-02-05"},
            {"id": "T002", "name": "Soccer Field B", "type": "Soccer", "capacity": 22, "hourly_rate": 85, "turf_health": 8.7, "drainage_score": 9.2, "last_maintenance": "2024-01-28"},
            {"id": "T003", "name": "Football Field", "type": "Football", "capacity": 100, "hourly_rate": 120, "turf_health": 7.8, "drainage_score": 8.5, "last_maintenance": "2024-01-20"}
        ]
    
    def _default_sponsors(self) -> List[Dict]:
        return [
            {"id": "S001", "name": "SportsTech Solutions", "type": "Naming Rights", "value": 50000, "status": "Active", "contact": "John Doe", "email": "john@sportstech.com", "renewal": "2024-12-31"},
            {"id": "S002", "name": "Healthy Energy Drinks", "type": "Beverage Partner", "value": 25000, "status": "Active", "contact": "Jane Smith", "email": "jane@healthyenergy.com", "renewal": "2024-06-30"},
            {"id": "S003", "name": "Athletic Gear Co", "type": "Equipment Sponsor", "value": 18000, "status": "Pending", "contact": "Bob Wilson", "email": "bob@athleticgear.com", "renewal": "2024-08-15"}
        ]
    
    def _default_board_members(self) -> List[Dict]:
        return [
            {"id": "B001", "name": "Dr. Robert Johnson", "position": "Chairman", "tenure": "2020-2026", "email": "rjohnson@board.com", "phone": "(555) 123-4567", "expertise": "Finance"},
            {"id": "B002", "name": "Maria Rodriguez", "position": "Vice Chairman", "tenure": "2021-2027", "email": "mrodriguez@board.com", "phone": "(555) 234-5678", "expertise": "Operations"},
            {"id": "B003", "name": "James Chen", "position": "Treasurer", "tenure": "2022-2028", "email": "jchen@board.com", "phone": "(555) 345-6789", "expertise": "Accounting"},
            {"id": "B004", "name": "Lisa Thompson", "position": "Secretary", "tenure": "2023-2029", "email": "lthompson@board.com", "phone": "(555) 456-7890", "expertise": "Legal"}
        ]
    
    def _default_referees(self) -> List[Dict]:
        return [
            {"id": "R001", "name": "Mike Anderson", "sports": ["Basketball", "Volleyball"], "level": "Professional", "rate": 150, "availability": "Available", "phone": "(555) 111-2222"},
            {"id": "R002", "name": "Sarah Brown", "sports": ["Soccer", "Football"], "level": "Semi-Professional", "rate": 120, "availability": "Available", "phone": "(555) 222-3333"},
            {"id": "R003", "name": "David Lee", "sports": ["Basketball"], "level": "Amateur", "rate": 80, "availability": "Busy", "phone": "(555) 333-4444"},
            {"id": "R004", "name": "Jennifer White", "sports": ["Tennis", "Volleyball"], "level": "Professional", "rate": 140, "availability": "Available", "phone": "(555) 444-5555"}
        ]
    
    def _default_tournaments(self) -> List[Dict]:
        return [
            {"id": "T001", "name": "State Basketball Championship", "sport": "Basketball", "date": "2024-03-15", "participants": 32, "status": "Confirmed", "revenue": 25000},
            {"id": "T002", "name": "Youth Soccer League", "sport": "Soccer", "date": "2024-04-10", "participants": 48, "status": "Pending", "revenue": 18000},
            {"id": "T003", "name": "Volleyball Tournament", "sport": "Volleyball", "date": "2024-05-05", "participants": 24, "status": "Planning", "revenue": 12000}
        ]
    
    def _default_maintenance(self) -> List[Dict]:
        return [
            {"id": "MR001", "facility": "Basketball Court 1", "type": "Floor Refinishing", "priority": "Medium", "status": "Scheduled", "date": "2024-03-01", "cost": 2500},
            {"id": "MR002", "facility": "Soccer Field A", "type": "Turf Inspection", "priority": "High", "status": "In Progress", "date": "2024-02-20", "cost": 800},
            {"id": "MR003", "facility": "HVAC System", "type": "Filter Replacement", "priority": "Low", "status": "Pending", "date": "2024-03-10", "cost": 300}
        ]
    
    def _default_bookings(self) -> List[Dict]:
        return [
            {"id": "BK001", "facility": "Basketball Court 1", "date": "2024-02-20", "time": "18:00-20:00", "client": "Youth League", "status": "Confirmed", "revenue": 150},
            {"id": "BK002", "facility": "Soccer Field A", "date": "2024-02-21", "time": "16:00-18:00", "client": "Local Club", "status": "Confirmed", "revenue": 190},
            {"id": "BK003", "facility": "Volleyball Court 1", "date": "2024-02-22", "time": "19:00-21:00", "client": "Tournament", "status": "Pending", "revenue": 110}
        ]
    
    def get_data(self, collection: str) -> List[Dict]:
        """Get all data from a collection"""
        return self.data_store.get(collection, [])
    
    def add_record(self, collection: str, record: Dict) -> bool:
        """Add a new record to a collection"""
        try:
            if collection not in self.data_store:
                self.data_store[collection] = []
            
            # Generate ID if not provided
            if 'id' not in record:
                existing_ids = [item.get('id', '') for item in self.data_store[collection]]
                record['id'] = self._generate_id(collection, existing_ids)
            
            self.data_store[collection].append(record)
            return True
        except Exception as e:
            st.error(f"Error adding record: {e}")
            return False
    
    def update_record(self, collection: str, record_id: str, updates: Dict) -> bool:
        """Update an existing record"""
        try:
            for i, record in enumerate(self.data_store[collection]):
                if record.get('id') == record_id:
                    self.data_store[collection][i].update(updates)
                    return True
            return False
        except Exception as e:
            st.error(f"Error updating record: {e}")
            return False
    
    def delete_record(self, collection: str, record_id: str) -> bool:
        """Delete a record from a collection"""
        try:
            self.data_store[collection] = [
                record for record in self.data_store[collection] 
                if record.get('id') != record_id
            ]
            return True
        except Exception as e:
            st.error(f"Error deleting record: {e}")
            return False
    
    def _generate_id(self, collection: str, existing_ids: List[str]) -> str:
        """Generate a new ID for a collection"""
        prefix_map = {
            "members": "M",
            "courts": "C", 
            "turfs": "T",
            "sponsors": "S",
            "board_members": "B",
            "referees": "R",
            "tournaments": "T",
            "maintenance_requests": "MR",
            "facility_bookings": "BK"
        }
        
        prefix = prefix_map.get(collection, "GEN")
        
        # Find the highest existing number
        numbers = []
        for existing_id in existing_ids:
            if existing_id.startswith(prefix):
                try:
                    number = int(existing_id[len(prefix):])
                    numbers.append(number)
                except ValueError:
                    continue
        
        next_number = max(numbers, default=0) + 1
        return f"{prefix}{next_number:03d}"

# =============================================================================
# SPONSORSHIP MANAGEMENT MODULE  
# =============================================================================

class SponsorshipManager:
    """Complete sponsorship management system"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def get_sponsors(self) -> List[Dict]:
        """Get all sponsors"""
        return self.data_manager.get_data("sponsors")
    
    def get_sponsor_analytics(self) -> Dict:
        """Get sponsorship analytics"""
        sponsors = self.get_sponsors()
        
        total_value = sum(s['value'] for s in sponsors)
        active_sponsors = len([s for s in sponsors if s['status'] == 'Active'])
        pending_sponsors = len([s for s in sponsors if s['status'] == 'Pending'])
        
        return {
            "total_sponsors": len(sponsors),
            "active_sponsors": active_sponsors,
            "pending_sponsors": pending_sponsors,
            "total_value": total_value,
            "avg_value": total_value / len(sponsors) if sponsors else 0,
            "renewal_due_30_days": len([s for s in sponsors if self._renewal_due_soon(s['renewal'])])
        }
    
    def _renewal_due_soon(self, renewal_date: str) -> bool:
        """Check if renewal is due within 30 days"""
        try:
            renewal = datetime.strptime(renewal_date, "%Y-%m-%d")
            return (renewal - datetime.now()).days <= 30
        except:
            return False
    
    def show_sponsorship_interface(self):
        """Display sponsorship management interface"""
        st.markdown("## 🤝 Sponsorship Management")
        st.markdown('<span class="ai-badge">PARTNERSHIP OPTIMIZATION</span>', unsafe_allow_html=True)
        
        # Analytics overview
        analytics = self.get_sponsor_analytics()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Sponsors", analytics['total_sponsors'])
        with col2:
            st.metric("Active Sponsors", analytics['active_sponsors'])
        with col3:
            st.metric("Total Value", f"${analytics['total_value']:,}")
        with col4:
            st.metric("Average Value", f"${analytics['avg_value']:,.0f}")
        with col5:
            st.metric("Renewals Due", analytics['renewal_due_30_days'])
        
        # Sponsor management tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Sponsor List", "➕ Add Sponsor", "📊 Analytics", "📄 Contracts"])
        
        with tab1:
            self._show_sponsor_list()
        
        with tab2:
            self._show_add_sponsor_form()
        
        with tab3:
            self._show_sponsor_analytics()
        
        with tab4:
            self._show_sponsor_contracts()
    
    def _show_sponsor_list(self):
        """Display list of all sponsors"""
        sponsors = self.get_sponsors()
        
        for sponsor in sponsors:
            status_color = {"Active": "🟢", "Pending": "🟡", "Expired": "🔴"}
            
            with st.expander(f"{status_color.get(sponsor['status'], '⚪')} {sponsor['name']} - ${sponsor['value']:,}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Type:** {sponsor['type']}  
                    **Value:** ${sponsor['value']:,}  
                    **Status:** {sponsor['status']}  
                    **Contact:** {sponsor['contact']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Email:** {sponsor['email']}  
                    **Renewal Date:** {sponsor['renewal']}  
                    **Days to Renewal:** {(datetime.strptime(sponsor['renewal'], '%Y-%m-%d') - datetime.now()).days}
                    """)
                
                # Action buttons
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button(f"✏️ Edit {sponsor['name']}", key=f"edit_sponsor_{sponsor['id']}"):
                        st.session_state[f"edit_sponsor_{sponsor['id']}"] = True
                
                with col_b:
                    if st.button(f"📧 Contact {sponsor['name']}", key=f"contact_sponsor_{sponsor['id']}"):
                        st.success(f"Email sent to {sponsor['contact']} at {sponsor['email']}")
                
                with col_c:
                    if st.button(f"🗑️ Delete {sponsor['name']}", key=f"delete_sponsor_{sponsor['id']}"):
                        if self.data_manager.delete_record("sponsors", sponsor['id']):
                            st.success(f"Deleted sponsor: {sponsor['name']}")
                            st.rerun()
                
                # Edit form
                if st.session_state.get(f"edit_sponsor_{sponsor['id']}", False):
                    with st.form(f"edit_sponsor_form_{sponsor['id']}"):
                        st.markdown("### Edit Sponsor Details")
                        
                        new_name = st.text_input("Sponsor Name", value=sponsor['name'])
                        new_type = st.selectbox("Sponsorship Type", 
                                               ["Naming Rights", "Beverage Partner", "Equipment Sponsor", "Event Sponsor", "Media Partner"],
                                               index=["Naming Rights", "Beverage Partner", "Equipment Sponsor", "Event Sponsor", "Media Partner"].index(sponsor['type']) if sponsor['type'] in ["Naming Rights", "Beverage Partner", "Equipment Sponsor", "Event Sponsor", "Media Partner"] else 0)
                        new_value = st.number_input("Annual Value ($)", value=sponsor['value'], min_value=0)
                        new_status = st.selectbox("Status", ["Active", "Pending", "Expired"], 
                                                 index=["Active", "Pending", "Expired"].index(sponsor['status']))
                        new_contact = st.text_input("Contact Person", value=sponsor['contact'])
                        new_email = st.text_input("Email", value=sponsor['email'])
                        new_renewal = st.date_input("Renewal Date", 
                                                   value=datetime.strptime(sponsor['renewal'], '%Y-%m-%d').date())
                        
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                updates = {
                                    "name": new_name,
                                    "type": new_type,
                                    "value": new_value,
                                    "status": new_status,
                                    "contact": new_contact,
                                    "email": new_email,
                                    "renewal": new_renewal.strftime('%Y-%m-%d')
                                }
                                
                                if self.data_manager.update_record("sponsors", sponsor['id'], updates):
                                    st.success("Sponsor updated successfully!")
                                    st.session_state[f"edit_sponsor_{sponsor['id']}"] = False
                                    st.rerun()
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"edit_sponsor_{sponsor['id']}"] = False
                                st.rerun()
    
    def _show_add_sponsor_form(self):
        """Display form to add new sponsor"""
        with st.form("add_sponsor_form"):
            st.markdown("### Add New Sponsor")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Sponsor Name *", placeholder="e.g., SportsTech Solutions")
                sponsor_type = st.selectbox("Sponsorship Type *", 
                                          ["Naming Rights", "Beverage Partner", "Equipment Sponsor", "Event Sponsor", "Media Partner"])
                value = st.number_input("Annual Value ($) *", min_value=0, value=10000)
                contact = st.text_input("Contact Person *", placeholder="John Doe")
            
            with col2:
                email = st.text_input("Email *", placeholder="contact@sponsor.com")
                phone = st.text_input("Phone", placeholder="(555) 123-4567")
                renewal_date = st.date_input("Contract Renewal Date *", 
                                           value=datetime.now().date() + timedelta(days=365))
                status = st.selectbox("Status", ["Pending", "Active", "Expired"], index=0)
            
            benefits = st.text_area("Sponsorship Benefits", 
                                   placeholder="List the benefits provided to this sponsor...")
            
            if st.form_submit_button("➕ Add Sponsor"):
                if name and sponsor_type and value and contact and email:
                    new_sponsor = {
                        "name": name,
                        "type": sponsor_type,
                        "value": value,
                        "status": status,
                        "contact": contact,
                        "email": email,
                        "phone": phone,
                        "renewal": renewal_date.strftime('%Y-%m-%d'),
                        "benefits": benefits,
                        "created_date": datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    if self.data_manager.add_record("sponsors", new_sponsor):
                        st.success(f"✅ Added new sponsor: {name}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add sponsor")
                else:
                    st.error("❌ Please fill in all required fields")
    
    def _show_sponsor_analytics(self):
        """Display sponsor analytics and insights"""
        sponsors = self.get_sponsors()
        
        if not sponsors:
            st.info("No sponsor data available")
            return
        
        # Revenue by type
        type_revenue = {}
        for sponsor in sponsors:
            sponsor_type = sponsor['type']
            type_revenue[sponsor_type] = type_revenue.get(sponsor_type, 0) + sponsor['value']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Revenue by Sponsorship Type")
            
            if PLOTLY_AVAILABLE:
                fig = px.pie(values=list(type_revenue.values()), names=list(type_revenue.keys()),
                           title="Sponsorship Revenue Distribution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                revenue_df = pd.DataFrame(list(type_revenue.items()), columns=['Type', 'Revenue'])
                st.bar_chart(revenue_df.set_index('Type'))
        
        with col2:
            st.markdown("### 📅 Renewal Timeline")
            
            # Group by renewal month
            renewal_months = {}
            for sponsor in sponsors:
                try:
                    month = datetime.strptime(sponsor['renewal'], '%Y-%m-%d').strftime('%Y-%m')
                    renewal_months[month] = renewal_months.get(month, 0) + 1
                except:
                    continue
            
            if renewal_months:
                renewal_df = pd.DataFrame(list(renewal_months.items()), columns=['Month', 'Renewals'])
                st.bar_chart(renewal_df.set_index('Month'))
        
        # Sponsor insights
        st.markdown("### 🔍 Sponsorship Insights")
        
        insights = [
            f"📊 **Total Portfolio Value:** ${sum(s['value'] for s in sponsors):,}",
            f"🏆 **Largest Sponsor:** {max(sponsors, key=lambda x: x['value'])['name']} (${max(sponsors, key=lambda x: x['value'])['value']:,})",
            f"📈 **Average Deal Size:** ${sum(s['value'] for s in sponsors) / len(sponsors):,.0f}",
            f"⏰ **Urgent Renewals:** {len([s for s in sponsors if self._renewal_due_soon(s['renewal'])])} sponsors need attention",
            f"✅ **Active Rate:** {len([s for s in sponsors if s['status'] == 'Active']) / len(sponsors) * 100:.1f}%"
        ]
        
        for insight in insights:
            st.markdown(insight)
    
    def _show_sponsor_contracts(self):
        """Display sponsor contracts and documentation"""
        st.markdown("### 📄 Sponsor Contracts & Documentation")
        
        sponsors = self.get_sponsors()
        
        for sponsor in sponsors:
            with st.expander(f"📋 {sponsor['name']} Contract Details"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Contract Information:**")
                    st.markdown(f"- **Value:** ${sponsor['value']:,}")
                    st.markdown(f"- **Type:** {sponsor['type']}")
                    st.markdown(f"- **Renewal:** {sponsor['renewal']}")
                    st.markdown(f"- **Status:** {sponsor['status']}")
                
                with col2:
                    st.markdown("**Contact Information:**")
                    st.markdown(f"- **Contact:** {sponsor['contact']}")
                    st.markdown(f"- **Email:** {sponsor['email']}")
                    st.markdown(f"- **Phone:** {sponsor.get('phone', 'N/A')}")
                
                # Contract actions
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    if st.button(f"📄 Generate Contract", key=f"contract_{sponsor['id']}"):
                        st.success(f"Contract generated for {sponsor['name']}")
                
                with col_b:
                    if st.button(f"📧 Send Renewal", key=f"renewal_{sponsor['id']}"):
                        st.success(f"Renewal notice sent to {sponsor['contact']}")
                
                with col_c:
                    if st.button(f"💼 Schedule Meeting", key=f"meeting_{sponsor['id']}"):
                        st.success(f"Meeting scheduled with {sponsor['name']}")
                
                with col_d:
                    if st.button(f"📊 Performance Report", key=f"report_{sponsor['id']}"):
                        st.success(f"Performance report generated for {sponsor['name']}")

# =============================================================================
# COURT MANAGEMENT MODULE
# =============================================================================

class CourtManager:
    """Comprehensive court management system"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def get_courts(self) -> List[Dict]:
        """Get all courts"""
        return self.data_manager.get_data("courts")
    
    def show_court_interface(self):
        """Display court management interface"""
        st.markdown("## 🏀 Court Management System")
        st.markdown('<span class="ai-badge">FACILITY OPTIMIZATION</span>', unsafe_allow_html=True)
        
        # Court overview
        courts = self.get_courts()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Courts", len(courts))
        with col2:
            excellent_courts = len([c for c in courts if c['condition'] == 'Excellent'])
            st.metric("Excellent Condition", excellent_courts)
        with col3:
            total_capacity = sum(c['capacity'] for c in courts)
            st.metric("Total Capacity", total_capacity)
        with col4:
            avg_rate = sum(c['hourly_rate'] for c in courts) / len(courts) if courts else 0
            st.metric("Avg Hourly Rate", f"${avg_rate:.0f}")
        
        # Court management tabs
        tab1, tab2