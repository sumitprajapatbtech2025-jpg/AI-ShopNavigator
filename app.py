import streamlit as st
from groq import Groq
import json

# PAGE CONFIG
st.set_page_config(
    page_title="AI Product Description Generator",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# GALAXY CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@300;400&display=swap');
.stApp {
    background: radial-gradient(ellipse at 20% 20%, #0d0221 0%, #000000 70%) !important;
    font-family: 'DM Mono', monospace;
}
.stApp::before {
    content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 15% 25%, rgba(124,58,237,0.12), transparent 45%),
        radial-gradient(circle at 80% 70%, rgba(37,99,235,0.10), transparent 45%),
        radial-gradient(circle at 50% 5%, rgba(236,72,153,0.06), transparent 55%);
    filter: blur(80px); z-index: -2; pointer-events: none;
}
.stApp::after {
    content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background-image:
        radial-gradient(1px 1px at 10vw 10vh, #fff, transparent),
        radial-gradient(1px 1px at 25vw 35vh, #a78bfa, transparent),
        radial-gradient(2px 2px at 45vw 20vh, #fff, transparent),
        radial-gradient(1px 1px at 65vw 50vh, #fff, transparent),
        radial-gradient(1px 1px at 85vw 10vh, #60a5fa, transparent),
        radial-gradient(1px 1px at 15vw 75vh, #fff, transparent),
        radial-gradient(2px 2px at 35vw 90vh, #fff, transparent),
        radial-gradient(1px 1px at 55vw 65vh, #a78bfa, transparent),
        radial-gradient(2px 2px at 75vw 85vh, #fff, transparent),
        radial-gradient(1px 1px at 92vw 45vh, #fff, transparent),
        radial-gradient(2px 2px at 40vw 80vh, #60a5fa, transparent),
        radial-gradient(3px 3px at 20vw 12vh, #fff, transparent),
        radial-gradient(2px 2px at 88vw 22vh, #fff, transparent),
        radial-gradient(2px 2px at 66vw 77vh, #60a5fa, transparent),
        radial-gradient(2px 2px at 80vw 60vh, #fff, transparent);
    z-index: -1; pointer-events: none;
    animation: twinkle 6s ease-in-out infinite alternate;
}
@keyframes twinkle { 0% { opacity: 0.5; } 100% { opacity: 1.0; } }
.block-container {
    background: rgba(8,8,20,0.65) !important; backdrop-filter: blur(40px) !important;
    border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 28px !important;
    padding: 2.5rem 3rem !important; box-shadow: 0 0 80px rgba(124,58,237,0.07) !important;
}
.main-title {
    font-family: 'Playfair Display', serif; font-size: clamp(1.8rem, 4vw, 3rem);
    font-weight: 900; text-align: center;
    background: linear-gradient(135deg, #f8fafc 0%, #c4b5fd 50%, #60a5fa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 1px; margin-bottom: 8px;
}
.sub-title {
    text-align: center; color: #475569; font-family: 'DM Mono', monospace;
    font-size: 10px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 40px;
}
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 13px !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: rgba(124,58,237,0.6) !important; box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
}
label, .stSelectbox label {
    color: #64748b !important; font-family: 'DM Mono', monospace !important;
    font-size: 11px !important; letter-spacing: 1.5px !important; text-transform: uppercase !important;
}
.stButton > button {
    width: 100%; background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
    color: white !important; border: none !important; border-radius: 14px !important;
    padding: 16px !important; font-family: 'Playfair Display', serif !important;
    font-size: 16px !important; font-weight: 700 !important; letter-spacing: 1px !important;
    transition: all 0.3s !important; box-shadow: 0 0 40px rgba(124,58,237,0.35) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 0 60px rgba(124,58,237,0.55) !important; }
.tagline-banner {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(37,99,235,0.15));
    border: 1px solid rgba(139,92,246,0.3); border-radius: 18px;
    padding: 24px; text-align: center; margin-bottom: 24px;
}
.section-label { color: #7c3aed; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px; }
.description-text { color: #cbd5e1; font-family: 'Georgia', serif; font-size: 15px; line-height: 1.9; }
.usp-item { display: flex; align-items: flex-start; gap: 14px; padding: 14px 0; border-bottom: 1px solid rgba(255,255,255,0.05); color: #e2e8f0; font-size: 14px; line-height: 1.6; }
.score-bar-wrap { margin-bottom: 18px; }
.badge { display: inline-block; padding: 3px 12px; border-radius: 99px; background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.35); color: #c4b5fd; font-size: 11px; font-family: 'DM Mono', monospace; margin-right: 6px; }
.cta-btn { display: inline-block; background: linear-gradient(135deg, #7c3aed, #2563eb); color: white; padding: 12px 32px; border-radius: 99px; font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; box-shadow: 0 0 30px rgba(124,58,237,0.3); }
.price-tag { display: inline-block; background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.3); color: #fbbf24; padding: 6px 20px; border-radius: 99px; font-family: 'DM Mono', monospace; font-size: 15px; margin-top: 10px; }
.footer-text { text-align: center; color: #1e293b; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 3px; margin-top: 40px; }
section[data-testid="stSidebar"] { background: rgba(5,5,15,0.95) !important; border-right: 1px solid rgba(255,255,255,0.06) !important; }
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
.stAlert { border-radius: 12px !important; font-family: 'DM Mono', monospace !important; font-size: 13px !important; }
hr { border-color: rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-title">✦ Product Description Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">◆ Neural Copy Engine • Powered by Groq AI ◆</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════
#   YAHAN APNI GROQ API KEY DAALO  ↓↓↓
# ══════════════════════════════════════════════════
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# ══════════════════════════════════════════════════

# SIDEBAR
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.success("🔑 Groq API — 100% Free, No Quota!")
    st.divider()
    tone     = st.selectbox("🎨 Brand Tone", ["Luxury", "Professional", "Casual", "Futuristic", "Bold", "Minimalist"])
    audience = st.selectbox("🎯 Target Audience", ["General", "Professionals", "Tech Enthusiasts", "Kids", "Entrepreneurs", "Gen Z"])
    language = st.selectbox("🌐 Output Language", ["English", "Hindi", "Hinglish"])
    st.divider()
    # --- YAHAN NAYA SHOPPING SELECTION ADD KIYA HAI ---
    st.markdown("### 🛒 Shopping Platform")
    platform = st.radio("Select Platform", ["Amazon", "Flipkart", "Google Search"])
    st.divider()
    st.markdown("**v4.0** • Galaxy UI • Groq Engine")

# INPUT FORM
st.markdown("#### 📦 Product Details")
col1, col2 = st.columns(2)
with col1:
    product = st.text_input("Product Name *", placeholder="e.g. iPhone 16 Pro, Maruti 800")
    brand   = st.text_input("Brand Name",     placeholder="e.g. Apple, Samsung")
with col2:
    price        = st.text_input("Price (optional)", placeholder="e.g. ₹79,999 / $999")
    raw_features = st.text_area("Key Features * (one per line)", placeholder="AMOLED Display\n200MP Camera\n5000mAh Battery", height=120)


def generate_description(brand, product, price, features, tone, audience, language):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""You are an elite AI copywriter. Generate a premium product description in JSON format.
Return ONLY valid JSON — no markdown fences, no extra text.

JSON structure:
{{
  "tagline": "Short punchy tagline (max 10 words)",
  "emoji_summary": "3-5 relevant emojis",
  "description": "3-paragraph description separated by \\n\\n. Tone: {tone}. Audience: {audience}. Language: {language}.",
  "usp": ["unique selling point 1", "unique selling point 2", "unique selling point 3"],
  "score": {{"design": 4, "performance": 5, "value": 4, "innovation": 4}},
  "cta": "Call to action (max 5 words)"
}}

Brand: {brand or 'Unknown'}
Product: {product}
Price: {price or 'Not specified'}
Features:
{features}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.7,
    )
    raw = response.choices[0].message.content.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]
    return json.loads(raw.strip())


# GENERATE BUTTON
st.markdown("<br>", unsafe_allow_html=True)
if st.button("✦ Generate Premium Description"):
    if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
        st.error("⚠️ Pehle app.py mein GROQ_API_KEY daalo!")
    elif not product.strip():
        st.error("⚠️ Product name is required.")
    elif not raw_features.strip():
        st.error("⚠️ Please enter at least one feature.")
    else:
        with st.spinner("🌌 Neural Engine Processing..."):
            try:
                # --- SMART LINK LOGIC ---
                search_query = product.replace(" ", "+")
                if platform == "Amazon":
                    final_url = f"https://www.amazon.in/s?k={search_query}"
                elif platform == "Flipkart":
                    final_url = f"https://www.flipkart.com/search?q={search_query}"
                else:
                    final_url = f"https://www.google.com/search?q={search_query}"

                result       = generate_description(brand, product, price, raw_features, tone, audience, language)
                score        = result.get("score", {})
                usp_list     = result.get("usp", [])
                score_colors = {"design": "#a78bfa", "performance": "#34d399", "value": "#fbbf24", "innovation": "#60a5fa"}

                st.markdown(f"""
                <div class="tagline-banner">
                    <div style="font-size:32px;margin-bottom:10px;">{result.get('emoji_summary','✨')}</div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#e2e8f0;font-style:italic;font-weight:700;">
                        "{result.get('tagline','')}"
                    </div>
                    {'<div class="price-tag">' + price + '</div>' if price else ''}
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f'<div style="margin-bottom:20px;"><span class="badge">{tone}</span><span class="badge">{audience}</span><span class="badge">{language}</span></div>', unsafe_allow_html=True)

                tab1, tab2, tab3 = st.tabs(["📝 Description", "🔥 USPs", "📊 Scores"])

                with tab1:
                    st.markdown('<div class="section-label">Product Description</div>', unsafe_allow_html=True)
                    for para in result.get("description", "").split("\n\n"):
                        st.markdown(f'<p class="description-text">{para}</p>', unsafe_allow_html=True)
                    
                    # --- CLICKABLE SMART LINK BUTTON ---
                    st.markdown(f'''
                        <div style="text-align:center; margin-top:28px;">
                            <a href="{final_url}" target="_blank" style="text-decoration: none;">
                                <span class="cta-btn">Buy {product} on {platform} →</span>
                            </a>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    with st.expander("📋 Copy Raw Text"):
                        st.code(result.get("description", ""), language=None)

                with tab2:
                    st.markdown('<div class="section-label">Unique Selling Points</div>', unsafe_allow_html=True)
                    for i, point in enumerate(usp_list, 1):
                        st.markdown(f'<div class="usp-item"><div style="width:28px;height:28px;border-radius:8px;flex-shrink:0;background:linear-gradient(135deg,#7c3aed,#2563eb);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:13px;">{i}</div><div>{point}</div></div>', unsafe_allow_html=True)

                with tab3:
                    st.markdown('<div class="section-label">Score Analysis</div>', unsafe_allow_html=True)
                    for key, val in score.items():
                        color = score_colors.get(key, "#a78bfa")
                        pct   = int((val / 5) * 100)
                        stars = "★" * val + "☆" * (5 - val)
                        st.markdown(f'<div class="score-bar-wrap"><div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:13px;"><span style="color:#94a3b8;text-transform:capitalize;">{key}</span><span style="color:{color};">{stars} {val}/5</span></div><div style="height:6px;border-radius:99px;background:rgba(255,255,255,0.06);"><div style="height:100%;border-radius:99px;width:{pct}%;background:linear-gradient(90deg,{color},{color}88);"></div></div></div>', unsafe_allow_html=True)

                    avg = sum(score.values()) / len(score) if score else 0
                    st.markdown(f'<div style="margin-top:24px;padding:20px;text-align:center;background:rgba(139,92,246,0.08);border-radius:14px;border:1px solid rgba(139,92,246,0.2);"><div style="color:#64748b;font-size:11px;letter-spacing:2px;font-family:\'DM Mono\',monospace;">OVERALL SCORE</div><div style="font-family:\'Playfair Display\',serif;font-size:42px;font-weight:900;background:linear-gradient(135deg,#c4b5fd,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{avg:.1f}<span style="font-size:20px;">/5</span></div></div>', unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("❌ AI ne invalid response diya. Dobara try karein.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# FOOTER
st.divider()
st.markdown('<div class="footer-text">◆ NEURAL COPY ENGINE v4.0 • POWERED BY GROQ AI ◆</div>', unsafe_allow_html=True)