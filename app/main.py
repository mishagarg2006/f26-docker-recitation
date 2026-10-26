from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

#TODO Fix recitation hours to be correct for this semester.
RECITATION_HOURS = {"a": "10:00~10:50", "b": "10:00~10:50",
                    "c": "01:00~01:50", "d": "01:00~01:50", 
                    "e": "02:00~02:50", "f": "02:00~02:50"}
MICROSERVICE_LINK = "https://cmu-313.github.io/section_info/"


@app.get("/section_info/{section_id}")
def get_section_info(section_id: str):

    if section_id is None:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    response = requests.get(MICROSERVICE_LINK + section_id + ".json")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Invalid section id")

    # You can check out what the response body looks like in terminal using the print statement
    data = response.json()
    print(data)
    # Note: some sections have only one TA
    ta_name_list = data["ta"]
    print(ta_name_list)

    # TODO Fix this to return correct values for correct sections.
    start_time, end_time = RECITATION_HOURS[section_id].split("~")
    if section_id in ["a", "b", "c", "d", "e", "f"]:
        return {
            "section": section_id,
            "start_time": start_time,
            "end_time": end_time,
            "ta": ta_name_list
        }
    else:
        raise HTTPException(status_code=404, detail="Invalid section id")
