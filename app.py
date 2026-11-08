import streamlit as st
from dotenv import load_dotenv
from nyayaai.engine import analyze, complaint_draft
load_dotenv()
st.set_page_config(page_title="NyayaAI",page_icon="⚖️",layout="wide")
st.title("NyayaAI")
st.caption("A focused assistant for online-purchase refunds that have not arrived")
st.info("MVP scope: Indian consumer refund grievances; English text input. Not a substitute for an advocate.")
st.warning("Do not enter passwords, full card numbers, Aadhaar numbers, or unnecessary sensitive information. This demo does not intentionally store case data.")
st.subheader("1. Describe what happened")
narrative=st.text_area("Explain the purchase, cancellation/return, refund request, and responses",height=140,placeholder="I ordered ... I returned/cancelled ... The platform said ...")
with st.expander("Add details",expanded=True):
    a,b=st.columns(2)
    with a:
        seller=st.text_input("Seller/platform"); order_id=st.text_input("Order/booking ID"); purchase_date=st.text_input("Purchase date"); refund_requested_date=st.text_input("Refund request date")
    with b:
        amount=st.text_input("Amount paid/refund due"); refund_reason=st.text_input("Reason for refund"); payment_method=st.selectbox("Payment method",["Not specified","UPI","Card","Net banking","Wallet","Cash on delivery","Other"]); state=st.text_input("State/UT")
facts={"seller":seller,"order_id":order_id,"purchase_date":purchase_date,"refund_requested_date":refund_requested_date,"amount":amount,"refund_reason":refund_reason,"payment_method":payment_method,"state":state}
if st.button("Analyse my case",type="primary",disabled=not narrative.strip()):
    st.session_state.result=analyze(narrative,facts); st.session_state.facts=facts; st.session_state.narrative=narrative
if "result" in st.session_state:
    r=st.session_state.result; f=st.session_state.facts
    st.divider(); st.subheader("2. Preliminary case summary"); st.write(r["summary"]); st.caption(r["model_status"])
    c1,c2=st.columns(2)
    with c1:
        st.markdown("**Timeline / facts captured**")

        for item in r["timeline"]:
            if isinstance(item, dict):
                event = item.get("event", "Unknown event")
                date = item.get("date", "Date unknown")

                st.markdown(f"**{event}**")
                st.caption(f"Date: {date}")

            else:
                st.write("•", item)
        st.markdown("**Information still needed**")

        for item in r["missing_facts"]:
            if isinstance(item, dict):
                st.write("•", item.get("field", str(item)))
            else:
                st.write("•", item)

        if not r["missing_facts"]:
            st.write("No missing structured fields detected. Verify all details.")
    with c2:
        st.markdown("**Evidence to preserve**")
        for x in r["evidence"]: st.write("• ",x)
        st.markdown("**Suggested next steps**")
        for x in r["next_steps"]: st.write("• ",x)
    st.divider(); st.subheader("3. Draft a message to the seller/platform")
    name=st.text_input("Your name"); address=st.text_input("City/state or address to include")
    issue=st.text_area("Issue description",value=st.session_state.narrative,height=90)
    requested=st.text_area("Outcome requested",value=f"Please process the pending refund of {f.get('amount') or '[amount]'} and confirm the expected credit date.")
    draft=complaint_draft(name,address,f,issue,requested)
    st.text_area("Editable draft",value=draft,height=300)
    st.download_button("Download draft (.txt)",draft,file_name="nyayaai_complaint_draft.txt")
    st.divider(); st.subheader("4. Official guidance and sources")
    for item in r["official_guidance"]: st.write("• ",item)
    for src in r["legal_sources"]: st.markdown(f"- [{src['title']}]({src['url']})")
    st.warning(r["disclaimer"])
st.divider()
st.caption("Limitations: English text only; no voice, OCR, document verification, court/forum selection, filing, or legal representation. Outputs require user review.")
