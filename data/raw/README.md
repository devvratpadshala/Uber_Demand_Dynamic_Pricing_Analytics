# Raw Datasets

This directory contains the original, unprocessed public datasets obtained from open data repositories.

## Included Raw Datasets
1. **FiveThirtyEight NYC TLC Uber Trip Data (uber-raw-data-apr14-sample.csv)**
   - **Source:** FiveThirtyEight NYC TLC Freedom of Information Law (FOIL) repository
   - **URL:** https://github.com/fivethirtyeight/uber-tlc-foil-response
   - **Original License:** Creative Commons Attribution 4.0 International License (CC BY 4.0)
   - **Download Date:** October 2026
   - **Coverage:** April 2014 Uber pickups across New York City
   - **Columns:**
     - Date/Time: Timestamp of pickup (e.g., 4/1/2014 0:11:00)
     - Lat: Latitude of pickup location
     - Lon: Longitude of pickup location
     - Base: TLC base company dispatch licence code (e.g., B02512 Unter TLC base)
   - **Observation Count:** 100,000 real trip pickup records
   - **Limitation:** Contains exact pickup timestamps and geographic coordinates, but does not include fare amounts, trip durations, or actual surge multipliers (which are proprietary to Uber).
