<script>

import * as echarts from 'echarts';
import { onMount } from 'svelte';
import SensorSwitch from '../sensorswitch/SensorSwitch.svelte';

export let logs = [];

let sensorUnit = ["s", "hPA", "%", "°C", "%", "°C", "", "", "", "", "m"]
let sensorName = [
    "Laufende Sekunde", 
    "Druck",
    "Luftfeuchtigkeit (innen)",
    "Temperatur (innen)", 
    "Luftfeutichgkeit (außen)",
    "Temperatur (außen)",
    "Unix Timestamp",
    "GPS-Fix",
    "GPS-Satelliten",
    "GPS-Länge",
    "GPS-Breite",
    "Höhe"
]

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
let heights = [];
let fLogs = []; 

function formatDate(date){
    console.log(date)
    const hour = date.getHours()
    const minutes = date.getMinutes()
    return `${hour}:${minutes}`
}

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

    times = logs.map(row => formatDate(new Date(row[6] * 1000)))
    heights = logs.map(row => row[11])
    fLogs = [] // filtered logs
    
    logs.forEach(row => fLogs.push(row))
    
    changeSensor();
}

function changeSensor() {
    if (option && myChart) {
        option.xAxis.data = times;
        option.yAxis[1].name = sensorUnit[sensor];

        let data = [];
        for (let row of fLogs){
            data.push(row[sensor]);
        }

        option.series[1].data = data;
        option.series[1].name = sensorName[sensor]

        option.series[0].data = heights;

        myChart.setOption(option);
    }
}

onMount(() => {
    myChart = echarts.init(chart);

    option = {
        xAxis: {
            type: 'category',
        },
        yAxis: [
            {
                type: 'value',
                name: 'm',
                alignTicks: true,
            },
            {
                type: 'value',
                alignTicks: true,
            }
        ],
        tooltip: {
            trigger: 'axis'
        },
        series: [
            {
                name: "Höhe",
                yAxisIndex: 0,
                type: 'line',
                showSymbol: false,
            },
            {
                yAxisIndex: 1,
                type: 'line',
                showSymbol: false,
            }
        ], 
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

    input {
        background-color: inherit;
        color: white;
    }
</style>

<div class="wrapper">
    <nav>
        <h1 style="color: #eaeaea;font-size: 1.8rem;">Die 🎈 Louise</h1>
    </nav>

    <div class="content">
        <SensorSwitch bind:sensor={sensor} on:change={changeSensor} />
        <div style="position: relative; width: 100%; height: 70vh; overflow: hidden;" bind:this={chart}></div>
    </div>
</div>
