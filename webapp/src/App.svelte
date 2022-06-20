<script>
 	import FilePicker from "./filepicker/FilePicker.svelte";
 	import Dashboard from "./dashboard/Dashboard.svelte";
	export let name;

 	let picked = true;
</script>

<main>
	{#if !picked}
		<FilePicker />
	{:else}
		<Dashboard />
	{/if}
</main>
