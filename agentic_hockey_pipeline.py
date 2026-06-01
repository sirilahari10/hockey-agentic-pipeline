import pandas as pd
import numpy as np


# 1. BRONZE LAYER: RAW PLAY-BY-PLAY DATA
def ingest_raw_hockey_data():
    print("[INFO] Ingesting raw NHL Play-by-Play & Shift data...")
    data = [
        {"game_id": "2025020001", "period": 3, "time": "14:22", "event": "SHOT", "player_id": 87, "x_coord": 65, "y_coord": -5, "shift_length_sec": 45},
        {"game_id": "2025020001", "period": 2, "time": "08:15", "event": "GIVEAWAY", "player_id": 58, "x_coord": -80, "y_coord": 20, "shift_length_sec": 70},
        {"game_id": "2025020001", "period": 1, "time": "19:55", "event": "HIT", "player_id": 71, "x_coord": 40, "y_coord": 35, "shift_length_sec": 30},
    ]
    return pd.DataFrame(data)

# 2. SILVER/GOLD LAYER: dbt SIMULATION

def run_dbt_transformations(df):
    print("[INFO] Executing dbt transformations (Cleaning & Aggregating)...")
    
    df['dist_to_net'] = np.sqrt((89 - np.abs(df['x_coord']))**2 + (0 - df['y_coord'])**2)
    
    df['xG'] = np.where(df['event'] == 'SHOT', np.maximum(0, 0.2 - (df['dist_to_net'] * 0.005)), 0)
    
    df['is_high_danger'] = df['xG'] > 0.08
    df['is_fatigued'] = df['shift_length_sec'] > 60
    
    return df

# 3. AGENTIC AI WORKFLOW
def agentic_coaching_assistant(row):
    """
    Simulates an LLM 'Agent' querying the Gold data warehouse to 
    provide actionable, natural-language insights to the coaching staff.
    """
    if row['event'] == 'SHOT' and row['is_high_danger']:
        return f"High-danger shot attempt (xG: {row['xG']:.2f}) generated after {row['shift_length_sec']}-second shift. Exceptional endurance metric flagged."
    
    if row['event'] == 'GIVEAWAY' and row['is_fatigued']:
        return f"Defensive zone giveaway. Shift duration exceeded 65 seconds ({row['shift_length_sec']}s). Agent flags potential fatigue-related breakdown for video room."
        
    return None

def execute_agent(df):
    print("[INFO] Initializing Coaching Assistant AI Agent...\n" + "-"*50)
    
    df['agent_insight'] = df.apply(agentic_coaching_assistant, axis=1)
    
    for _, row in df.dropna(subset=['agent_insight']).iterrows():
        print(f"[AGENT INSIGHT] Period: {row['period']} | Event: {row['event']} | Player: {row['player_id']}")
        print(f"Insight: {row['agent_insight']}")
        print("-" * 50)


if __name__ == "__main__":
    raw_df = ingest_raw_hockey_data()
    gold_df = run_dbt_transformations(raw_df)
    execute_agent(gold_df)
