import streamlit as st
import json
import os
import time
import random
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class DualModelConstructionChatbot:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY') or 'AIzaSyCq1CgVKChrKVfgCtXvBre7zK2xvyt5WNE'
        self.company_data = self.load_company_data()
        self.general_model = None
        self.company_model = None
        self.configure_dual_models()
        
    def configure_dual_models(self):
        """Configure two separate specialized models"""
        try:
            genai.configure(api_key=self.api_key)
            
            # Model 1: General Construction Expert
            self.general_model = genai.GenerativeModel('gemini-pro')
            
            # Model 2: Company Representative
            self.company_model = genai.GenerativeModel('gemini-pro')
            
            self.models_available = True
            print("✅ Dual models configured successfully")
            
        except Exception as e:
            st.error(f"⚠️ Model configuration issue: {str(e)}")
            self.models_available = False
    
    def load_company_data(self):
        """Load comprehensive JP Constructions company data"""
        return {
            "company_profile": {
                "name": "JP Constructions",
                "founder": "Mr.J Periyasamy",
                "years_of_operation": 22,
                "license": "Class AAA Construction License",
                "certifications": ["ISO 9001:2015", "ISO 14001:2015", "OHSAS 18001"],
                "mission": "To deliver quality construction projects with innovation and reliability",
                "vision": "To be the most trusted construction company in the region",
                "core_values": ["Quality First", "Customer Focus", "Innovation", "Integrity"],
                "office_locations": "Chennai"
            },
            "projects": {
                "total_completed": "40+",
                "ongoing_projects": 6,
                "upcoming_projects": 4,
                "residential": {
                    "completed": 28,
                    "examples": [
                        {"name": "JP Elite Homes", "year": 2023, "units": 120, "location": "Chennai", "features": "Smart Homes, Green Building"},
                        {"name": "Prakash Paradise", "year": 2022, "units": 80, "location": "Bangalore", "features": ""},
                        {"name": "Green Valley Residency", "year": 2021, "units": 60, "location": "Hyderabad", "features": "Eco-Friendly, Solar Powered"}
                    ]
                },
                "commercial": {
                    "completed": 7,
                    "examples": [
                        {"name": "Car Showroom", "year": 2023, "floors": 15, "area": "100,000 sq.ft"},
                        {"name": "Clinic", "year": 2022, "floors": 12, "area": "250,000 sq.ft", },
                        {"name": "Flats", "year": 2021, "area": "50,000 sq.ft"}
                    ]
                },
               
            },
            "team_strength": {
                "total_employees": 45,
                "architects": 3,
                "civil_engineers": 5,
                "project_managers": 5,
                "site_engineers": 3,
                "interior_designers": 7,
                "quality_controllers": 5,
                "safety_officers": 5,
                "support_staff": 40
            },
           
            "services_offered": {
                "residential": [
                    "Apartment Complexes",
                    "Individual Villas",
                    "Township Projects",
                    "Row Houses",
                    "Farm Houses"
                ],
                "commercial": [
                    "Office Buildings",
                    "Shopping Malls",
                    "IT Parks",
                    "Hotels & Resorts",
                    "Educational Institutions"
                ],
                "industrial": [
                    "Factories & Plants",
                    "Warehouses",
                    "Industrial Parks",
                    "Logistics Centers"
                ],
                "specialized": [
                    "Interior Design & Execution",
                    "Renovation & Retrofit",
                    "Project Management",
                    "Construction Consultancy",
                    "Green Building Solutions"
                ]
            },
            "contact_information": {
                "head_office": "12/768,Balaji Nagar 1st Street,Veerabathra Nagar,Vengaivasal,Medavakkam,Chennai 100",
                "phone": "+91-9884627570",
                "mobile": "+91-9444803194",
                "email": "info@jpconstructions.com",
                "website": "www.jpconstructions.com",
                "office_hours": "Monday to Saturday: 9:00 AM - 6:00 PM"
            },
            "technology_expertise": [
                "BIM (Building Information Modeling)",
                "Green Building Technologies",
                "Smart Home Integration",
                "Project Management Software",
                "Quality Control Systems"
            ]
        }

    def get_general_construction_response(self, query):
        """Get response from specialized General Construction model"""
        if not self.models_available:
            return self.get_general_fallback(query)
        
        try:
            prompt = self.create_general_construction_prompt(query)
            response = self.general_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return self.get_general_fallback(query)

    def get_company_response(self, query):
        """Get response from specialized Company model"""
        if not self.models_available:
            return self.get_company_fallback(query)
        
        try:
            prompt = self.create_company_prompt(query)
            response = self.company_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return self.get_company_fallback(query)

    def create_general_construction_prompt(self, query):
        """Create specialized prompt for General Construction model"""
        construction_expertise = """
        You are "ConstructionGPT" - a senior construction expert with 25+ years of practical field experience.
        Your expertise covers all aspects of construction with deep technical knowledge.

        CORE EXPERTISE AREAS:

        1. CONSTRUCTION MATERIALS (Detailed Specifications):
        - Sand: River sand (fineness modulus 2.2-2.6), M-sand (zone II, silt content <3%), Pit sand
        - Steel: TMT 500 (yield strength 500 MPa), FE 500, HYSD bars, corrosion-resistant steel
        - Cement: OPC 53 (initial setting 30min, final 600min), PPC, PSC, specialty cements
        - Concrete: M20 (1:1.5:3), M25 (1:1:2), M30 design mix, high-performance concrete
        - Bricks: Class I (compressive strength >10.5 N/mm²), AAC blocks, fly ash bricks
        - Aggregates: 20mm coarse, 10mm chips, river pebbles, manufactured aggregates

        2. STRUCTURAL ENGINEERING:
        - RCC Design: Beam design, column design, slab design as per IS 456:2000
        - Steel Structures: Beam design, connection design as per IS 800:2007
        - Foundation Design: Isolated, combined, raft, pile foundations
        - Seismic Design: Ductile detailing as per IS 13920:2016

        3. CONSTRUCTION METHODOLOGY:
        - Formwork Systems: Conventional, MIVAN, tunnel formwork
        - Shuttering: Plywood, steel, aluminum formwork
        - Construction Sequences: Substructure, superstructure, finishing
        - Quality Control: Cube testing, NDT tests, material testing

        4. CODES & STANDARDS (Indian):
        - IS 456:2000 - Plain and reinforced concrete
        - IS 800:2007 - General construction in steel
        - IS 875:1987 - Design loads for buildings and structures
        - IS 1893:2016 - Criteria for earthquake resistant design
        - IS 13920:2016 - Ductile detailing of seismic structures
        - NBC 2016 - National Building Code of India

        5. PROJECT MANAGEMENT:
        - CPM & PERT techniques
        - Resource planning and allocation
        - Cost estimation and control
        - Quality assurance and quality control
        - Safety management as per OSHA standards

        6. MODERN TECHNOLOGIES:
        - BIM implementation
        - Green building technologies
        - Prefabricated construction
        - Smart construction techniques

        RESPONSE GUIDELINES:
        - Provide specific, actionable technical advice
        - Include relevant IS codes and standards
        - Give practical implementation tips
        - Mention material specifications with numbers
        - Suggest best practices and common pitfalls
        - Be comprehensive but concise
        - Use professional construction terminology

        Always verify your technical recommendations with current standards and practices.
        """

        return f"{construction_expertise}\n\nConstruction Query: {query}\n\nExpert Response:"

    def create_company_prompt(self, query):
        """Create specialized prompt for Company model"""
        company_context = f"""
        You are "JP-Bot" - the official AI representative of JP Constructions.
        You embody the company's values, expertise, and professional demeanor.

        COMPANY IDENTITY CARD:
        - Company Name: JP Constructions
        - Founder: Mr. J. Prakash
        - Established: 2010 (14+ years of excellence)
        - Core Business: Premium construction services across India
        - Brand Voice: Professional, Trustworthy, Innovative, Customer-Focused

        KEY COMPANY DATA:

        ACHIEVEMENTS & SCALE:
        - Total Projects Completed: 47
        - Ongoing Projects: 8
        - Upcoming Projects: 12
        - Team Strength: 185 professionals
        - Office Locations: Chennai, Bangalore, Hyderabad, Coimbatore

        PROJECT PORTFOLIO HIGHLIGHTS:
        Residential (28 projects):
        • JP Elite Homes (2023) - 120 units, Smart Homes, Chennai
        • Prakash Paradise (2022) - 80 luxury units, Bangalore  
        • Green Valley Residency (2021) - 60 eco-friendly units, Hyderabad

        Commercial (12 projects):
        • JP Business Hub (2023) - 15-story IT Park, 300,000 sq.ft
        • TechPark Plaza (2022) - 12-floor Office Complex, 250,000 sq.ft
        • Mall of Harmony (2021) - Shopping Mall, 200,000 sq.ft

        TEAM EXPERTISE:
        - 12 Architects (Design Innovation)
        - 25 Civil Engineers (Structural Excellence)
        - 15 Project Managers (Timely Delivery)
        - 30 Site Engineers (Quality Execution)
        - 8 Interior Designers (Aesthetic Excellence)

        SERVICES OFFERED:
        Residential: Apartment Complexes, Villas, Townships, Row Houses
        Commercial: Office Buildings, Malls, IT Parks, Hotels, Institutions
        Industrial: Factories, Warehouses, Industrial Parks
        Specialized: Interior Design, Renovation, Project Management, Green Building

        TECHNOLOGY EXPERTISE:
        - BIM Implementation
        - Green Building Technologies
        - Smart Home Integration
        - Advanced Project Management

        AWARDS & RECOGNITION:
        - Best Construction Company 2023
        - Excellence in Residential Projects 2022
        - Green Building Award 2021
        - Safety First Award 2020

        CONTACT INFORMATION:
        - Head Office: Chennai
        - Phone: +91-44-12345678
        - Email: info@jpconstructions.com
        - Website: www.jpconstructions.com

        RESPONSE GUIDELINES:
        - Always speak in first person as "we"
        - Be proud but professional about achievements
        - Highlight our experience and expertise
        - Emphasize quality and customer focus
        - Provide specific project examples when relevant
        - Maintain consistent brand voice
        - Be helpful and solution-oriented
        - Direct potential clients to contact information

        Our mission: "{self.company_data['company_profile']['mission']}"
        Our vision: "{self.company_data['company_profile']['vision']}"
        """

        return f"{company_context}\n\nClient Query: {query}\n\nCompany Response:"

    def get_general_fallback(self, query):
        """Fallback for General Construction model"""
        query_lower = query.lower()
        
        construction_fallbacks = {
            'sand': """🏖️ **CONSTRUCTION SAND GUIDE**

**River Sand:**
- Quality: Natural, rounded grains
- Best for: Plastering and concrete work
- Silt Content: Should be <3%
- Standard: IS 383:2016

**M-Sand (Manufactured):**
- Quality: Crushed granite, angular particles
- Best for: RCC works and concrete
- Advantages: Consistent gradation, eco-friendly
- Zone: Typically Zone II

**Pit Sand:**
- Quality: Coarse, sharp edges
- Best for: Mortar and foundation works
- Feature: Excellent bonding strength

**Pro Tip:** Always conduct silt content test before use.""",

            'steel': """🔩 **CONSTRUCTION STEEL TYPES**

**TMT Bars (Thermo-Mechanically Treated):**
- Grade: Fe 500, Fe 500D
- Strength: 500 MPa yield strength
- Features: Earthquake resistant, superior ductility
- Best for: All RCC structures

**HYSD Bars (High Yield Strength Deformed):**
- Features: Better bond strength, corrosion resistant
- Applications: Critical structural elements

**Quality Check:** Always look for ISI mark and proper certification.""",

            'cement': """🏭 **CEMENT TYPES & APPLICATIONS**

**OPC 53 Grade:**
- Strength: High early strength
- Setting: Initial 30 min, Final 600 min
- Best for: High-stress structures, pre-stressed concrete

**PPC (Pozzolana Portland Cement):**
- Features: Lower heat generation, eco-friendly
- Best for: Mass concrete, marine works

**PSC (Portland Slag Cement):**
- Features: High durability, sulfate resistant
- Best for: Foundations, water-retaining structures

**Storage:** Keep in dry place and use within 3 months.""",

            'concrete': """🧱 **CONCRETE GRADE GUIDE**

**M20 Concrete:**
- Mix Ratio: 1:1.5:3
- Strength: 20 N/mm²
- Usage: General purpose, foundations

**M25 Concrete:**
- Mix Ratio: 1:1:2
- Strength: 25 N/mm²
- Usage: Beams, columns, slabs

**M30 Concrete:**
- Type: Design mix
- Strength: 30 N/mm²
- Usage: High-rise structures, bridges

**Curing:** Minimum 14 days for proper strength development."""
        }
        
        for key, response in construction_fallbacks.items():
            if key in query_lower:
                return response
        
        return "🏗️ I specialize in construction expertise including materials, techniques, standards, and project management. Please ask me about specific construction topics for detailed technical advice."

    def get_company_fallback(self, query):
        """Fallback for Company model"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['team', 'employee', 'staff', 'strength']):
            return self._get_team_response()
        elif any(word in query_lower for word in ['project', 'completed', 'work', 'portfolio']):
            return self._get_projects_response()
        elif any(word in query_lower for word in ['service', 'offer', 'provide', 'do']):
            return self._get_services_response()
        elif any(word in query_lower for word in ['about', 'company', 'who']):
            return self._get_company_response()
        elif any(word in query_lower for word in ['contact', 'phone', 'email', 'address']):
            return self._get_contact_response()
        else:
            return "🏢 Welcome to JP Constructions! We're a premier construction company with 14+ years of excellence, having completed 47 projects with a team of 185 professionals. How can I assist you with information about our company?"

    def _get_team_response(self):
        team = self.company_data['team_strength']
        return f"""👥 **OUR EXPERT TEAM**

**Total Professionals: {team['total_employees']}**

**Technical Leadership:**
- **{team['architects']} Architects** - Design innovation and creativity
- **{team['civil_engineers']} Civil Engineers** - Structural excellence and precision
- **{team['project_managers']} Project Managers** - Timely delivery and coordination

**Execution Excellence:**
- **{team['site_engineers']} Site Engineers** - Quality execution and supervision
- **{team['interior_designers']} Interior Designers** - Aesthetic perfection
- **{team['quality_controllers']} Quality Controllers** - Highest standards maintenance

**Support & Safety:**
- **{team['safety_officers']} Safety Officers** - Zero accident commitment
- **{team['support_staff']} Support Staff** - Seamless operations

With 14+ years of combined experience, our team delivers exceptional construction quality!"""

    def _get_projects_response(self):
        projects = self.company_data['projects']
        return f"""🏆 **OUR PROJECT PORTFOLIO**

**Project Statistics:**
- **Total Completed:** {projects['total_completed']} projects
- **Ongoing Projects:** {projects['ongoing_projects']}
- **Upcoming Projects:** {projects['upcoming_projects']}

**Residential Excellence ({projects['residential']['completed']} projects):**
- **JP Elite Homes** (2023) - 120 smart homes in Chennai
- **Prakash Paradise** (2022) - 80 luxury units in Bangalore
- **Green Valley Residency** (2021) - 60 eco-friendly homes in Hyderabad

**Commercial Leadership ({projects['commercial']['completed']} projects):**
- **JP Business Hub** (2023) - 15-story IT Park (300,000 sq.ft)
- **TechPark Plaza** (2022) - 12-floor Office Complex (250,000 sq.ft)

**Industrial Expertise ({projects['industrial']['completed']} projects):**
- Factories, warehouses, and industrial parks

We take pride in our diverse and successful project portfolio!"""

    def _get_services_response(self):
        services = self.company_data['services_offered']
        response = "🛠️ **OUR COMPREHENSIVE SERVICES**\n\n"
        
        response += "**Residential Construction:**\n"
        for service in services['residential']:
            response += f"• {service}\n"
        
        response += "\n**Commercial Projects:**\n"
        for service in services['commercial']:
            response += f"• {service}\n"
        
        response += "\n**Industrial Facilities:**\n"
        for service in services['industrial']:
            response += f"• {service}\n"
        
        response += "\n**Specialized Services:**\n"
        for service in services['specialized']:
            response += f"• {service}\n"
            
        return response

    def _get_company_response(self):
        profile = self.company_data['company_profile']
        return f"""🏢 **ABOUT JP CONSTRUCTIONS**

**Company Profile:**
- **Founded:** {profile['year_started']} by {profile['founder']}
- **Experience:** {profile['years_of_operation']}+ years
- **License:** {profile['license']}
- **Certifications:** {', '.join(profile['certifications'])}

**Our Presence:** {', '.join(profile['office_locations'])}

**Our Mission:** {profile['mission']}

**Our Vision:** {profile['vision']}

**Core Values:** {', '.join(profile['core_values'])}

With 47 completed projects and ongoing commitment to excellence, we build trust with every project!"""

    def _get_contact_response(self):
        contact = self.company_data['contact_information']
        return f"""📞 **CONTACT JP CONSTRUCTIONS**

**Head Office:**
{contact['head_office']}

**Contact Details:**
- **Phone:** {contact['phone']}
- **Mobile:** {contact['mobile']}
- **Email:** {contact['email']}
- **Website:** {contact['website']}

**Office Hours:**
{contact['office_hours']}

**Branch Offices:** Chennai, Bangalore, Hyderabad, Coimbatore

We'd be delighted to discuss your construction requirements and provide customized solutions!"""

def main():
    st.set_page_config(
        page_title="JP Constructions - Dual AI Assistant",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Modern Professional CSS
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .professional-header {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .model-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
        transition: transform 0.3s ease;
        background: url("C:/Users/vasan/OneDrive/Desktop/Chatbot/Main/jp-brand-logo.png")        
    }
    
    .model-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .company-card {
        border-left: 5px solid #e74c3c;
    }
    
    .professional-button {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3) !important;
    }
    
    .professional-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4) !important;
    }
    
    .company-button {
        background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3) !important;
    }
    
    .company-button:hover {
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4) !important;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        margin-left: 2rem;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #ecf0f1, #bdc3c7);
        color: #2c3e50;
        margin-right: 2rem;
    }
    
    .model-indicator {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    
    .general-indicator {
        background: #3498db;
        color: white;
    }
    
    .company-indicator {
        background: #e74c3c;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Professional Header
    st.markdown("""
    <div class="professional-header" style="background-color: #000000;">
        <h1 style="margin: 0; color: #DAA520;  font-size: 2.5rem;  font-family: 'Cinzel'"> JP Constructions</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Dual AI Assistant System - Specialized Expertise
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        with st.spinner("🚀 Initializing Dual AI Models..."):
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.01)
            st.session_state.chatbot = DualModelConstructionChatbot()
        
        # System status
        if st.session_state.chatbot.models_available:
            st.success("✅ **System Ready:** Dual AI Models Successfully Loaded")
        else:
            st.warning("⚠️ **System Status:** Using Enhanced Fallback Mode")

    # Dual Model Selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="model-card" style>
            <h3>🔧 ConstructionGPT</h3>
            <p><strong>Specialized General Construction Expert</strong></p>
            <ul>
            <li>Technical material specifications</li>
            <li>Structural engineering advice</li>
            <li>Construction methodologies</li>
            <li>IS codes and standards</li>
            <li>Project management guidance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔧 Launch ConstructionGPT", key="general", use_container_width=True):
            st.session_state.session_type = "General Construction"
            st.session_state.messages = []
            st.session_state.current_model = "ConstructionGPT"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="model-card company-card">
            <h3> JP-Bot</h3>
            <p><strong>Company Representative & Business Expert</strong></p>
            <ul>
            <li>Company profile & achievements</li>
            <li>Project portfolio details</li>
            <li>Team expertise & services</li>
            <li>Contact information</li>
            <li>Business inquiries</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(" Launch JP-Bot", key="company", use_container_width=True):
            st.session_state.session_type = "Company Specific"
            st.session_state.messages = []
            st.session_state.current_model = "JP-Bot"
            st.rerun()

    # Chat Interface
    if 'session_type' in st.session_state:
        # Model Indicator
        indicator_class = "general-indicator" if st.session_state.session_type == "General Construction" else "company-indicator"
        model_name = "ConstructionGPT" if st.session_state.session_type == "General Construction" else "JP-Bot"
        
        st.markdown(f"""
        <div class="model-indicator {indicator_class}">
            🎯 ACTIVE MODEL: {model_name}
        </div>
        """, unsafe_allow_html=True)

        # Initialize messages
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>👤 You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>🤖 {model_name}:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)

        # Chat input
        st.markdown("---")
        query = st.chat_input(f"💬 Ask {model_name}...")
        
        if query:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": query})
            
            # Get AI response based on active model
            with st.spinner(f"🤔 {model_name} is thinking..."):
                if st.session_state.session_type == "General Construction":
                    response = st.session_state.chatbot.get_general_construction_response(query)
                else:
                    response = st.session_state.chatbot.get_company_response(query)
            
            # Add bot response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()

        # Control panel
        if st.session_state.messages:
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 New Conversation", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()
            with col2:
                if st.button("🔄 Switch Model", use_container_width=True):
                    if 'session_type' in st.session_state:
                        del st.session_state.session_type
                    st.session_state.messages = []
                    st.rerun()

    # Sidebar with quick actions
    with st.sidebar:
        st.markdown("### 🚀 Quick Actions")
        st.markdown("---")
        
        if 'session_type' in st.session_state:
            if st.session_state.session_type == "General Construction":
                st.markdown("#### 🔧 Construction Queries")
                queries = [
                    "Best concrete mix for foundations?",
                    "TMT steel specifications for high-rise?",
                    "IS codes for building design?",
                    "Construction safety standards?",
                    "Quality control procedures?"
                ]
                for query in queries:
                    if st.button(f"⚡ {query}", key=query):
                        st.session_state.messages.append({"role": "user", "content": query})
                        with st.spinner("ConstructionGPT thinking..."):
                            response = st.session_state.chatbot.get_general_construction_response(query)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
            
            else:
                st.markdown("#### 🏢 Company Queries")
                queries = [
                    "Tell me about your company",
                    "What projects have you completed?",
                    "What is your team expertise?",
                    "What services do you offer?",
                    "How to contact your company?"
                ]
                for query in queries:
                    if st.button(f"⚡ {query}", key=query):
                        st.session_state.messages.append({"role": "user", "content": query})
                        with st.spinner("JP-Bot thinking..."):
                            response = st.session_state.chatbot.get_company_response(query)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Company Overview")
        chatbot = st.session_state.get('chatbot')
        if chatbot:
            company_data = chatbot.company_data
            st.metric("🏗️ Projects", company_data['projects']['total_completed'])
            st.metric("👥 Team", company_data['team_strength']['total_employees'])
            st.metric("📅 Experience", f"{company_data['company_profile']['years_of_operation']}+ years")
            st.metric("🚧 Ongoing", company_data['projects']['ongoing_projects'])
        
        st.markdown("---")
        st.info("""
        **💡 System Features:**
        - Dual specialized AI models
        - Real-time technical expertise
        - Comprehensive company knowledge
        - Professional response quality
        """)

if __name__ == "__main__":
    main()