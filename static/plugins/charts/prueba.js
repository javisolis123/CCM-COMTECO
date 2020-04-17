var chartTemperatue;
var chartHumidity;

        function requestData() {
            // Ajax call to get the Data from Flask
            var requests = $.get('/datos');

            var tm = requests.done(function (result) {
                // Temperature
                var seriesTemperature = chartTemperatue.series[0],
                    shiftTemperature = seriesTemperature.data.length > 20;

                // Humidity
                var seriesHumidity = chartHumidity.series[0],
                    shiftHumidity = seriesTemperature.data.length > 20;

                // Add the Point
                // Time Temperature\
                var data1 = [];
                data1.push(result[0]);
                data1.push(result[3]);


                // Add the Point
                // Time Humidity
                var data2 = [];
                data2.push(result[0]);
                data2.push(result[4]);


                chartTemperatue.series[0].addPoint(data1, true, shiftTemperature);
                chartHumidity.series[0].addPoint(data2, true, shiftHumidity);

                //Cuadro 1x1
                $(".TRtemperatura").text("");
                $(".TRtemperatura").text("Temperatura: " + result[1] + "°C");
                $(".TRhumedad").text("");
                $(".TRhumedad").text("Humedad: " + result[2] + "%");

                //Cuadro 1x2
                $(".TRch1").text("");
                $(".TRch1").text("Actual: " + result[3] + " [V]");
                $(".TRch1max").text("");
                $(".TRch1max").text("Máxima: " + result[9] + " [V]");
                $(".TRch1min").text("");
                $(".TRch1min").text("Mínima: " + result[10] + " [V]");

                //Cuadro 1x3
                $(".TRch2").text("");
                $(".TRch2").text("Actual: " + result[4] + " [V]");
                $(".TRch2max").text("");
                $(".TRch2max").text("Máxima: " + result[11] + " [V]");
                $(".TRch2min").text("");
                $(".TRch2min").text("Mínima: " + result[12] + " [V]");

                //Cuadro 2x1
                $(".PromTemp").text("");
                $(".PromTemp").text("Temperatura: " + result[15] + "°C");
                $(".PromHum").text("");
                $(".PromHum").text("Humedad: " + result[16] + "%");

                //Cuadro 2x2
                $(".Tmaxima").text("");
                $(".Tmaxima").text("Temperatura Máxima: " + result[7] + "°C");
                $(".Tminima").text("");
                $(".Tminima").text("Temperatura Mínima: " + result[8] + "°C");
                $(".Hmaxima").text("");
                $(".Hmaxima").text("Humedad Máxima: " + result[13] + "%");
                $(".Hminima").text("");
                $(".Hminima").text("Humedad Mínima: " + result[14] + "%");

                //Cuadro 1x3
                $(".TempGabinete").text("");
                $(".TempGabinete").text("Temperatura: " + result[4] + " [V]");
                $(".voltajeDC").text("");
                $(".voltajeDC").text("Voltaje DC: " + result[5] + " [VDC]");
                $(".voltajeAC").text("");
                $(".voltajeAC").text("Voltaje AC: " + result[6] + " [VAC]");
                
                // call it again after one second
                setTimeout(requestData, 5000);
            });
        }

        $(document).ready(function () {
            // --------------Chart 1 ----------------------------
            chartTemperatue = new Highcharts.Chart({
                chart:
                {
                    renderTo: 'data-temperature',
                    defaultSeriesType: 'area',
                    events: {
                        load: requestData
                    }
                },
                title:
                {
                    text: 'Potencia de Recepcion Principal'
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 150,
                    maxZoom: 20 * 1000
                },
                yAxis: {
                    minPadding: 0.2,
                    maxPadding: 0.2,
                    title: {
                        text: 'Voltaje',
                        margin: 80
                    }
                },
                series: [{
                    color: '#c23d23',
                    lineColor: '#303030',
                    name: 'Potencia Recibida',
                    data: []
                }]
            });
            // --------------Chart 1 Ends - -----------------

            chartHumidity = new Highcharts.Chart({
                chart:
                {
                    renderTo: 'data-humidity',
                    defaultSeriesType: 'area',
                    events: {
                        load: requestData
                    }
                },
                title:
                {
                    text: 'Potencia de Recepcion Secundaria'
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 150,
                    maxZoom: 20 * 1000
                },
                yAxis: {
                    minPadding: 0.2,
                    maxPadding: 0.2,
                    title: {
                        text: 'Voltaje',
                        margin: 80
                    }
                },
                series: [{
                    lineColor: '#1d82b8',
                    name: 'Potencia Recibida',
                    data: []
                }]
            });


        });