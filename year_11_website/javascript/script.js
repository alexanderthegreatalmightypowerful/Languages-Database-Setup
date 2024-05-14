function sendData() { 
  var value = document.getElementById('submit_code').value; 
  console.log('Sending Data: ' + value);
  const url = 'http://127.0.0.1:5000/get_data'; 
  var mode = 'POST'; 
  var data = {'data' : value};
  var table = document.getElementById('data_table')
  //let gotton = fetch(url, {
   // 'method' : mode,
   // 'body' : data,
   // 'mode' : 'no-cors'
  //});
  $.ajax({
        url: url,
        method: mode,
        data: data,
        crossDomain: false,
        mode : 'no-cors',
        dataType : 'json',
      }).done(function (data) {
        console.log(data['columns']);
        console.log(data['data']);
        var table_data = data;

        var tables = {};
        var table_data_holder = [];
        var data_string = '<tr>';
        for(var column in data['columns']){
          data_string += '<th>' + data['columns'][column] + '</th>';
          tables[data['columns'][column]] = [];
          console.log(data['columns'][column]);
        }
        data_string += '</tr>';
        console.log(data['data']);
        
        for(var item in data['rows']){
          data_string += '<tr>';
          for(value in data['rows'][item]){
            data_string += "<td>" + data['rows'][item][value] +"</td>";
            console.log(data['rows'][item][value]);
          }
          data_string += '</tr>';
        }
        
        data_string = data_string + '</tr>'
        console.log(data_string);

        table.innerHTML = data_string;
      

      }).fail(function (error) {
        alert(error);
      });

}