import os
import json
import pandas as pd
from typing import TypedDict, List, Dict
import dotenv   # Load environment variables from .env file if exists
import streamlit as st
from sqlalchemy import create_engine, inspect
from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# -------------------- CONFIG --------------------
dotenv.load_dotenv()  # Load environment variables from .env file if it exists
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY")

# SQLite database
DB_PATH = "testdata.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# -------------------- STATE SCHEMA --------------------
class AppState(TypedDict):
    messages: List[str]
    generated_data: List[Dict]

# -------------------- LLM SETUP --------------------
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.2)

system_prompt = """
You are a data generator. Generate realistic e-commerce order data in JSON format.
Return ONLY a JSON array with objects containing:
customer_id, order_id, product_name, category, price, quantity, date, state, city, payment_method.
Example:
[
 {"customer_id": "IND1001", "order_id": "ORD1001", "product_name": "Kurta", "category": "Clothing", "price":1200,
  "quantity":2, "date":"2024-03-08", "state":"Maharashtra", "city":"Mumbai", "payment_method":"Credit Card"}
]
Generate exactly 10 records.
"""

# -------------------- NODES --------------------
def synthesize_data(state: AppState) -> AppState:
    """Generate synthetic data using LLM"""
    user_msg = state["messages"][-1] if state["messages"] else "Generate synthetic data"
    response = llm([SystemMessage(content=system_prompt), HumanMessage(content=user_msg)])
    
    try:
        data = json.loads(response.content)
        if isinstance(data, dict):
            data = [data]
    except json.JSONDecodeError:
        st.error("AI did not return valid JSON structured data.")
        data = []
    
    return {"messages": state["messages"], "generated_data": data}

def manage_db(state: AppState) -> AppState:
    """Store generated data in SQLite database"""
    data = state.get("generated_data", [])
    if not data:
        st.warning("No data to store in DB")
        return state

    df = pd.DataFrame(data)

    # Create table name based on current count
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    table_number = len(existing_tables) + 1
    table_name = f"table_{table_number}"

    # Store data
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    st.success(f"✅ Stored {len(df)} records in table: {table_name}")
    return state

# -------------------- LANGGRAPH SETUP --------------------
graph = StateGraph(state_schema=AppState)
graph.add_node("synthesize", synthesize_data)
graph.add_node("store", manage_db)
graph.set_entry_point("synthesize")
graph.add_edge("synthesize", "store")
compiled_graph = graph.compile()

# -------------------- STREAMLIT UI --------------------
st.title("🧪 Test Data Creator - Phase 2 (LangGraph)")

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.text_input("Enter your request (e.g., 'Generate 10 orders for March 2024'):")

if st.button("Generate & Store"):
    if prompt:
        st.session_state.messages.append(prompt)
        inputs = {"messages": st.session_state.messages, "generated_data": []}
        output = compiled_graph.invoke(inputs)

        generated_data = output.get("generated_data", [])
        if generated_data:
            st.subheader("Generated Data")
            st.dataframe(pd.DataFrame(generated_data))

# Show existing tables
st.subheader("Existing Tables in DB")
inspector = inspect(engine)
tables = inspector.get_table_names()
st.write(tables)
