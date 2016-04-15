# factory-city
50 factories and 32 cities lat and long are given in the attached excel.  We have to assign only 2 factories per city.

Solution: find nearest two factories for each city and assign.
This might result in few factories never getting assigned.
We solve that by finding nearest city to these factories and assigning them as a factory for that city and removing the further of the two already assigned city.
