
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
     color: #999;
     border-radius: .5rem;
     display: flex;
     justify-content: center;
     align-items: center;
     margin: 10px;
     cursor: pointer;
     font-family: arial, sans-serif;
     font-weight: 500;
     background: rgba(255,255,255,0.007);
     transition: all ease .3s;
 }

 label:hover {
     background: rgba(255,255,255,0.01);
 }

 input:checked + label {
     background: #6755BE;
     color: white;
 }

 p {
     font-size: 1.1rem;
     text-transform: uppercase;
     padding-left: 1rem;
     color: #ccc;
 }
</style>

<script>

 import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let sensor = 0;

 $: sensor & dispatch('change', sensor);
</script>

<div style="background: #1E1F26; border-radius: .75rem;">
    <p style="margin-top: 30px;">S & J Datenlogger</p>

    <input id="pressure" type="radio" bind:group={sensor} name="sensor" value="1" />
    <label for="pressure">Druck</label>

    <input id="humidity-inside" type="radio" bind:group={sensor} name="sensor" value="2" />
    <label for="humidity-inside">Luftfeuchtigkeit (innen)</label>

    <input id="temp-inside" type="radio" bind:group={sensor} name="sensor" value="3" />
    <label for="temp-inside">Temperatur (innen)</label>

    <input id="humidity-outside" type="radio" bind:group={sensor} name="sensor" value="4" />
    <label for="humidity-outside">Luftfeuchtigkeit (außen)</label>

    <input id="temp-outside" type="radio" bind:group={sensor} name="sensor" value="5" />
    <label for="temp-outside">Temperatur (außen)</label>

    <input id="gps-height" type="radio" bind:group={sensor} name="sensor" value="11" />
    <label for="gps-height">GPS-Höhe</label>
</div>
