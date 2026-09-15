from fastapi import FastAPI , HTTPException
from schemas import SensorEvent

app = FastAPI(title = "SmartStudy Backend")

# In-memory storage for testing prototype logic
study_areas = {
    "LIBRARY 01" : {
        "name" : "Library 1st Floor",
        "capacity" : 50,
        "current_occupancy" : 20,
        "wifi_available" : True,
        "power_available" : True
    }
}

@app.get("/")
def root():
    return {"status" : "SmartStudy API online"}

@app.post("/api/sensor/event")
def handle_sensor_event(event_data : SensorEvent):
    area_id = event_data.area_id

    if area_id not in study_areas:
        raise HTTPException(status_code=404 , detail = "Study area not found")

    area = study_areas[area_id]

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

@app.get("/api/study-areas")
def get_study_areas():
    return study_areas

