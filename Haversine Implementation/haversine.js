
function haversineDistance(latA, lonA, latB, lonB){
        // convert latitude and longitude from degree to rad
        latA = (latA) * Math.PI/180.0;
        lonA = (lonA) * Math.PI/180.0;
        latB = (latB) * Math.PI/180.0;
        lonB = (lonB) * Math.PI/180.0;
        
        latDif = latB-latA;
        lonDif = lonB-lonA;
        
        let radius = 6371;
        let initialDistance = Math.pow(Math.sine(latDif/2),2) +Math.pow(Math.sin(lonDif/2),2) * Math.cos(latA)*Math.cos(latB);
        let finalDistance = 2 * radius * Math.asin(Math.sqrt(initialDistance));
        return finalDistance
}