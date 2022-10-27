
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

export let sensor = 9;

 $: sensor & dispatch('change', sensor);
</script>

<div style="background: #1E1F26; border-radius: .75rem;">
    <p>Stratoflights Datenlogger</p>
    <input checked id="height" type="radio" bind:group={sensor} name="sensor" value="9" />
    <label for="height">Flughöhe</label>
    <input id="velocity" type="radio" bind:group={sensor} name="sensor" value="7" />
    <label for="velocity">Geschwindigkeit</label>
    <input id="temp" type="radio" bind:group={sensor} name="sensor" value="10" />
    <label for="temp">Temperatur</label>

    <p style="margin-top: 30px;">S & J Datenlogger</p>
    <input id="uv" type="radio" bind:group={sensor} name="sensor" value="2" />
    <label for="uv">UV-Intensität</label>
    <input id="actualTemp" type="radio" bind:group={sensor} name="sensor" value="0" />
    <label for="actualTemp">Temperatur (außen)</label>
    <input id="pressure" type="radio" bind:group={sensor} name="sensor" value="1" />
    <label for="pressure">Luftdruck</label>
    <input id="ir" type="radio" bind:group={sensor} name="sensor" value="3" />
    <label for="ir">Infrarot</label>
    <input id="visible" type="radio" bind:group={sensor} name="sensor" value="4" />
    <label for="visible">Sichtbares Licht</label>
</div>
