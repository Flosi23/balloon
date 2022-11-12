<script>

import * as echarts from 'echarts';
import { onMount } from 'svelte';
import SensorSwitch from '../sensorswitch/SensorSwitch.svelte';

export let logs = [];

let sensorUnit = ["°C", "hPA", "Lux", "Lux", "Lux", "", "", "", "", "", "", "", "", "", ""]

$: {
    if (myChart) {}
    if (logs) {
    generateChartData();
    }
}

let chart; // dom element
let myChart; // echarts object
let option; // echarts options
let sensor = 9; // selected sensor data

let times = [];
let fLogs = []; 

function generateChartData() {
    /*
    The generated CSV has the form: 
        0  Running second,
        1  Pressure,
        2  Humidity inside,
        3  Temperature inside,
        4  Humidity outside,
        5  Temperature outside,
        6  Unix timestamp,
        7  GPS-Fix,
        8  GPS-Satellites,
        9  GPS-Length,
        10 GPS-Width,
        11 GPS-Height
    If a value was not recorded, the fields value will instead be "--.---"
    */

    times = logs.map(row => row[6])
    fLogs = [] // filtered logs
    
    logs.forEach(row => fLogs.push(row))
    
    changeSensor();
}

function changeSensor() {
    if (option && myChart) {
        option.xAxis.data = times;
        option.yAxis.name = sensorUnit[sensor];

        let data = [];
        for (let row of fLogs){
            data.push(row[sensor]);
        }
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
