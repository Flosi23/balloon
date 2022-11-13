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

let sensorOne = 1; // selected sensor data
let sensorTwo = 0;

let times = [];

let currentTab = 0;

function formatDate(date){
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

    changeSensorOne()
}

function changeSensorOne(){
    changeSensor(0,sensorOne)
}

function changeSensorTwo(){ 
    changeSensor(1,sensorTwo)
}

function changeSensor(yAxisIndex, sensor) {
    if (option && myChart) {
        option.xAxis.data = times;
        option.yAxis[yAxisIndex].name = sensorUnit[sensor];

        let data = [];
        for (let row of logs){
            data.push(row[sensor]);
        }

        option.series[yAxisIndex].data = data;
        option.series[yAxisIndex].name = sensorName[sensor]

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
                yAxisIndex: 0,
                type: 'line',
                showSymbol: false,
                lineStyle: {
                    color: sensorOneColor
                }
            },
            {
                yAxisIndex: 1,
                type: 'line',
                showSymbol: false,
                lineStyle: {
                    color: sensorTwoColor
                }
            }
        ], 
    };

    option && myChart.setOption(option);

})

function resizeGraph() {
    if (myChart)
        myChart.resize();
}

const sensorOneColor = "#6755BE"
const sensorTwoColor = "#a3be8c"
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

    .sensor-select {
        --background-color: #282C31;
        --border-radius: 10px;
        --border-width: 2px;
        background: var(--background-color);
        display: flex;
        flex-direction: column;
        border-radius: var(--border-radius);

        .tab {
            width: 100%;
            display: flex;
            justify-content: space-between;

            div {
                width: 50%;
                padding: 5px;
                text-align: center;
                font-size: larger;
                cursor: pointer;
                border: var(--border-width) solid var(--background-color);
                border-bottom: var(--border-width) solid var(--border-color);
                border-top-left-radius: var(--border-radius);
                border-top-right-radius: var(--border-radius);
            } 

            .selected {
                border: var(--border-width) solid var(--border-color);
                border-bottom: var(--border-width) solid var(--background-color);
            }
            
        }

        .tab-content {
            flex-grow: 1;
            padding: 12px;
            border: var(--border-width) solid var(--border-color);
            border-top: none;
            border-bottom-left-radius: var(--border-radius);
            border-bottom-right-radius: var(--border-radius);
        }
    }

     
</style>

<div class="wrapper">
    <nav>
        <h1 style="color: #eaeaea;font-size: 1.8rem;">Die 🎈 Louise</h1>
    </nav>

    <div class="content" style="--border-color: {currentTab == 0 ? sensorOneColor : sensorTwoColor}">
        <div class="sensor-select">
            <div class="tab">
                <div class="{currentTab == 0 ? "selected" : "" }" on:click={() => {currentTab = 0}}>Graph 1</div>
                <div class="{currentTab == 1 ? "selected" : ""}" on:click={() => {currentTab = 1}}>Graph 2</div>
            </div>
            <div class="tab-content"> 
                {#if currentTab == 0}
                    <SensorSwitch textColor="white" selectColor={sensorOneColor} id="0" bind:sensor={sensorOne} on:change={changeSensorOne} />
                {:else}
                    <SensorSwitch textColor="black" selectColor={sensorTwoColor}  id="1" bind:sensor={sensorTwo} on:change={changeSensorTwo} />
                {/if}
            </div>
        </div>
        <div style="position: relative; width: 100%; height: 70vh; overflow: hidden;" bind:this={chart}></div>
    </div>
</div>
