
<style type="text/scss">
 input {
     cursor: none;
     opacity: 0;
     position: absolute;
     z-index: -1;
 }

 label {
    width: 250px;
    height: 45px;
    color: var(--text-soft-color);
    border-radius: .5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 10px 0;
    cursor: pointer;
    font-family: arial, sans-serif;
    font-weight: 500;
    background: var(--btn-bg);
 }

 label:hover {
     background: var(--btn-bg-hover);
 }

 input:checked + label {
     background: var(--select-color);
     color: var(--text-color);
 } 
</style>

<script>

 import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let sensor = 0;
export let id = "0"
export let selectColor = ""
export let textColor = ""

 $: sensor & dispatch('change', sensor);
</script>

<div style="
    --select-color: {selectColor};
    --text-color: {textColor};
">
    <input id="pressure-{id}" type="radio" bind:group={sensor} name="sensor{id}" value="1" />
    <label for="pressure-{id}">Druck</label>

    <input id="humidity-inside-{id}" type="radio" bind:group={sensor} name="sensor{id}" value="2" />
    <label for="humidity-inside-{id}">Luftfeuchtigkeit (innen)</label>

    <input id="temp-inside-{id}" type="radio" bind:group={sensor} name="sensor{id}" value="3" />
    <label for="temp-inside-{id}">Temperatur (innen)</label>

    <input id="humidity-outside-{id}" type="radio" bind:group={sensor} name="sensor{id}" value="4" />
    <label for="humidity-outside-{id}">Luftfeuchtigkeit (außen)</label>

    <input id="temp-outside-{id}" type="radio" bind:group={sensor} name="sensor{id}" value="5" />
    <label for="temp-outside-{id}">Temperatur (außen)</label>

    <input id="gps-height-{id}" type="radio" bind:group={sensor} name="sensor{id}" value="11" />
    <label for="gps-height-{id}">GPS-Höhe</label>

    <input id="comp-height-{id}" type="radio" bind:group={sensor} name="sensor{id}" value="12" />
    <label for="comp-height-{id}">Berechnete Höhe</label>
</div>
