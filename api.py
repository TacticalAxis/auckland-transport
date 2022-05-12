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
    combinedData = None
    if (data != None or data != []):
        try:
            combinedData = data["response"]["entity"]
            hasTrip = False
            finalData = {}

            if len(combinedData) == 1:
                finalData["latitude"] = str(combinedData[0]["vehicle"]["position"]["latitude"])
                finalData["longitude"] = str(combinedData[0]["vehicle"]["position"]["longitude"])
                finalData["speed"] = combinedData[0]["vehicle"]["position"]["speed"]
                finalData["label"] = "".join(combinedData[0]["vehicle"]["vehicle"]["label"].split())

                finalData["trip_id"] = "Not in service"
                finalData["route_id"] = "Not in service"
                finalData["stop_sequence"] = 0
                finalData["stop_id"] = "Not in service"
                
                finalData["next_stop"] = "N/A"
                finalData["next_stop_time"] = "N/A"

                finalData["next_stop_name"] = "N/A"

                finalData["route_short"] = finalData["label"]
                finalData["route_description"] = "Not in service"
            elif len(combinedData) == 2:
                finalData["latitude"] = str(combinedData[1]["vehicle"]["position"]["latitude"])
                finalData["longitude"] = str(combinedData[1]["vehicle"]["position"]["longitude"])
                finalData["speed"] = combinedData[1]["vehicle"]["position"]["speed"]
                finalData["label"] = "".join(combinedData[1]["vehicle"]["vehicle"]["label"].split())

                finalData["trip_id"] = str(combinedData[0]["trip_update"]["trip"]["trip_id"])
                finalData["route_id"] = str(combinedData[0]["trip_update"]["trip"]["route_id"])
                finalData["stop_sequence"] = combinedData[0]["trip_update"]["stop_time_update"]["stop_sequence"]
                finalData["stop_id"] = str(combinedData[0]["trip_update"]["stop_time_update"]["stop_id"])
            
                tripData = getTrip(finalData["trip_id"], finalData["stop_sequence"] + 1)
                
                finalData["next_stop"] = str(tripData["next_stop"])
                finalData["next_stop_time"] = str(tripData["next_stop_time"])

                stopData = getStop(finalData["stop_id"])
                finalData["next_stop_name"] = str(stopData["stop_name"])

                routeData = getRoute(finalData["route_id"])
                finalData["route_short"] = str(routeData["route_short_name"])
                finalData["route_description"] = str(routeData["route_description"])
            return finalData
        except Exception as e:
            print("e" + str(e))
    else:
        return None

def getVehicle(vehicleID:str):
    newVehicleID = None

    if len(vehicleID.strip()) == 5:
        if vehicleID[:2].upper().strip() == "HE":
            newVehicleID = "HE0" + vehicleID[2:]
    else:
        newVehicleID = vehicleID
    newVehicleID = "".join(newVehicleID.upper().strip().split()).strip()
    print(newVehicleID)

    finalID = None
    
    data = getData("/v2/public/realtime/vehiclelocations", {}, "getVehicleID")
    if (data != None):
        vehicleData = data["response"]["entity"]
        for i in range(0, len(vehicleData)):
            try:
                if (vehicleData[i]["vehicle"]["vehicle"]["label"] != None):
                    compare = "".join(vehicleData[i]["vehicle"]["vehicle"]["label"].split()).strip()
                    # print(compare + ": " + newVehicleID)
                    if (compare == newVehicleID):
                        finalID = vehicleData[i]["vehicle"]["vehicle"]["id"]
                        break
            except Exception as e:
                pass
        
        if finalID != None:
            finalData = getCombinedData(finalID)
            if finalData != None:

                finalData["type"] = None
                finalData["id"] = newVehicleID
                if (len(newVehicleID) >= 3):
                    if (len(newVehicleID) == 6):
                        if (newVehicleID[:3].isalpha()) and (newVehicleID[3:].isdigit()):
                            finalData["type"] = "train"
                        elif (newVehicleID[:2].isalpha()) and (newVehicleID[4:].isdigit()):
                            finalData["type"] = "bus"
                        else:
                            finalData["type"] = "ferry"
                if finalData["type"] == None:
                    finalData["type"] = "ferry"
                return finalData
            else:
                return None
        else:
            return None
    else:
        return None

def getStopInfo(stopID:str, max:int):
    data = getData("/v2/gtfs/stops/stopinfo/{}".format(stopID),  {}, "getStopInfo")
    finalData = []
    if data != None:
        count = 0
        for i in data["response"]:
            finalData.append(i)
            count += 1
            if count == max:
                break
    else:
        return None
    
    return finalData