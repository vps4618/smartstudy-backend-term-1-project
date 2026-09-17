from fastapi import FastAPI , HTTPException
from schemas import SensorEvent,mock_db

app = FastAPI(title = "SmartStudy Backend")

# info page
@app.get("/")
def root():
    return {"status" : "SmartStudy API online"}

# gathering posted data and update db
@app.post("/api/sensor/event")
def handle_sensor_event(event_data : SensorEvent):
    area_id = event_data.area_id

    if area_id not in mock_db:
        raise HTTPException(status_code=404 , detail = "Study area not found")

    area = mock_db[area_id]

    if event_data.event == "ENTER":
        if area["current_occupancy"] < area["capacity"]:
            area["current_occupancy"] += 1
    elif event_data.event == "EXIT":
        if area["current_occupancy"] > 0:
            area["current_occupancy"] -= 1

    return {
        "status" : "success",
        "area_id" : area_id,
        "new_occupancy" : area["current_occupancy"]
    }

# displaying study area details
@app.get("/api/study-areas")
def get_study_areas():
    return mock_db

# displaying recommendations
@app.get("/api/recommendations")
def get_recommendations():
    results = []
    for area_id, data in mock_db.items():
        availability_ratio = (data["capacity"] - data["current_occupancy"]) / data["capacity"]
        
        # Calculate base score (adjust with actual DB metrics later)
        score = (0.40 * availability_ratio) + (0.15 * int(data["wifi"])) + (0.10 * int(data["power"]))
        
        results.append({"area_id": area_id, "score": score, "current_occupancy": data["current_occupancy"]})
    
    # Sort descending by score
    return sorted(results, key=lambda x: x["score"], reverse=True)