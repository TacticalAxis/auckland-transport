# The [Unofficial] Auckland Transport Discord Bot

## About

This is the repository for The [Unofficial] Auckland Transport Discord Bot. While this bot is still in alpha development, the first preview is now functional with a working command: /locate

The aim of this Discord Bot is to provide users on the Discord platform a way to access Auckland Transport's real-time vehicle and bus stop information. Since Discord is supported on many platforms, this bot is available on those same platforms.

Since this bot is currently in a very early development stage, it is not available to the public to be added to their personal servers.

## Commands

> /locate <_vehicleID_>

Through the use of the Vehicle ID system (i.e. AMP129 - train, or RT1303 - bus), using this in combination with the /locate command on a server with this bot, it displays the relevant information for that vehicle.

Both buses and trains show the route short name (i.e EAST - train, or 95C - bus), the route description, current location, speed, and next-stop information. This is only available for buses and trains, as they go from stop to stop, since ferries travel from a departure location directly to an arrival location. The next-stop information shows the stop number, location, and estimated time of arrival

![Train Usage](https://github.com/TacticalAxis/auckland-transport/blob/main/images/demo/image1.PNG)
