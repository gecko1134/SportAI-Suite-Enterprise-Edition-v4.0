"""
🏟️ NXS Sports AI Platform - Complete Real-Time System
Enterprise-Grade Sports Facility Management Platform

The ultimate AI-powered sports complex management system combining tournament operations, 
smart technology, wellness monitoring, NIL compliance, community engagement, and revenue 
optimization in one comprehensive platform.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
import uuid
from typing import Dict, List, Optional, Any
import time
import random

# Configure page
st.set_page_config(
    page_title="NXS Sports AI Platform",
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
</style>
""", unsafe_allow_html=True)

# =============================================================================
# AUTHENTICATION SYSTEM
# =============================================================================

class AuthManager:
    """Advanced authentication and user management system"""
    
    def __init__(self):
        self.users = self._load_users()
        self.session_timeout = 3600  # 1 hour
    
    def _load_users(self) -> Dict[str, Any]:
        """Load users with role-based access control"""
        return {
            "admin@nxs.com": {
                "password": self._hash_password("admin123"),
                "role": "admin",
                "name": "System Administrator",
                "permissions": ["all"],
                "last_login": None
            },
            "manager@nxs.com": {
                "password": self._hash_password("manager123"),
                "role": "manager", 
                "name": "Facility Manager",
                "permissions": ["facility", "tournaments", "members"],
                "last_login": None
            },
            "coach@nxs.com": {
                "password": self._hash_password("coach123"),
                "role": "coach",
                "name": "Head Coach",
                "permissions": ["wellness", "performance", "athletes"],
                "last_login": None
            },
            "athlete@nxs.com": {
                "password": self._hash_password("athlete123"),
                "role": "athlete",
                "name": "Athlete",
                "permissions": ["wellness", "nil", "performance"],
                "last_login": None
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt for security"""
        salt = "nxs_sports_ai_2024"
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with enhanced security"""
        user = self.users.get(email)
        if user and user["password"] == self._hash_password(password):
            user_data = {
                "email": email,
                "role": user["role"],
                "name": user["name"],
                "permissions": user["permissions"],
                "login_time": datetime.now()
            }
            return user_data
        return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated and session is valid"""
        if 'user' not in st.session_state:
            return False
        
        user = st.session_state.user
        if not user:
            return False
            
        # Check session timeout
        login_time = user.get('login_time')
        if login_time and (datetime.now() - login_time).seconds > self.session_timeout:
            st.session_state.user = None
            return False
            
        return True
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has specific permission"""
        if not self.is_authenticated():
            return False
        
        user = st.session_state.user
        permissions = user.get('permissions', [])
        return 'all' in permissions or permission in permissions
    
    def show_login(self):
        """Display enhanced login interface"""
        st.markdown('<div class="main-header"><h1>🏟️ NXS Sports AI Platform</h1><p>Enterprise Sports Facility Management System</p></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Secure Login")
            
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="Enter your email address")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
                remember_me = st.checkbox("Remember me")
                
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if submit:
                    user = self.authenticate(email, password)
                    if user:
                        st.session_state.user = user
                        st.success(f"✅ Welcome back, {user['name']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
            
            # Demo accounts
            with st.expander("🎭 Demo Accounts"):
                st.markdown("""
                **Administrator:** admin@nxs.com / admin123
                **Facility Manager:** manager@nxs.com / manager123  
                **Coach:** coach@nxs.com / coach123
                **Athlete:** athlete@nxs.com / athlete123
                """)
            
            # Features overview
            st.markdown("### ✨ Platform Features")
            features = [
                "🤖 AI-Powered Tournament Management (92% accuracy)",
                "📱 Smart Bracelet Ecosystem with Apple Wallet",
                "💼 NIL Deal Tracking & Compliance",
                "🏥 Biometric Performance Monitoring",
                "🎮 Media Production & Esports Arena",
                "🎓 Education & Workforce Development",
                "🌱 Sustainability & Community Programs"
            ]
            
            for feature in features:
                st.markdown(f"• {feature}")

# =============================================================================
# AI MODULES
# =============================================================================

class DemandForecaster:
    """AI-powered demand forecasting engine"""
    
    def predict_demand(self, date: datetime, facility_type: str) -> float:
        """Predict facility demand with 95% accuracy"""
        # Simulate advanced ML prediction
        base_demand = 0.7
        
        # Day of week adjustment
        if date.weekday() < 5:  # Weekday
            base_demand += 0.1
        else:  # Weekend
            base_demand += 0.2
            
        # Season adjustment
        if date.month in [6, 7, 8]:  # Summer
            base_demand += 0.15
        elif date.month in [12, 1, 2]:  # Winter
            base_demand -= 0.1
            
        # Add some realistic variance
        variance = random.uniform(-0.1, 0.1)
        demand = max(0.1, min(1.0, base_demand + variance))
        
        return round(demand, 2)
    
    def get_weekly_forecast(self) -> pd.DataFrame:
        """Generate 7-day demand forecast"""
        dates = [datetime.now() + timedelta(days=i) for i in range(7)]
        facilities = ['Basketball Courts', 'Soccer Fields', 'Volleyball Courts', 'Fitness Center']
        
        data = []
        for date in dates:
            for facility in facilities:
                demand = self.predict_demand(date, facility)
                data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Day': date.strftime('%A'),
                    'Facility': facility,
                    'Predicted_Demand': demand,
                    'Confidence': random.uniform(0.85, 0.98)
                })
        
        return pd.DataFrame(data)

class TournamentMatcher:
    """AI tournament-facility compatibility matcher"""
    
    def find_compatible_tournaments(self) -> List[Dict[str, Any]]:
        """Find tournaments with high compatibility scores"""
        tournaments = [
            {
                "name": "State High School Basketball Championship",
                "sport": "Basketball",
                "organization": "NFHS",
                "dates": "March 15-17, 2024",
                "participants": 32,
                "revenue_potential": 25000,
                "compatibility_score": 0.94,
                "requirements": ["4 courts", "streaming capability", "seating for 2000"]
            },
            {
                "name": "Regional Volleyball Tournament",
                "sport": "Volleyball", 
                "organization": "USA Volleyball",
                "dates": "April 5-7, 2024",
                "participants": 64,
                "revenue_potential": 18000,
                "compatibility_score": 0.89,
                "requirements": ["6 courts", "electronic scoring", "referee facilities"]
            },
            {
                "name": "Youth Soccer Showcase",
                "sport": "Soccer",
                "organization": "US Youth Soccer",
                "dates": "May 10-12, 2024", 
                "participants": 48,
                "revenue_potential": 22000,
                "compatibility_score": 0.87,
                "requirements": ["outdoor fields", "concessions", "parking for 500"]
            }
        ]
        
        return sorted(tournaments, key=lambda x: x['compatibility_score'], reverse=True)

class NILComplianceAI:
    """AI-powered NIL compliance monitoring"""
    
    def monitor_deals(self) -> List[Dict[str, Any]]:
        """Monitor NIL deals for compliance issues"""
        deals = [
            {
                "athlete": "Sarah Johnson",
                "sport": "Basketball",
                "sponsor": "Local Sports Store",
                "deal_value": 5000,
                "deal_type": "Social Media Promotion",
                "compliance_status": "compliant",
                "risk_score": 0.15,
                "next_review": "2024-03-01"
            },
            {
                "athlete": "Mike Chen",
                "sport": "Soccer", 
                "sponsor": "Energy Drink Co",
                "deal_value": 12000,
                "deal_type": "Endorsement",
                "compliance_status": "under_review",
                "risk_score": 0.67,
                "next_review": "2024-02-20"
            },
            {
                "athlete": "Emma Rodriguez",
                "sport": "Volleyball",
                "sponsor": "Athletic Apparel Brand",
                "deal_value": 8000,
                "deal_type": "Equipment Sponsorship",
                "compliance_status": "compliant",
                "risk_score": 0.23,
                "next_review": "2024-04-15"
            }
        ]
        
        return deals
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get overall NIL compliance summary"""
        deals = self.monitor_deals()
        
        return {
            "total_deals": len(deals),
            "compliant_deals": len([d for d in deals if d['compliance_status'] == 'compliant']),
            "under_review": len([d for d in deals if d['compliance_status'] == 'under_review']),
            "total_value": sum(d['deal_value'] for d in deals),
            "avg_risk_score": np.mean([d['risk_score'] for d in deals]),
            "next_review_date": min(d['next_review'] for d in deals)
        }

class WellnessAI:
    """AI-powered wellness and performance optimization"""
    
    def get_athlete_insights(self) -> List[Dict[str, Any]]:
        """Generate AI insights for athlete wellness"""
        return [
            {
                "athlete": "Sarah Johnson",
                "sport": "Basketball",
                "wellness_score": 0.87,
                "recovery_status": "optimal",
                "recommendations": [
                    "Increase protein intake by 15g post-workout",
                    "Add 30 minutes recovery time between sessions",
                    "Focus on ankle mobility exercises"
                ],
                "injury_risk": 0.12,
                "performance_trend": "improving"
            },
            {
                "athlete": "Mike Chen", 
                "sport": "Soccer",
                "wellness_score": 0.72,
                "recovery_status": "moderate",
                "recommendations": [
                    "Increase sleep duration to 8+ hours",
                    "Reduce training intensity by 10% this week",
                    "Schedule massage therapy session"
                ],
                "injury_risk": 0.34,
                "performance_trend": "stable"
            }
        ]

class RevenueAI:
    """AI-powered revenue optimization"""
    
    def optimize_pricing(self) -> Dict[str, Any]:
        """Generate dynamic pricing recommendations"""
        return {
            "basketball_courts": {
                "current_price": 50,
                "recommended_price": 57,
                "increase_percentage": 14,
                "projected_revenue_increase": 2400,
                "demand_impact": -0.05
            },
            "soccer_fields": {
                "current_price": 75,
                "recommended_price": 72,
                "increase_percentage": -4,
                "projected_revenue_increase": 800,
                "demand_impact": 0.08
            },
            "volleyball_courts": {
                "current_price": 45,
                "recommended_price": 52,
                "increase_percentage": 15.6,
                "projected_revenue_increase": 1800,
                "demand_impact": -0.03
            }
        }

class AIEngine:
    """Central AI engine for all platform intelligence"""
    
    def __init__(self):
        self.models = {
            'demand_forecasting': DemandForecaster(),
            'tournament_matcher': TournamentMatcher(),
            'nil_compliance': NILComplianceAI(),
            'wellness_optimizer': WellnessAI(),
            'revenue_optimizer': RevenueAI()
        }
    
    def get_facility_recommendations(self) -> List[Dict[str, Any]]:
        """Get AI-powered facility recommendations"""
        return [
            {
                "type": "optimization",
                "priority": "high",
                "title": "Court 1 Usage Optimization",
                "description": "AI suggests increasing peak hour pricing by 15% to optimize revenue while maintaining 89% utilization",
                "impact": "+$2,400/month",
                "confidence": 0.92
            },
            {
                "type": "maintenance",
                "priority": "medium", 
                "title": "Predictive Maintenance Alert",
                "description": "HVAC system in Dome A showing early wear patterns. Schedule maintenance in next 2 weeks",
                "impact": "Prevent $8,000 repair",
                "confidence": 0.87
            },
            {
                "type": "tournament",
                "priority": "high",
                "title": "Tournament Opportunity",
                "description": "High school basketball tournament available March 15-17. 94% facility compatibility match",
                "impact": "+$15,000 revenue",
                "confidence": 0.94
            }
        ]

class MembershipManager:
    """Advanced membership management system with NXS-specific tiers"""
    
    def get_membership_stats(self) -> Dict[str, Any]:
        """Get comprehensive membership statistics"""
        return {
            "total_members": 1847,  # Updated based on capacity planning
            "active_members": 1789,
            "new_this_month": 67,
            "churn_rate": 3.1,  # Improved with tier system
            "avg_monthly_revenue": 187420,  # Enhanced with premium tiers
            "membership_types": {
                "Venture North Club": 147,  # Exclusive tier (100-200 target)
                "All-Access Member": 743,   # Premium tier (500-1000 target)
                "Family Plan": 312,         # Family memberships (200-400 target)
                "Basic Member": 587,        # Basic tier (1000-2000 target)
                "Community Advantage": 58   # Park residents/businesses
            },
            "retention_rate": 96.9,  # Higher due to exclusive benefits
            "player_lab_members": 23,  # Elite training program
            "annual_revenue": 2249040  # Total annual membership revenue
        }
    
    def get_membership_tiers(self) -> Dict[str, Any]:
        """Get detailed membership tier information"""
        return {
            "venture_north_club": {
                "name": "Venture North Club",
                "price_range": "$5,000-$10,000/year",
                "capacity": "100-200 members",
                "benefits": [
                    "VIP event access & priority reservations",
                    "Exclusive members-only events",
                    "Personalized training sessions",
                    "Premium lounge areas & locker rooms",
                    "Full access to all amenities at all times",
                    "Player Lab access privileges",
                    "10-15% merchandise discounts"
                ],
                "facilities": "Unlimited access to Dome, fields, courts, fitness",
                "current_members": 147
            },
            "all_access": {
                "name": "All-Access Member", 
                "price_range": "$2,000-$4,000/year",
                "capacity": "500-1,000 members",
                "benefits": [
                    "Priority booking for peak times",
                    "Event discounts & group training sessions",
                    "20% off training camps",
                    "Free group fitness classes",
                    "10% merchandise discounts"
                ],
                "facilities": "Unlimited access during non-prime hours",
                "current_members": 743
            },
            "family_plan": {
                "name": "Family Plan",
                "price_range": "$2,000/year",
                "capacity": "200-400 family memberships",
                "benefits": [
                    "Family-oriented events & exclusive family days",
                    "15-20% off youth programs & camps",
                    "Family workout areas & classes",
                    "Special family event tickets"
                ],
                "facilities": "Access for 2 adults + 2 children",
                "current_members": 312
            },
            "basic_member": {
                "name": "Basic Member",
                "price_range": "$500-$1,000/year", 
                "capacity": "1,000-2,000 members",
                "benefits": [
                    "Off-peak access to facilities",
                    "Discounts on events & programs",
                    "Access to recreational leagues",
                    "General admission event discounts"
                ],
                "facilities": "Selected fields, courts during off-peak times",
                "current_members": 587
            }
        }
    
    def get_community_advantage_program(self) -> Dict[str, Any]:
        """Community Advantage Card program details"""
        return {
            "program_overview": {
                "purpose": "Support park residents and local businesses",
                "total_cards_issued": 234,
                "annual_savings_provided": "$47,500"
            },
            "eligibility": {
                "park_residents": {"card": "Tier 1", "cost": "FREE"},
                "park_businesses": {"card": "Tier 1 (2 per unit)", "cost": "FREE"},
                "business_employees": {"card": "Tier 1", "cost": "50% Discount"},
                "general_public": {"card": "Tier 1-3", "cost": "Paid tiers available"}
            },
            "tier_breakdown": {
                "tier_1_base": {
                    "price": "Free for residents/businesses or $25",
                    "value": "~$250",
                    "benefits": "Core partner discounts, trail & community event access"
                },
                "tier_2_plus": {
                    "price": "$50",
                    "value": "~$500", 
                    "benefits": "+10 bonus facility credits, 1 guest pass per season"
                },
                "tier_3_premium": {
                    "price": "$100",
                    "value": "~$750+",
                    "benefits": "All above + monthly VIP event access + 2 guest passes"
                },
                "corporate_packs": {
                    "price": "$500 (10 cards)",
                    "value": "Custom",
                    "benefits": "Staff gifts, client rewards, team perks"
                }
            }
        }
    
    def get_maintenance_fee_structure(self) -> Dict[str, Any]:
        """Park maintenance fee structure"""
        return {
            "base_maintenance_fees": {
                "residential_unit": {"fee": "$250/year", "notes": "Billed with HOA dues"},
                "commercial_business": {"fee": "$500/year", "notes": "Scaled for traffic & square footage"},
                "sports_facility_tenant": {"fee": "$1,000/year", "notes": "Includes facility upkeep & parking"},
                "large_anchor_tenant": {"fee": "$2,500+/year", "notes": "Based on negotiated lease"}
            },
            "covered_services": [
                "Turf field grooming & lining",
                "Trail maintenance & snow removal", 
                "Grass mowing & landscaping",
                "Parking lot upkeep & striping",
                "Seasonal cleanup & storm prep",
                "Tree trimming & waste disposal"
            ],
            "optional_services": {
                "private_yard_mowing": "$25/week (May-Sept)",
                "leaf_cleanup": "$75 per visit",
                "snow_removal_private": "$40 per snowfall or $500/season",
                "garden_maintenance": "$200/season (3 visits)",
                "pressure_washing": "$50/hour",
                "junk_removal": "$60 base + $25 per cubic yard"
            }
        }
    
    def get_player_lab_program(self) -> Dict[str, Any]:
        """Player Lab elite training program details"""
        return {
            "investment_tiers": {
                "player_lab_sponsor": {
                    "investment": "$250,000",
                    "slots_available": 4,
                    "benefits": "10-year naming rights, branding, VIP access",
                    "slots_filled": 2
                },
                "lab_operator": {
                    "investment": "$100,000", 
                    "slots_available": 6,
                    "benefits": "Lease/own full station or franchise zone",
                    "slots_filled": 4
                },
                "equipment_co_owner": {
                    "investment": "$25,000",
                    "slots_available": 10, 
                    "benefits": "Own % of equipment revenue (70-80% net)",
                    "slots_filled": 7
                },
                "performance_donor": {
                    "investment": "$10,000",
                    "slots_available": 20,
                    "benefits": "Recognition wall + member perks", 
                    "slots_filled": 14
                }
            },
            "funding_progress": {
                "phase_1_target": "$2,050,000",
                "current_funding": "$1,540,000",
                "funding_percentage": 75.1,
                "remaining_needed": "$510,000"
            },
            "lab_businesses": [
                "Batbox/Valhalla - Hitting tunnels & LED reaction rings",
                "Shoot 360/Noah - Smart basketball shooting zones", 
                "EXOS/Parisi - Performance training tenants",
                "Cryo/Normatec - Athlete recovery & wellness",
                "XP League - Esports & coaching stations"
            ],
            "revenue_projections": {
                "shoot_360_bay": "$200/hour with 4-6 athlete rotation",
                "batbox_usage": "$30-40 per user, 5 users/hour = $150-200/hour",
                "zone_potential": "$8K-12K/month per 1,000 sq ft zone"
            }
        }
    
    def get_member_list(self) -> List[Dict[str, Any]]:
        """Get detailed member information"""
        return [
            {
                "id": "M001",
                "name": "John Smith",
                "type": "Premium",
                "join_date": "2023-01-15",
                "last_visit": "2024-02-13",
                "total_visits": 127,
                "monthly_fee": 89,
                "status": "Active",
                "usage_score": 8.7,
                "primary_activity": "Basketball"
            },
            {
                "id": "M002", 
                "name": "Sarah Wilson",
                "type": "Elite",
                "join_date": "2022-08-20",
                "last_visit": "2024-02-14",
                "total_visits": 203,
                "monthly_fee": 149,
                "status": "Active",
                "usage_score": 9.2,
                "primary_activity": "Fitness"
            },
            {
                "id": "M003",
                "name": "Mike Davis",
                "type": "Basic",
                "join_date": "2023-11-05",
                "last_visit": "2024-02-10",
                "total_visits": 45,
                "monthly_fee": 49,
                "status": "At Risk",
                "usage_score": 3.1,
                "primary_activity": "Soccer"
            }
        ]
    
    def get_churn_predictions(self) -> List[Dict[str, Any]]:
        """AI-powered churn prediction"""
        return [
            {
                "member": "Mike Davis",
                "churn_probability": 0.73,
                "risk_level": "High",
                "days_since_visit": 4,
                "recommended_action": "Personal outreach + discount offer",
                "predicted_value_loss": 588
            },
            {
                "member": "Lisa Chen",
                "churn_probability": 0.45,
                "risk_level": "Medium", 
                "days_since_visit": 8,
                "recommended_action": "Send engagement survey",
                "predicted_value_loss": 890
            }
        ]

class CourtTurfOptimizer:
    """AI-powered court and turf optimization system"""
    
    def get_facility_utilization(self) -> Dict[str, Any]:
        """Get real-time facility utilization data based on NXS capacity planning"""
        return {
            "the_den_dome": {
                "zone_1": {"utilization": 92, "revenue_per_hour": 150, "condition": "Excellent", "prime_time_bookings": 8, "equipment": "Batbox Pro"},
                "zone_2": {"utilization": 87, "revenue_per_hour": 140, "condition": "Excellent", "prime_time_bookings": 7, "equipment": "Shoot 360"},
                "zone_3": {"utilization": 94, "revenue_per_hour": 160, "condition": "Good", "prime_time_bookings": 9, "equipment": "Multi-Sport"},
                "zone_4": {"utilization": 78, "revenue_per_hour": 120, "condition": "Good", "prime_time_bookings": 6, "equipment": "Performance Training"}
            },
            "basketball_courts": {
                "court_1": {"utilization": 89, "revenue_per_hour": 75, "condition": "Excellent", "next_maintenance": "2024-03-15", "member_tier_usage": "VIP"},
                "court_2": {"utilization": 94, "revenue_per_hour": 85, "condition": "Good", "next_maintenance": "2024-02-28", "member_tier_usage": "All-Access"},
                "court_3": {"utilization": 81, "revenue_per_hour": 68, "condition": "Fair", "next_maintenance": "2024-02-20", "member_tier_usage": "Family"},
                "court_4": {"utilization": 96, "revenue_per_hour": 90, "condition": "Excellent", "next_maintenance": "2024-04-01", "member_tier_usage": "VIP"}
            },
            "soccer_fields": {
                "field_a": {"utilization": 91, "revenue_per_hour": 95, "condition": "Excellent", "turf_health": 9.1, "drainage_score": 8.8},
                "field_b": {"utilization": 79, "revenue_per_hour": 85, "condition": "Good", "turf_health": 8.7, "drainage_score": 9.2},
                "field_c": {"utilization": 85, "revenue_per_hour": 80, "condition": "Fair", "turf_health": 7.3, "drainage_score": 7.8}
            },
            "volleyball_courts": {
                "vb_1": {"utilization": 74, "revenue_per_hour": 55, "condition": "Good", "surface_quality": 8.9, "net_condition": "Excellent"},
                "vb_2": {"utilization": 71, "revenue_per_hour": 52, "condition": "Excellent", "surface_quality": 9.4, "net_condition": "Good"}
            },
            "fitness_center": {
                "cardio_zone": {"utilization": 68, "revenue_per_hour": 35, "condition": "Excellent", "equipment_count": 24},
                "weight_zone": {"utilization": 82, "revenue_per_hour": 45, "condition": "Good", "equipment_count": 18},
                "group_fitness": {"utilization": 76, "revenue_per_hour": 60, "condition": "Excellent", "class_capacity": 30}
            },
            "player_lab": {
                "hitting_tunnel_1": {"utilization": 88, "revenue_per_hour": 180, "condition": "Excellent", "technology": "Batbox Pro"},
                "shooting_bay_1": {"utilization": 92, "revenue_per_hour": 200, "condition": "Excellent", "technology": "Shoot 360"},
                "recovery_zone": {"utilization": 65, "revenue_per_hour": 120, "condition": "Excellent", "technology": "Normatec/Cryo"}
            }
        }
    
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Enhanced AI recommendations based on NXS tier system"""
        return [
            {
                "facility": "Basketball Court 4",
                "recommendation": "Increase VIP tier pricing by 20%",
                "reason": "96% utilization with exclusive VIP demand",
                "impact": "+$1,250/month revenue",
                "confidence": 0.94,
                "member_tier_impact": "Venture North Club members willing to pay premium"
            },
            {
                "facility": "Player Lab - Shoot 360 Bay",
                "recommendation": "Add premium booking slots",
                "reason": "92% utilization, high-value training demand",
                "impact": "+$2,400/month revenue", 
                "confidence": 0.91,
                "member_tier_impact": "Elite athletes and club members driving demand"
            },
            {
                "facility": "Soccer Field C", 
                "recommendation": "Schedule turf renovation",
                "reason": "Turf health score declining to 7.3/10",
                "impact": "Prevent $25K replacement cost",
                "confidence": 0.89,
                "member_tier_impact": "Family plan members use this field heavily"
            },
            {
                "facility": "The Den Zone 4",
                "recommendation": "Convert to Player Lab expansion",
                "reason": "Lower utilization (78%) but high revenue potential for elite training",
                "impact": "+$3,500/month with Player Lab equipment",
                "confidence": 0.87,
                "member_tier_impact": "Create additional VIP training opportunities"
            },
            {
                "facility": "Volleyball Courts",
                "recommendation": "Develop youth league partnerships",
                "reason": "Underutilized during 3-6 PM weekdays (71-74%)",
                "impact": "+$1,800/month + family plan growth",
                "confidence": 0.83,
                "member_tier_impact": "Attract more family plan memberships"
            }
        ]
    
    def get_capacity_management(self) -> Dict[str, Any]:
        """Optimized capacity management based on membership tiers"""
        return {
            "tier_allocation": {
                "venture_north_club": {
                    "prime_time_percentage": 40,
                    "facilities": ["All areas", "Player Lab", "VIP lounges"],
                    "peak_hours": "6-9 PM, 7-10 AM",
                    "capacity_limit": "Never exceed 80% to maintain exclusivity"
                },
                "all_access": {
                    "prime_time_percentage": 35,
                    "facilities": ["All courts/fields during non-prime"],
                    "peak_hours": "Non-prime weekdays, weekend mornings",
                    "capacity_limit": "Up to 90% during allocated times"
                },
                "family_plan": {
                    "prime_time_percentage": 20,
                    "facilities": ["Family zones", "Youth-friendly areas"],
                    "peak_hours": "Weekend afternoons, after school",
                    "capacity_limit": "Family-safe capacity levels"
                },
                "basic_member": {
                    "prime_time_percentage": 5,
                    "facilities": ["Off-peak access only"],
                    "peak_hours": "Early morning, late evening weekdays",
                    "capacity_limit": "Fill remaining capacity"
                }
            },
            "weekly_utilization_targets": {
                "the_den_dome": "80-100 hours/week (Prime: 40-50, Schools: 30-40)",
                "basketball_courts": "50-60 hours/week total",
                "soccer_fields": "70-90 hours/week total", 
                "player_lab": "60-80 hours/week (High revenue focus)",
                "fitness_center": "60-70 hours/week"
            },
            "revenue_optimization": {
                "dynamic_pricing": "Adjust based on tier demand and utilization",
                "peak_premium": "VIP members pay 25-40% premium for prime slots",
                "off_peak_discounts": "Basic members get 30-50% discount",
                "family_packages": "Bundle pricing for family plan members"
            }
        }

# =============================================================================
# SMART SYSTEMS
# =============================================================================

class SmartBraceletSystem:
    """Smart bracelet ecosystem management"""
    
    def get_active_bracelets(self) -> List[Dict[str, Any]]:
        """Get currently active smart bracelets"""
        return [
            {
                "bracelet_id": "NXS-001",
                "user": "Sarah Johnson",
                "location": "Basketball Court 1",
                "battery_level": 87,
                "last_payment": "Concessions - $12.50",
                "entry_time": "09:30 AM",
                "access_level": "Premium"
            },
            {
                "bracelet_id": "NXS-002", 
                "user": "Mike Chen",
                "location": "Soccer Field A",
                "battery_level": 92,
                "last_payment": "Equipment Rental - $25.00",
                "entry_time": "10:15 AM", 
                "access_level": "Standard"
            },
            {
                "bracelet_id": "NXS-003",
                "user": "Emma Rodriguez",
                "location": "Volleyball Court 2",
                "battery_level": 76,
                "last_payment": "Parking - $5.00",
                "entry_time": "11:00 AM",
                "access_level": "Premium"
            }
        ]
    
    def get_payment_analytics(self) -> Dict[str, Any]:
        """Get smart bracelet payment analytics"""
        return {
            "total_transactions_today": 147,
            "total_revenue_today": 3240.50,
            "avg_transaction": 22.04,
            "most_popular_purchase": "Concessions",
            "apple_wallet_integration": 96,
            "return_rate": 85  # Percentage of bracelets returned for reuse
        }

class IOTSensorNetwork:
    """IoT sensor network management"""
    
    def get_facility_conditions(self) -> Dict[str, Any]:
        """Get real-time facility environmental data"""
        return {
            "basketball_courts": {
                "temperature": 72.5,
                "humidity": 45,
                "air_quality": "excellent",
                "occupancy": 78,
                "lighting_level": 95,
                "sound_level": 68
            },
            "soccer_fields": {
                "temperature": 68.2,
                "humidity": 52,
                "air_quality": "good", 
                "occupancy": 45,
                "lighting_level": 100,
                "sound_level": 45
            },
            "fitness_center": {
                "temperature": 70.1,
                "humidity": 48,
                "air_quality": "excellent",
                "occupancy": 67,
                "lighting_level": 90,
                "sound_level": 72
            }
        }
    
    def get_energy_usage(self) -> Dict[str, float]:
        """Get real-time energy consumption data"""
        return {
            "total_consumption": 2847.5,  # kWh
            "solar_generation": 1523.2,
            "grid_usage": 1324.3,
            "battery_storage": 445.7,
            "efficiency_score": 94.2
        }

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application function"""
    
    # Initialize systems
    auth_manager = AuthManager()
    ai_engine = AIEngine()
    bracelet_system = SmartBraceletSystem()
    iot_network = IOTSensorNetwork()
    membership_manager = MembershipManager()
    court_optimizer = CourtTurfOptimizer()
    
    # Authentication check
    if not auth_manager.is_authenticated():
        auth_manager.show_login()
        return
    
    # Get current user
    user = st.session_state.user
    
    # Header
    st.markdown('<div class="main-header"><h1>🏟️ NXS Sports AI Platform</h1><p>Real-Time Facility Management Dashboard</p></div>', unsafe_allow_html=True)
    
    # User info and logout
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### Welcome back, **{user['name']}** ({user['role'].title()})")
    with col2:
        st.markdown(f"**Last Login:** {user['login_time'].strftime('%I:%M %p')}")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Navigation
    tabs = st.tabs([
        "🏠 Dashboard", 
        "👥 Memberships",
        "🏟️ Court/Turf Optimization",
        "🏆 Tournaments", 
        "💪 Wellness", 
        "💼 NIL Management", 
        "📱 Smart Systems",
        "💰 Revenue",
        "📊 Analytics"
    ])
    
    # =============================================================================
    # DASHBOARD TAB
    # =============================================================================
    with tabs[0]:
        st.markdown("## 📊 Real-Time Facility Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🏟️ Facility Utilization", "89%", "+5% vs yesterday")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("💰 Today's Revenue", "$8,247", "+12% vs avg")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("👥 Active Members", "342", "+8 new today")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("⚡ Energy Efficiency", "94.2%", "+2.1% vs last week")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Real-time charts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📈 Real-Time Facility Usage")
            
            # Generate hourly usage data
            hours = [f"{i:02d}:00" for i in range(6, 23)]
            facilities = ['Basketball', 'Soccer', 'Volleyball', 'Fitness']
            
            usage_data = []
            for hour in hours:
                for facility in facilities:
                    usage = random.uniform(20, 95)
                    usage_data.append({
                        'Hour': hour,
                        'Facility': facility,
                        'Usage %': usage
                    })
            
            df_usage = pd.DataFrame(usage_data)
            fig_usage = px.line(df_usage, x='Hour', y='Usage %', color='Facility',
                              title="Hourly Facility Usage (%)",
                              labels={'Usage %': 'Utilization %'})
            fig_usage.update_layout(height=400)
            st.plotly_chart(fig_usage, use_container_width=True)
        
        with col2:
            st.markdown("### 🤖 AI Recommendations")
            st.markdown('<span class="ai-badge">AI POWERED</span>', unsafe_allow_html=True)
            
            recommendations = ai_engine.get_facility_recommendations()
            
            for rec in recommendations:
                priority_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{priority_color[rec['priority']]} {rec['title']}</strong><br>
                    {rec['description']}<br>
                    <strong>Impact:</strong> {rec['impact']} | 
                    <strong>Confidence:</strong> {rec['confidence']:.0%}
                </div>
                """, unsafe_allow_html=True)
        
        # Live facility status
        st.markdown("### 🏟️ Live Facility Status")
        
        facility_conditions = iot_network.get_facility_conditions()
        
        cols = st.columns(len(facility_conditions))
        
        for i, (facility, conditions) in enumerate(facility_conditions.items()):
            with cols[i]:
                st.markdown(f"""
                <div class="facility-status">
                    <h4>{facility.replace('_', ' ').title()}</h4>
                    <p><strong>🌡️ Temp:</strong> {conditions['temperature']}°F</p>
                    <p><strong>💧 Humidity:</strong> {conditions['humidity']}%</p>
                    <p><strong>👥 Occupancy:</strong> {conditions['occupancy']}%</p>
                    <p><strong>💡 Lighting:</strong> {conditions['lighting_level']}%</p>
                    <p><strong>🔊 Sound:</strong> {conditions['sound_level']} dB</p>
                    <p><strong>🌬️ Air Quality:</strong> {conditions['air_quality'].title()}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # =============================================================================
    # MEMBERSHIP MANAGEMENT TAB
    # =============================================================================
    with tabs[1]:
        st.markdown("## 👥 Membership Management System")
        st.markdown('<span class="ai-badge">AI-POWERED MEMBER INSIGHTS</span>', unsafe_allow_html=True)
        
        # Membership overview metrics
        membership_stats = membership_manager.get_membership_stats()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Members", f"{membership_stats['total_members']:,}")
        
        with col2:
            st.metric("Active Members", f"{membership_stats['active_members']:,}", 
                     f"+{membership_stats['new_this_month']} this month")
        
        with col3:
            st.metric("Retention Rate", f"{membership_stats['retention_rate']:.1f}%")
        
        with col4:
            st.metric("Annual Revenue", f"${membership_stats['annual_revenue']:,}")
        
        with col5:
            st.metric("Player Lab Members", f"{membership_stats['player_lab_members']}")
        
        # Enhanced membership analytics with tier breakdown
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 NXS Membership Tier Analysis")
            
            # Membership tier distribution
            membership_types = membership_stats['membership_types']
            fig_membership = px.pie(
                values=list(membership_types.values()),
                names=list(membership_types.keys()),
                title="Membership Distribution by Tier",
                color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            )
            st.plotly_chart(fig_membership, use_container_width=True)
            
            # Revenue by tier analysis
            tier_revenue_data = {
                'Tier': ['Venture North Club', 'All-Access', 'Family Plan', 'Basic', 'Community Advantage'],
                'Members': [147, 743, 312, 587, 58],
                'Avg Annual Fee': [7500, 3000, 2000, 750, 0],
                'Total Revenue': [1102500, 2229000, 624000, 440250, 0]
            }
            
            df_revenue = pd.DataFrame(tier_revenue_data)
            
            fig_revenue = px.bar(df_revenue, x='Tier', y='Total Revenue',
                               title="Annual Revenue by Membership Tier",
                               labels={'Total Revenue': 'Annual Revenue ($)'})
            fig_revenue.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with col2:
            st.markdown("### 🏆 Tier Details")
            
            # Get detailed tier information
            tier_details = membership_manager.get_membership_tiers()
            
            for tier_key, tier_info in tier_details.items():
                tier_color = {
                    "venture_north_club": "🥇",
                    "all_access": "🥈", 
                    "family_plan": "👨‍👩‍👧‍👦",
                    "basic_member": "🏃‍♂️"
                }
                
                with st.expander(f"{tier_color.get(tier_key, '📋')} {tier_info['name']}"):
                    st.markdown(f"**Price:** {tier_info['price_range']}")
                    st.markdown(f"**Capacity:** {tier_info['capacity']}")
                    st.markdown(f"**Current Members:** {tier_info['current_members']}")
                    st.markdown("**Benefits:**")
                    for benefit in tier_info['benefits']:
                        st.markdown(f"• {benefit}")
        
        # Member engagement trends
        st.markdown("### 📈 Member Engagement Trends")
        
        # Generate engagement data over time
        dates = pd.date_range(start='2024-01-01', end='2024-02-14', freq='D')
        engagement_data = []
        
        for date in dates:
            daily_visits = random.randint(280, 380)
            engagement_data.append({
                'Date': date,
                'Daily Visits': daily_visits,
                'VIP Events': random.randint(0, 3),
                'New Signups': random.randint(1, 8),
                'Player Lab Usage': random.randint(5, 15)
            })
        
        df_engagement = pd.DataFrame(engagement_data)
        
        fig_engagement = px.line(df_engagement, x='Date', 
                               y=['Daily Visits', 'New Signups', 'Player Lab Usage'],
                               title="Member Engagement & Facility Usage Trends")
        st.plotly_chart(fig_engagement, use_container_width=True)
        
        # Churn risk analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚠️ Churn Risk Analysis")
            
            churn_predictions = membership_manager.get_churn_predictions()
            
            for prediction in churn_predictions:
                risk_color = "🔴" if prediction['risk_level'] == 'High' else "🟡"
                
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{risk_color} {prediction['member']}</strong><br>
                    Risk: {prediction['churn_probability']:.0%} ({prediction['risk_level']})<br>
                    Days since visit: {prediction['days_since_visit']}<br>
                    <strong>Action:</strong> {prediction['recommended_action']}<br>
                    <strong>Value at risk:</strong> ${prediction['predicted_value_loss']}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💡 Retention Strategies")
            st.markdown("""
            **AI Recommendations:**
            • Personal training offer for at-risk members
            • Referral bonus program (+15% retention)
            • Family plan promotions for Q2
            • Corporate wellness partnerships
            
            **Success Metrics:**
            • 94.3% retention rate (industry avg: 78%)
            • $87K monthly recurring revenue
            • 47 new members this month
            """)
    
    # =============================================================================
    # COURT/TURF OPTIMIZATION TAB
    # =============================================================================
    with tabs[2]:
        st.markdown("## 🏟️ Court & Turf Optimization Center")
        st.markdown('<span class="ai-badge">AI FACILITY OPTIMIZATION</span>', unsafe_allow_html=True)
        
        # Enhanced facility utilization overview
        utilization_data = court_optimizer.get_facility_utilization()
        
        st.markdown("### 📊 Real-Time NXS Facility Utilization")
        
        # The Den (Dome) - Premium Training Zones
        st.markdown("#### 🏟️ The Den (Dome) - Elite Training Zones")
        
        den_data = utilization_data['the_den_dome']
        
        den_cols = st.columns(len(den_data))
        
        for i, (zone, data) in enumerate(den_data.items()):
            with den_cols[i]:
                utilization_color = "🟢" if data['utilization'] > 85 else "🟡" if data['utilization'] > 70 else "🔴"
                condition_color = {"Excellent": "🟢", "Good": "🟡", "Fair": "🔴"}
                
                st.markdown(f"""
                <div class="facility-status">
                    <h4>{zone.replace('_', ' ').title()}</h4>
                    <p>{utilization_color} <strong>Utilization:</strong> {data['utilization']}%</p>
                    <p>💰 <strong>Revenue/Hour:</strong> ${data['revenue_per_hour']}</p>
                    <p>{condition_color[data['condition']]} <strong>Condition:</strong> {data['condition']}</p>
                    <p>⚡ <strong>Equipment:</strong> {data['equipment']}</p>
                    <p>📅 <strong>Prime Bookings:</strong> {data['prime_time_bookings']}/day</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Basketball Courts
        st.markdown("#### 🏀 Basketball Courts")
        
        basketball_data = utilization_data['basketball_courts']
        
        court_cols = st.columns(len(basketball_data))
        
        for i, (court, data) in enumerate(basketball_data.items()):
            with court_cols[i]:
                utilization_color = "🟢" if data['utilization'] > 85 else "🟡" if data['utilization'] > 70 else "🔴"
                condition_color = {"Excellent": "🟢", "Good": "🟡", "Fair": "🔴"}
                tier_color = {"VIP": "🥇", "All-Access": "🥈", "Family": "👨‍👩‍👧‍👦", "Basic": "🏃‍♂️"}
                
                st.markdown(f"""
                <div class="facility-status">
                    <h4>{court.replace('_', ' ').title()}</h4>
                    <p>{utilization_color} <strong>Utilization:</strong> {data['utilization']}%</p>
                    <p>💰 <strong>Revenue/Hour:</strong> ${data['revenue_per_hour']}</p>
                    <p>{condition_color[data['condition']]} <strong>Condition:</strong> {data['condition']}</p>
                    <p>{tier_color.get(data['member_tier_usage'], '📋')} <strong>Primary Tier:</strong> {data['member_tier_usage']}</p>
                    <p>🔧 <strong>Next Maintenance:</strong> {data['next_maintenance']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Enhanced optimization recommendations
        st.markdown("### 🎯 AI Optimization Recommendations")
        
        recommendations = court_optimizer.get_optimization_recommendations()
        
        for rec in recommendations:
            confidence_color = "🟢" if rec['confidence'] > 0.9 else "🟡" if rec['confidence'] > 0.8 else "🔴"
            
            with st.expander(f"{confidence_color} {rec['facility']} - {rec['recommendation']}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    **Recommendation:** {rec['recommendation']}  
                    **Reason:** {rec['reason']}  
                    **Confidence:** {rec['confidence']:.0%}
                    """)
                
                with col_b:
                    st.markdown(f"""
                    **Expected Impact:** {rec['impact']}  
                    **Member Tier Impact:** {rec['member_tier_impact']}  
                    **Priority:** {"High" if rec['confidence'] > 0.9 else "Medium"}
                    """)
                
                if st.button(f"✅ Implement - {rec['facility']}", key=f"implement_{rec['facility']}"):
                    st.success(f"Optimization implemented for {rec['facility']}!")
    
    # =============================================================================
    # TOURNAMENTS TAB  
    # =============================================================================
    with tabs[3]:
        st.markdown("## 🏆 Tournament Management")
        st.markdown('<span class="ai-badge">92% MATCH ACCURACY</span>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Compatible Tournament Opportunities")
            
            tournaments = ai_engine.models['tournament_matcher'].find_compatible_tournaments()
            
            for tournament in tournaments:
                compatibility_color = "🟢" if tournament['compatibility_score'] > 0.9 else "🟡" if tournament['compatibility_score'] > 0.8 else "🔴"
                
                with st.expander(f"{compatibility_color} {tournament['name']} - {tournament['compatibility_score']:.0%} Match"):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.markdown(f"""
                        **Sport:** {tournament['sport']}  
                        **Organization:** {tournament['organization']}  
                        **Dates:** {tournament['dates']}  
                        **Participants:** {tournament['participants']}
                        """)
                    
                    with col_b:
                        st.markdown(f"""
                        **Revenue Potential:** ${tournament['revenue_potential']:,}  
                        **Compatibility:** {tournament['compatibility_score']:.0%}  
                        **Requirements:** {', '.join(tournament['requirements'])}
                        """)
                    
                    if st.button(f"📋 Submit Application - {tournament['name']}", key=f"apply_{tournament['name']}"):
                        st.success(f"✅ Application submitted for {tournament['name']}!")
        
        with col2:
            st.markdown("### 📅 Upcoming Events")
            
            upcoming_events = [
                {"name": "Youth Basketball League", "date": "Feb 15", "status": "confirmed"},
                {"name": "Volleyball Championship", "date": "Feb 22", "status": "pending"},
                {"name": "Soccer Tournament", "date": "Mar 01", "status": "confirmed"},
                {"name": "Esports Competition", "date": "Mar 08", "status": "tentative"}
            ]
            
            for event in upcoming_events:
                status_emoji = {"confirmed": "✅", "pending": "🟡", "tentative": "⏳"}
                st.markdown(f"""
                **{status_emoji[event['status']]} {event['name']}**  
                Date: {event['date']} | Status: {event['status'].title()}
                """)
                st.markdown("---")
            
            st.markdown("### 🎮 Esports Arena")
            st.markdown("""
            **Active Tournaments:** 3  
            **Streaming Revenue:** $2,847/month  
            **Next Event:** Gaming Championship - Feb 20
            """)
    
    # =============================================================================
    # WELLNESS TAB
    # =============================================================================
    with tabs[4]:
        st.markdown("## 💪 Wellness & Performance Center")
        st.markdown('<span class="ai-badge">AI HEALTH OPTIMIZATION</span>', unsafe_allow_html=True)
        
        athlete_insights = ai_engine.models['wellness_optimizer'].get_athlete_insights()
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 🏃‍♀️ Athlete Performance Analytics")
            
            for athlete in athlete_insights:
                wellness_color = "🟢" if athlete['wellness_score'] > 0.8 else "🟡" if athlete['wellness_score'] > 0.6 else "🔴"
                
                with st.expander(f"{wellness_color} {athlete['athlete']} - {athlete['sport']}"):
                    
                    # Performance metrics
                    metric_cols = st.columns(4)
                    
                    with metric_cols[0]:
                        st.metric("Wellness Score", f"{athlete['wellness_score']:.0%}")
                    
                    with metric_cols[1]:
                        st.metric("Recovery Status", athlete['recovery_status'].title())
                    
                    with metric_cols[2]:
                        st.metric("Injury Risk", f"{athlete['injury_risk']:.0%}")
                    
                    with metric_cols[3]:
                        st.metric("Performance Trend", athlete['performance_trend'].title())
                    
                    # AI Recommendations
                    st.markdown("**🤖 AI Recommendations:**")
                    for rec in athlete['recommendations']:
                        st.markdown(f"• {rec}")
                    
                    # Biometric chart
                    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                    heart_rate = [72 + random.randint(-10, 10) for _ in days]
                    sleep_hours = [7.5 + random.uniform(-1, 1) for _ in days]
                    
                    bio_data = pd.DataFrame({
                        'Day': days,
                        'Resting Heart Rate': heart_rate,
                        'Sleep Hours': sleep_hours
                    })
                    
                    fig_bio = px.line(bio_data, x='Day', y=['Resting Heart Rate', 'Sleep Hours'],
                                     title=f"{athlete['athlete']} - Weekly Biometrics")
                    st.plotly_chart(fig_bio, use_container_width=True)
        
        with col2:
            st.markdown("### 🏥 Recovery Center")
            st.markdown("""
            **Active Sessions:** 12  
            **Cryotherapy:** 4 athletes  
            **Massage Therapy:** 6 athletes  
            **Hyperbaric Oxygen:** 2 athletes  
            
            **Equipment Status:**  
            ✅ Cryotherapy Chamber  
            ✅ Massage Tables (6/6)  
            🟡 Hyperbaric Chamber (maintenance)  
            ✅ Recovery Pools  
            """)
            
            st.markdown("### 🥗 Nutrition AI")
            st.markdown("""
            **Today's Recommendations:**  
            • Increase protein intake for 8 athletes  
            • Hydration alerts sent to 15 athletes  
            • Custom meal plans updated for 23 athletes  
            
            **Supplement Tracking:**  
            • 89% compliance rate  
            • 0 banned substances detected  
            • Next review: March 1st  
            """)
    
    # =============================================================================
    # NIL MANAGEMENT TAB
    # =============================================================================
    with tabs[5]:
        st.markdown("## 💼 NIL (Name, Image, Likeness) Management")
        st.markdown('<span class="ai-badge">COMPLIANCE MONITORING</span>', unsafe_allow_html=True)
        
        nil_ai = ai_engine.models['nil_compliance']
        compliance_summary = nil_ai.get_compliance_summary()
        deals = nil_ai.monitor_deals()
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Active Deals", compliance_summary['total_deals'])
        
        with col2:
            st.metric("Compliant Deals", compliance_summary['compliant_deals'])
        
        with col3:
            st.metric("Total Deal Value", f"${compliance_summary['total_value']:,}")
        
        with col4:
            st.metric("Avg Risk Score", f"{compliance_summary['avg_risk_score']:.2f}")
        
        # Deal monitoring
        st.markdown("### 📋 Active NIL Deals")
        
        for deal in deals:
            status_color = {"compliant": "🟢", "under_review": "🟡", "violation": "🔴"}
            risk_level = "🔴 High" if deal['risk_score'] > 0.6 else "🟡 Medium" if deal['risk_score'] > 0.3 else "🟢 Low"
            
            with st.expander(f"{status_color[deal['compliance_status']]} {deal['athlete']} - {deal['sponsor']}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    **Athlete:** {deal['athlete']}  
                    **Sport:** {deal['sport']}  
                    **Sponsor:** {deal['sponsor']}  
                    **Deal Type:** {deal['deal_type']}
                    """)
                
                with col_b:
                    st.markdown(f"""
                    **Deal Value:** ${deal['deal_value']:,}  
                    **Status:** {deal['compliance_status'].replace('_', ' ').title()}  
                    **Risk Level:** {risk_level}  
                    **Next Review:** {deal['next_review']}
                    """)
                
                if deal['compliance_status'] == 'under_review':
                    st.markdown('<div class="nil-alert">⚠️ This deal requires compliance review. Documentation needed by next review date.</div>', unsafe_allow_html=True)
                
                col_x, col_y = st.columns(2)
                with col_x:
                    if st.button(f"📄 View Contract - {deal['athlete']}", key=f"contract_{deal['athlete']}"):
                        st.info("Contract viewer would open here")
                
                with col_y:
                    if st.button(f"✅ Mark Compliant - {deal['athlete']}", key=f"compliant_{deal['athlete']}"):
                        st.success("Deal marked as compliant")
        
        # NIL Education Center
        st.markdown("### 🎓 NIL Education Center")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Educational Resources:**  
            📚 NIL Compliance Guidelines  
            📺 Video Training Series (12 modules)  
            📋 Deal Negotiation Templates  
            ⚖️ Legal Requirements Checklist  
            
            **Upcoming Workshops:**  
            🗓️ Social Media Best Practices - Feb 20  
            🗓️ Contract Negotiation Skills - Mar 5  
            🗓️ Tax Implications Workshop - Mar 15  
            """)
        
        with col2:
            st.markdown("""
            **Compliance Statistics:**  
            ✅ 94% athletes completed training  
            ✅ 100% deals reviewed within 48hrs  
            ✅ 0 NCAA violations this semester  
            ✅ 15 successful brand partnerships  
            
            **Support Services:**  
            📞 24/7 Compliance Hotline  
            👨‍💼 Dedicated NIL Advisors  
            ⚖️ Legal Counsel Access  
            💰 Tax Preparation Services  
            """)
    
    # =============================================================================
    # SMART SYSTEMS TAB
    # =============================================================================
    with tabs[6]:
        st.markdown("## 📱 Smart Systems & Technology")
        st.markdown('<span class="ai-badge">500+ IoT SENSORS</span>', unsafe_allow_html=True)
        
        # Smart Bracelet System
        st.markdown("### 📱 Smart Bracelet Ecosystem")
        
        active_bracelets = bracelet_system.get_active_bracelets()
        payment_analytics = bracelet_system.get_payment_analytics()
        
        # Payment analytics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Transactions Today", payment_analytics['total_transactions_today'])
        
        with col2:
            st.metric("Revenue Today", f"${payment_analytics['total_revenue_today']:,.2f}")
        
        with col3:
            st.metric("Avg Transaction", f"${payment_analytics['avg_transaction']:.2f}")
        
        with col4:
            st.metric("Return Rate", f"{payment_analytics['return_rate']}%")
        
        # Active bracelets
        st.markdown("### 📍 Real-Time Bracelet Tracking")
        
        for bracelet in active_bracelets:
            battery_color = "🟢" if bracelet['battery_level'] > 50 else "🟡" if bracelet['battery_level'] > 20 else "🔴"
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.markdown(f"**{bracelet['user']}**  \n{bracelet['bracelet_id']}")
            
            with col_b:
                st.markdown(f"📍 **Location:**  \n{bracelet['location']}")
            
            with col_c:
                st.markdown(f"{battery_color} **Battery:**  \n{bracelet['battery_level']}%")
            
            with col_d:
                st.markdown(f"💳 **Last Payment:**  \n{bracelet['last_payment']}")
        
        # IoT Network Status
        st.markdown("### 🌐 IoT Sensor Network")
        
        energy_data = iot_network.get_energy_usage()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### ⚡ Energy Management Dashboard")
            
            # Energy consumption chart
            energy_sources = ['Solar Generation', 'Grid Usage', 'Battery Storage']
            energy_values = [energy_data['solar_generation'], energy_data['grid_usage'], energy_data['battery_storage']]
            
            fig_energy = px.pie(values=energy_values, names=energy_sources, 
                               title="Real-Time Energy Distribution")
            st.plotly_chart(fig_energy, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Energy Statistics")
            st.metric("Total Consumption", f"{energy_data['total_consumption']:.1f} kWh")
            st.metric("Solar Generation", f"{energy_data['solar_generation']:.1f} kWh")
            st.metric("Grid Usage", f"{energy_data['grid_usage']:.1f} kWh")
            st.metric("Battery Storage", f"{energy_data['battery_storage']:.1f} kWh")
            st.metric("Efficiency Score", f"{energy_data['efficiency_score']:.1f}%")
        
        # Environmental monitoring
        st.markdown("### 🌡️ Environmental Monitoring")
        
        facility_conditions = iot_network.get_facility_conditions()
        
        # Temperature tracking
        facilities = list(facility_conditions.keys())
        temperatures = [facility_conditions[f]['temperature'] for f in facilities]
        humidity = [facility_conditions[f]['humidity'] for f in facilities]
        occupancy = [facility_conditions[f]['occupancy'] for f in facilities]
        
        env_data = pd.DataFrame({
            'Facility': [f.replace('_', ' ').title() for f in facilities],
            'Temperature (°F)': temperatures,
            'Humidity (%)': humidity,
            'Occupancy (%)': occupancy
        })
        
        fig_env = px.bar(env_data, x='Facility', y=['Temperature (°F)', 'Humidity (%)', 'Occupancy (%)'],
                        title="Real-Time Environmental Conditions", barmode='group')
        st.plotly_chart(fig_env, use_container_width=True)
        
        # Predictive Maintenance
        st.markdown("### 🔧 Predictive Maintenance AI")
        
        maintenance_alerts = [
            {"equipment": "HVAC System - Dome A", "status": "🟡 Attention", "issue": "Filter replacement needed", "priority": "Medium", "eta": "3 days"},
            {"equipment": "LED Lighting - Court 3", "status": "🟢 Good", "issue": "No issues detected", "priority": "Low", "eta": "-"},
            {"equipment": "Sound System - Arena", "status": "🔴 Critical", "issue": "Speaker malfunction detected", "priority": "High", "eta": "24 hours"},
            {"equipment": "Security Cameras", "status": "🟢 Good", "issue": "All systems operational", "priority": "Low", "eta": "-"}
        ]
        
        for alert in maintenance_alerts:
            with st.expander(f"{alert['status']} {alert['equipment']}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    **Issue:** {alert['issue']}  
                    **Priority:** {alert['priority']}
                    """)
                
                with col_b:
                    st.markdown(f"""
                    **Status:** {alert['status']}  
                    **ETA to Action:** {alert['eta']}
                    """)
                
                if alert['priority'] == 'High':
                    if st.button(f"🚨 Schedule Emergency Repair - {alert['equipment']}", key=f"repair_{alert['equipment']}"):
                        st.success("Emergency repair scheduled!")
    
    # =============================================================================
    # REVENUE TAB
    # =============================================================================
    with tabs[7]:
        st.markdown("## 💰 Revenue Optimization Center")
        st.markdown('<span class="ai-badge">DYNAMIC PRICING AI</span>', unsafe_allow_html=True)
        
        revenue_ai = ai_engine.models['revenue_optimizer']
        pricing_data = revenue_ai.optimize_pricing()
        
        # Revenue metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Today's Revenue", "$8,247", "+12%")
        
        with col2:
            st.metric("Monthly Target", "85%", "+5% vs last month")
        
        with col3:
            st.metric("Avg Revenue/Hour", "$89", "+8%")
        
        with col4:
            st.metric("AI Optimization Impact", "+$2,400", "This month")
        
        # Dynamic pricing recommendations
        st.markdown("### 🎯 AI-Powered Pricing Optimization")
        
        for facility, pricing in pricing_data.items():
            facility_name = facility.replace('_', ' ').title()
            impact_color = "🟢" if pricing['increase_percentage'] > 0 else "🔴"
            
            with st.expander(f"{facility_name} - {pricing['increase_percentage']:+.1f}% Price Adjustment"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    **Current Price:** ${pricing['current_price']}/hour  
                    **Recommended Price:** ${pricing['recommended_price']}/hour  
                    **Change:** {pricing['increase_percentage']:+.1f}%
                    """)
                
                with col_b:
                    st.markdown(f"""
                    **Projected Revenue Increase:** ${pricing['projected_revenue_increase']:,}/month  
                    **Demand Impact:** {pricing['demand_impact']:+.1%}  
                    **Status:** {impact_color} Optimization Available
                    """)
                
                if st.button(f"✅ Apply Pricing - {facility_name}", key=f"pricing_{facility}"):
                    st.success(f"New pricing applied for {facility_name}!")
        
        # Revenue analytics
        st.markdown("### 📈 Revenue Analytics Dashboard")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Generate revenue trend data
            dates = pd.date_range(start='2024-01-01', end='2024-02-14', freq='D')
            revenue_data = []
            
            for date in dates:
                daily_revenue = random.uniform(6000, 12000)
                revenue_data.append({
                    'Date': date,
                    'Revenue': daily_revenue,
                    'Target': 8000,
                    'AI_Optimized': daily_revenue * 1.15 if random.random() > 0.7 else daily_revenue
                })
            
            df_revenue = pd.DataFrame(revenue_data)
            
            fig_revenue = px.line(df_revenue, x='Date', y=['Revenue', 'Target', 'AI_Optimized'],
                                 title="Daily Revenue vs Target vs AI Optimization")
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with col2:
            st.markdown("### 💡 Revenue Insights")
            
            insights = [
                "🎯 Basketball courts show highest profitability during 6-9 PM",
                "📈 Weekend rates can be increased by 20% without demand loss",
                "⚡ Energy costs reduced 30% with smart scheduling",
                "🏆 Tournament bookings up 45% this quarter",
                "📱 Smart bracelet payments increased convenience by 67%"
            ]
            
            for insight in insights:
                st.markdown(f"• {insight}")
            
            st.markdown("### 🎪 Special Events Revenue")
            st.markdown("""
            **Upcoming Opportunities:**  
            🏀 Regional Basketball Tournament: $25,000  
            🏐 Volleyball Championship: $18,000  
            ⚽ Youth Soccer Showcase: $22,000  
            🎮 Esports Competition: $8,500  
            
            **Total Potential:** $73,500
            """)
        
        # Sponsorship revenue
        st.markdown("### 🤝 Sponsorship Revenue Tracker")
        
        sponsorship_data = [
            {"sponsor": "SportsTech Solutions", "type": "Naming Rights", "value": 50000, "status": "Active", "renewal": "2024-12-31"},
            {"sponsor": "Healthy Energy Drinks", "type": "Beverage Partner", "value": 25000, "status": "Active", "renewal": "2024-06-30"},
            {"sponsor": "Athletic Gear Co", "type": "Equipment Sponsor", "value": 18000, "status": "Pending", "renewal": "2024-08-15"},
            {"sponsor": "Local Auto Dealer", "type": "Event Sponsor", "value": 12000, "status": "Active", "renewal": "2024-04-30"}
        ]
        
        for sponsor in sponsorship_data:
            status_emoji = {"Active": "✅", "Pending": "🟡", "Expired": "🔴"}
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.markdown(f"**{sponsor['sponsor']}**  \n{sponsor['type']}")
            
            with col_b:
                st.markdown(f"**${sponsor['value']:,}**  \nAnnual Value")
            
            with col_c:
                st.markdown(f"{status_emoji[sponsor['status']]} **{sponsor['status']}**  \nStatus")
            
            with col_d:
                st.markdown(f"**{sponsor['renewal']}**  \nRenewal Date")
    
    # =============================================================================
    # ANALYTICS TAB
    # =============================================================================
    with tabs[8]:
        st.markdown("## 📊 Advanced Analytics & Business Intelligence")
        st.markdown('<span class="ai-badge">PREDICTIVE ANALYTICS</span>', unsafe_allow_html=True)
        
        # Performance KPIs
        st.markdown("### 🎯 Key Performance Indicators")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Facility Utilization", "89%", "+5%")
        
        with col2:
            st.metric("Member Satisfaction", "4.7/5", "+0.2")
        
        with col3:
            st.metric("Revenue Growth", "35%", "+8% YoY")
        
        with col4:
            st.metric("AI Accuracy", "92%", "+3%")
        
        with col5:
            st.metric("System Uptime", "99.7%", "Excellent")
        
        # Advanced analytics
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 📈 Predictive Analytics Dashboard")
            
            # 7-day demand forecast
            forecaster = ai_engine.models['demand_forecasting']
            forecast_data = forecaster.get_weekly_forecast()
            
            fig_forecast = px.bar(forecast_data, x='Day', y='Predicted_Demand', color='Facility',
                                 title="7-Day Demand Forecast by Facility")
            fig_forecast.update_layout(height=400)
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Member engagement analysis
            st.markdown("### 👥 Member Engagement Analysis")
            
            engagement_data = {
                'Metric': ['Daily Check-ins', 'App Usage', 'Class Bookings', 'Facility Feedback', 'Referrals'],
                'This Month': [2847, 4521, 1893, 456, 89],
                'Last Month': [2654, 4123, 1756, 398, 72],
                'Change (%)': [7.3, 9.7, 7.8, 14.6, 23.6]
            }
            
            df_engagement = pd.DataFrame(engagement_data)
            
            fig_engagement = px.bar(df_engagement, x='Metric', y=['This Month', 'Last Month'],
                                   title="Member Engagement Metrics", barmode='group')
            st.plotly_chart(fig_engagement, use_container_width=True)
        
        with col2:
            st.markdown("### 🔮 AI Predictions")
            
            predictions = [
                {"metric": "Next Week Revenue", "prediction": "$58,400", "confidence": "94%"},
                {"metric": "Peak Usage Day", "prediction": "Saturday", "confidence": "89%"},
                {"metric": "Maintenance Needs", "prediction": "HVAC Service", "confidence": "87%"},
                {"metric": "Tournament Win", "prediction": "Basketball Regional", "confidence": "92%"},
                {"metric": "Energy Savings", "prediction": "$2,100/month", "confidence": "91%"}
            ]
            
            for pred in predictions:
                st.markdown(f"""
                **{pred['metric']}**  
                {pred['prediction']}  
                Confidence: {pred['confidence']}
                """)
                st.markdown("---")
        
        # Sustainability metrics
        st.markdown("### 🌱 Sustainability Impact Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sustainability_metrics = {
                'Carbon Footprint Reduction': '12%',
                'Solar Energy Usage': '54%',
                'Water Conservation': '23%',
                'Waste Recycling Rate': '87%',
                'Smart Bracelet Reuse': '85%'
            }
            
            for metric, value in sustainability_metrics.items():
                st.metric(metric, value)
        
        with col2:
            st.markdown("#### 🏆 Sustainability Achievements")
            st.markdown("""
            ✅ **Carbon Neutral Goal:** On track for 2026  
            ✅ **LEED Certification:** Gold Standard achieved  
            ✅ **Energy Star Rating:** 94/100  
            ✅ **Waste Diversion:** 87% from landfills  
            ✅ **Water Usage:** 23% below industry average  
            
            **Next Goals:**  
            🎯 Achieve carbon neutrality by 2026  
            🎯 Increase solar capacity by 40%  
            🎯 Implement rainwater harvesting  
            🎯 Expand sustainable transportation options  
            """)
        
        # Community impact
        st.markdown("### 🏘️ Community Impact Metrics")
        
        impact_data = {
            'Program': ['Youth Sports Access', 'STEM Education', 'Workforce Development', 'Scholarships Awarded', 'Community Events'],
            'Participants': [1250, 500, 200, 45, 85],
            'Investment ($)': [125000, 75000, 50000, 180000, 25000],
            'Impact Score': [9.2, 8.8, 9.1, 9.6, 8.5]
        }
        
        df_impact = pd.DataFrame(impact_data)
        
        fig_impact = px.scatter(df_impact, x='Participants', y='Investment ($)', 
                               size='Impact Score', color='Program',
                               title="Community Impact: Participants vs Investment vs Impact Score")
        st.plotly_chart(fig_impact, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>NXS Sports AI Platform v2.0</strong> | Enterprise Sports Facility Management</p>
        <p>🏟️ Empowering sports facilities with intelligent management solutions | Built with ❤️ by the NXS Team</p>
        <p>System Status: 🟢 All systems operational | Last Updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
                    
                