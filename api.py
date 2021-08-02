import requests
from bs4 import BeautifulSoup
import html2text
import json
import re
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import os

def getData(apiUrl:str, params:set, dataType:dict):
    headers = {'Ocp-Apim-Subscription-Key': os.environ.get('ATAPI')}

    try:
        conn = http.client.HTTPSConnection('api.at.govt.nz')
        conn.request("GET", "{}?%s".format(apiUrl) % urllib.parse.urlencode(params), "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        
        jsonData = data.decode('utf-8')
        finalData = json.loads(jsonData)

        return finalData
    except Exception as e:
        print("[" + dataType + "]: " + e)
        return None


def getActiveNumber():
    data = getData("/v2/public/realtime/vehiclelocations", {}, "getActiveNumber")
    if (data != None):
        return len(data["response"]["entity"])
    else:
        return 0

def getRoute(routeID:str):
    data = getData("/v2/gtfs/routes/routeId/{}".format(routeID), {}, "getRoute")
    if (data != None):
        routes = data["response"][0]

        finalData = {}
        finalData["route_short_name"] = routes["route_short_name"]
        finalData["route_description"] = routes["route_long_name"]

        return finalData
    else:
        return None

def getStop(stopID:str):
    data = getData("/v2/gtfs/stops/stopId/{}".format(stopID), {}, "getRoute")
    if (data != None):
        stop = data["response"][0]["stop_name"]

        finalData = {}
        finalData["stop_name"] = stop

        return finalData
    else:
        return None

def getTrip(tripID:str, stopSequence:int):
    data = getData("/v2/gtfs/stopTimes/tripId/{}".format(tripID), {}, "getRoute")
    if (data != None):
        trips = data["response"]
        finalData = {}

        finalData["next_stop"] = None
        finalData["next_stop_time"] = None

        for i in range(0, len(trips)):
            if (trips[i]["stop_sequence"] == (stopSequence + 1)):
                finalData["next_stop"] = trips[i]["stop_id"].split("-")[0]
                finalData["next_stop_time"] = trips[i]["arrival_time"]
                break
        
        if (finalData["next_stop"] == None):
            finalData["next_stop"] = "End of Journey"
            finalData["next_stop_time"] = "N/A"

        return finalData
    else:
        return None

def getCombinedData(busRealID:str):
    data = getData("/v2/public/realtime".format(busRealID),  {"vehicleid": busRealID}, "getCombinedData")
    if (data != None or data != []):
        combinedData = data["response"]["entity"]
        finalData = {}
        
        finalData["trip_id"] = combinedData[0]["trip_update"]["trip"]["trip_id"]
        finalData["route_id"] = combinedData[0]["trip_update"]["trip"]["route_id"]
        finalData["stop_sequence"] = combinedData[0]["trip_update"]["stop_time_update"]["stop_sequence"]
        finalData["stop_id"] = combinedData[0]["trip_update"]["stop_time_update"]["stop_id"]
        
        tripData = getTrip(finalData["trip_id"], finalData["stop_sequence"] + 1)
        
        finalData["next_stop"] = tripData["next_stop"]
        finalData["next_stop_time"] = tripData["next_stop_time"]

        stopData = getStop(finalData["stop_id"])
        finalData["next_stop_name"] = stopData["stop_name"]

        routeData = getRoute(finalData["route_id"])
        finalData["route_short"] = routeData["route_short_name"]
        finalData["route_description"] = routeData["route_description"]

        finalData["latitude"] = combinedData[1]["vehicle"]["position"]["latitude"]
        finalData["longitude"] = combinedData[1]["vehicle"]["position"]["longitude"]
        finalData["speed"] = combinedData[1]["vehicle"]["position"]["speed"] * 3.6
        finalData["number_plate"] = combinedData[1]["vehicle"]["vehicle"]["license_plate"] # no

        return finalData
    else:
        return None

def getVehicle(vehicleID:str):
    newVehicleID = None

    if len(vehicleID.strip()) == 5:
        if vehicleID[:2].upper().strip() == "HE":
            newVehicleID = "HE0" + vehicleID[2:]
    else:
        newVehicleID = vehicleID
    newVehicleID = newVehicleID.upper()

    finalID = None
    
    data = getData("/v2/public/realtime/vehiclelocations", {}, "getVehicleID")
    if (data != None):
        vehicleData = data["response"]["entity"]
        for i in range(0, len(vehicleData)):
            try:
                if (vehicleData[i]["vehicle"]["vehicle"]["label"] != None):
                    if ("".join(vehicleData[i]["vehicle"]["vehicle"]["label"]).strip() == str(newVehicleID).strip()):
                        finalID = vehicleData[i]["vehicle"]["vehicle"]["id"]
                        break
            except Exception as e:
                pass
        
        if finalID != None:
            finalData = getCombinedData(finalID)
            finalData["id"] = newVehicleID

            if (len(newVehicleID) >= 3):
                if (len(newVehicleID) == 6):
                    if (newVehicleID[:3].isalpha()) and (newVehicleID[3:].isdigit()):
                        finalData["type"] = "train"
                    elif (newVehicleID[:2].isalpha()) and (newVehicleID[4:].isdigit()):
                        finalData["type"] = "bus"
                    else:
                        finalData["type"] = "ferry"
            return finalData
        else:
            return None
    else:
        return None