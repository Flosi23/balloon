<script>

 import * as echarts from 'echarts';
 import { onMount } from 'svelte';
 import SensorSwitch from '../sensorswitch/SensorSwitch.svelte';
 import debounce from 'lodash/debounce';

 //export let clogs = []; // custom logs (from our own logger)
 export let logs = [];

 let logType = 0;

 let sensorUnit = ["°C", "hPA", "Lux", "Lux", "Lux", "", "", "", "", "", "", "", "", "", ""]

 $: {
     if (myChart) {}
     if (logs) {
         if (logs[0].length > 10) {
             generateChartData();
             logType = 0;
         } else {
             generateCChartData();
             logType = 1;
         }
     }
 }

 /*$: {
     if (myChart) {}
     if (clogs) console.log("clogs working", clogs);
 }*/

 let chart; // dom element
 let myChart; // echarts object
 let option; // echarts options
 let sensor = 9; // selected sensor data

 $: sensor & console.log("sensor is", sensor);

 let times = [];
 let fLogs = [];

 function generateCChartData() {
     //logs = logs.map(m => {m[0] = m[0].split("").length > 1 ?  m[0].split(" ")[1] : m[0]; return m;});

     for (let i = 0; i < logs.length; i++) {
         if (logs[i][0].split(" ").length == 2) {
             logs[i][0] = logs[i][0].split(" ")[1];
             logs[i][0] = logs[i][0].split(".")[0];
             //console.log(logs[i]);
             times.push(logs[i].shift());
         }

         for (let j = 1; j < logs[i].length; j++) {
             logs[i][j] = (+logs[i][j]).toFixed(2);
         }

     }

     //console.log(logs);
     fLogs = logs;

     changeSensor();

 }

 function generateChartData() {

     // Format: Uhrzeit [0], Datum [1], Sensorenaktiv [2], Satelliten (anzahl) [3], Breitengrad [4], Längengrad [5],
     // Geschwindigkeit (in Knoten) [6], Geschwindigkeit (in km/h) [7], Kurs über Boden [8],
     // Höhe [9], Bordtemperatur [10], Batteriespannung [11], Loggerstatus [12]



     // Custom logger format:
     // Temperatur [0], Luftdruck [1], UV [2], IR [3], Sichtbar [4]


     times = logs.map(m => { m.shift(); return m[0]; });
     fLogs = []; // filtered logs
     fLogs.push(logs[0]);

     let start = 0;
     let end = 1;

     while (end < times.length) {
         var dif = ( new Date("1970-1-1 " + times[end]) - new Date("1970-1-1 " + times[start]) ) / 1000;
         if (dif < 2 && end < times.length - 1) {
             end++;
         } else {
             fLogs.push(logs[end]);
             start = end;
             end++;
         }
     }

     fLogs = fLogs.filter(f => f[2] == "Y");
     times = fLogs.map(m => { return m[0]; }); // get times from new logs

     console.log("filtered Logs", fLogs);


     for (let i = 0; i < fLogs.length - 1; i++) {
         //var dif = ( new Date("1970-1-1 " + end-time) - new Date("1970-1-1 " + start-time) ) / 1000 / 60 / 60;
         var dif = ( new Date("1970-1-1 " + times[i + 1]) - new Date("1970-1-1 " + times[i]) ) / 1000;
         console.log("dif of " + times[i + 1] + " and " + times[i], dif);
         i++;
     }

     /*if (option && myChart) {
         option.xAxis.data = times;

         let data = [];
         for (let row of fLogs) data.push(row[10]);
         console.log("data", data);
         option.series[0].data = data;
         myChart.setOption(option);
     }*/
     changeSensor();


 }

 function changeSensor() {
     console.log("sensor in ssD", sensor);
     if (option && myChart) {
         option.xAxis.data = times;
         option.yAxis.name = sensorUnit[sensor];

         let data = [];
         for (let row of fLogs) data.push(row[sensor]);
         //console.log("data", data);
         option.series[0].data = data;
         myChart.setOption(option);
     }
 }


 onMount(() => {
     myChart = echarts.init(chart);

    option = {
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
        type: 'value'
    },
    tooltip: {
        trigger: 'axis'
    },
    series: [
        {
        data: [150, 230, 224, 218, 135, 147, 260],
        type: 'line'
        }
    ]
    };

    option && myChart.setOption(option);

 })

 function resizeGraph() {
        if (myChart)
            myChart.resize();
 }
</script>


<svelte:window on:resize={resizeGraph} />

<svelte:head>
    <link href="https://fonts.googleapis.com/css2?family=Shadows+Into+Light&family=Teko&display=swap" rel="stylesheet">
</svelte:head>

<style lang="scss">
 * {
     color: white;
 }
 .wrapper {
     padding: 0 20px;
     font-family: 'Teko', sans-serif;
 }
 nav {
     width: 100%;
     height: auto;
     display: flex;
     justify-content: space-between;
     padding: 0 20px;
     box-sizing: border-box;
     align-items: center;

     p {
         font-size: 1.2rem;
     }
 }
 .content {
     display: flex;
     flex-wrap: nowrap;
     max-width: 100vw;
 }
</style>

<div class="wrapper">
    <nav>
        <h1 style="color: #eaeaea;font-size: 1.8rem;">Die 🎈 Louise</h1>
        <p>Flug: 17.06.22 11:00 - 15:00</p>
    </nav>

    <div class="content">
        <SensorSwitch bind:sensor={sensor} on:change={changeSensor} />
        <div style="position: relative; width: 100%; height: 70vh; overflow: hidden;" bind:this={chart}></div>
    </div>
</div>
