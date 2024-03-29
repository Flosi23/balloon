<script>

import * as echarts from 'echarts';
import { onMount } from 'svelte';
import SensorSwitch from '../sensorswitch/SensorSwitch.svelte';

export let logs = [];

let sensorUnit = ["s", "hPA", "%", "°C", "%", "°C", "", "", "", "", "", "m", "m"]
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
    "GPS-Höhe",
    "Berechnete Höhe"
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

let change1 = 0;
let change2 = 0;

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
        12 Computed Height
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
        option.yAxis[0].max = null;
        option.yAxis[1].max = null;
        option.yAxis[0].min = null;
        option.yAxis[1].min = null;
        option.yAxis[0].alignTicks = true;
        option.yAxis[1].alignTicks = true;

        option.xAxis.data = times;
        option.yAxis[yAxisIndex].name = sensorUnit[sensor];

        let data = [];
        for (let row of logs){
            data.push(row[sensor]);
        }

        if(sensorUnit[sensorOne] === sensorUnit[sensorTwo]){
            console.log("Units are the same")
            const dataSensorOne = logs.map((row) => row[sensorOne])
            const dataSensorTwo = logs.map((row) => row[sensorTwo])
            const dataCombined = dataSensorOne.concat(dataSensorTwo).filter(val => !isNaN(val));
            const max = Math.max(...dataCombined)
            let min = Math.min(...dataCombined)
            min = min > 0 ? 0 : min; 
            console.log("max", max)
            option.yAxis[0].max = max;
            option.yAxis[1].max = max;
            option.yAxis[0].min = min;           
            option.yAxis[1].min = min;
            option.yAxis[0].alignTicks = false;
            option.yAxis[1].alignTicks = false;
        }

        option.series[yAxisIndex].data = data;
        option.series[yAxisIndex].name = sensorName[sensor]

        console.log("option", option)

        myChart.setOption(option);
    }
}

onMount(() => {
    myChart = echarts.init(chart);

    option = {
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                }
            }
        },
        xAxis: {
            type: 'category',
        },
        yAxis: [
            {
                type: 'value',
                // alignTicks: true,
            },
            {
                type: 'value',
                // alignTicks: true,
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

     myChart.on("dataZoom", function(params) {
         let firstEntry = logs[params.batch[0].startValue];
         let lastEntry = logs[params.batch[0].endValue];
         if (!lastEntry) {
             change1 = 0;
             change2 = 0;
             return;
         }
         let seconds = (lastEntry[6] - firstEntry[6]);
         console.log("seconds", seconds);
         change1 = (lastEntry[sensorOne] - firstEntry[sensorOne]) / seconds * 60;

         if (sensorTwo > 1) {
             change2 = (lastEntry[sensorTwo] - firstEntry[sensorTwo]) / seconds * 60;
         } else {
             change2 = 0;
         }

     });

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
    .content {
        display: flex;
        flex-wrap: nowrap;
        max-width: 100vw;
    }

    .sensor-select {
        --background-color: var(--panel-bg);
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

        {#if change1 != 0}
            <p style="text-align: center; font-size: 1.5rem;">Veränderung:&nbsp; <span style="color: #c2c3fb;">{change1.toFixed(4)} {sensorUnit[sensorOne]}/min</span></p>
        {/if}
        {#if change2 != 0}
            <p style="text-align: center; font-size: 1.5rem;">Veränderung:&nbsp; <span style="color: rgb(169, 191, 150);">{change2.toFixed(4)} {sensorUnit[sensorTwo]}/min</span></p>
        {/if}
    </div>
    <div style="position: relative; width: 100%; height: 70vh; overflow: hidden;" bind:this={chart}></div>
</div>
