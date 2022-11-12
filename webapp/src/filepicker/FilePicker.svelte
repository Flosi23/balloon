<style type="text/css" media="screen">
 button {
     background: #6E7BF2;
     color: white;
     cursor: pointer;
     border: 1px solid white;
     border-radius: .375rem;
 }
 .upload {
     position: absolute;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     text-align: center;
     padding: 10px 20px;
     border-radius: .75rem;
     background: #282C31;
     color: white;
 }
</style>

<script>

 import { createEventDispatcher } from 'svelte';

 const dispatch = createEventDispatcher();

let data = [];

function pickFile() {
    let fr = new FileReader();


    fr.onload = (e) => {
        let rows = fr.result.split(/\r\n|\n/);
        for (let i = 0; i < rows.length - 1; i++) {
            data.push(rows[i].split(","));
        }

        dispatch('setlogs', data);
    }

    fr.readAsText(this.files[0]);
}
</script>

<div class="wrapper">
    <div class="upload">
        <h3 style="margin-top: 7.5px;">Logdatei hochladen</h3>
        <input type="file" on:change={pickFile} />
    </div>
</div>
