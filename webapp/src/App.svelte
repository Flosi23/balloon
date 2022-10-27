<script>
 	import FilePicker from "./filepicker/FilePicker.svelte";
 	import Dashboard from "./dashboard/Dashboard.svelte";
	export let name;

 	let picked = false;

    let logs;
 function setLogs(l) {
     //console.log(l.detail);
     logs = l.detail;
    picked = true;
 }

 function setType(t) {

 }
</script>

<main>
	{#if !picked}
		<FilePicker on:setType={setType} on:setlogs={setLogs} />
	{:else}
		<Dashboard logs={logs} />
	{/if}
</main>
