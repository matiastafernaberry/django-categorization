dato = request.rawGet(
          `/api/v1/bg/bg-documents-7-days-all-by-client/${campaign.project_id}/${hour.value}`,
          PROXY_URL,
      );
      
  return Promise.all([dato]).then(values => {
    console.log(values);
    return values;
    var myJsonString = JSON.stringify(values[0][0].data);
    var datoPost = axios.post('http://127.0.0.1:8000/keywordextract/', 
      myJsonString); 
    arrayReturn = values;
    console.log(arrayReturn);
    console.log(arrayReturn[0][0]);
    return values;
    return Promise.all([datoPost]).then(values => {
        console.log(values);
        //console.log(values[0]['config']['data']);JSON.parse(
        //var myJsonString = JSON.parse(values[0]['data']);
        var myJsonString = values[0]['data'];
        //myJsonString = "'" + myJsonString + "'";
        //myJsonString = JSON.stringify(myJsonString);
        myJsonString = myJsonString.replace(/"/g, '');
        myJsonString = myJsonString.replace(/'/g, '"');
        console.log(myJsonString);
        myJsonString = JSON.parse(myJsonString);
        console.log(myJsonString);
        //arrayReturn[0][0].data = myJsonString
        return arrayReturn;
      
    });
  });