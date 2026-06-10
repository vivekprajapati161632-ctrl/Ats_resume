import streamlit as st
import os
from utils import init_workspace
from resume_parser import parse_resume
from resume_optimizer import analyze_ats_matching, optimize_resume, generate_docx_resume, generate_pdf_resume

def main():
    st.set_page_config(page_title="ATS Resume Optimizer", page_icon="🚀", layout="wide")
    init_workspace()
    
    st.title("🚀 Custom ATS AI Resume Optimization Studio")
    st.markdown("Free Tier Gemini 2.5 Flash Parsing & Optimization Framework Engine")
    st.markdown("---")
    
    with st.sidebar:
        st.header("⚙️ API Configuration")
        gemini_key = st.text_input("Gemini Secure API Key:", type="password", placeholder="AIzaSy...")
        if gemini_key:
            os.environ["GEMINI_API_KEY"] = gemini_key
            st.success("Gemini Engine Lock Success!")
        else:
            st.warning("Supply a valid Gemini API Key from Google AI Studio to unlock.")
            
        st.markdown("---")
        st.header("📂 Data Loading Desk")
        uploaded_file = st.file_uploader("Upload Existing Resume (PDF/DOCX):", type=["pdf", "docx"])

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Position Target Specification")
        jd_text = st.text_area("Paste Targeted Job Description (JD):", height=260, placeholder="Paste requirements directly from LinkedIn or Naukri...")
        run_engine = st.button("✨ Run Optimization Engine Pipeline", type="primary")

    with col2:
        st.header("📊 Analytical Metrics Reporting")
        
        if run_engine:
            if not gemini_key:
                st.error("Authentication Error: Specify your Gemini API Key in the Sidebar first.")
                return
            if not uploaded_file or not jd_text.strip():
                st.error("Validation Error: Please load both a file stream and a target description block.")
                return
                
            temp_input_path = os.path.join("output", uploaded_file.name)
            with open(temp_input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            progress_bar = st.progress(10)
            
            try:
                st.write("⏳ Phase 1: Scanning file contexts and isolating metadata metrics...")
                parsed_resume = parse_resume(temp_input_path)
                progress_bar.progress(40)
                
                st.write("⏳ Phase 2: Running semantic keyword comparison modeling vector check...")
                diagnostics = analyze_ats_matching(parsed_resume, jd_text)
                progress_bar.progress(70)
                
                st.write("⏳ Phase 3: Rewriting history bullets structure natively...")
                optimized_resume = optimize_resume(parsed_resume, jd_text, diagnostics)
                
                docx_out = "output/optimized_resume.docx"
                pdf_out = "output/optimized_resume.pdf"
                
                generate_docx_resume(optimized_resume, docx_out)
                generate_pdf_resume(optimized_resume, pdf_out)
                
                progress_bar.progress(100)
                st.success("🎉 Full Matching Pipeline Complete!")
                
                # Render Metrics Interface Cards
                c1, c2 = st.columns(2)
                c1.metric("ATS Scoring Level", f"{diagnostics['ats_score']}/100")
                c2.metric("Vector Keywords Match Ratio", f"{diagnostics['match_percentage']}%")
                
                st.write(f"**Missing Tools Detected:** {', '.join(diagnostics['missing_keywords'][:6])}")
                
                st.markdown("### 📝 Tailored Summary Output Preview")
                st.info(optimized_resume.get("summary"))
                
                # Dynamic Download Blocks Trigger
                st.markdown("### 📥 Download Production Assets")
                with open(docx_out, "rb") as f1:
                    st.download_button("Download ATS Resume (DOCX)", data=f1.read(), file_name="optimized_resume.docx")
                with open(pdf_out, "rb") as f2:
                    st.download_button("Download ATS Resume (PDF)", data=f2.read(), file_name="optimized_resume.pdf")
                    
            except Exception as pipeline_err:
                st.error(f"🚨 Pipeline Framework Process Crash: {str(pipeline_err)}")
            finally:
                if os.path.exists(temp_input_path):
                    os.remove(temp_input_path)

if __name__ == "__main__":
    main()
