<script>
	import Dashboard from "./dashboard/Dashboard.svelte";
	import { onMount } from "svelte";

	let fetched = false;
	
	let logs = [];

	let darkMode = true;

	async function fetchCSV() {
		const res = await fetch("/data.csv")
		const csv = await res.text()	

		let rows = csv.split(/\r\n|\n/)
        for (let i = 0; i < rows.length - 1; i++) {
            logs.push(rows[i].split(","))
        }

		fetched = true
	}

	function loadColorModeSetting(){
		const colorModeStorageItem = localStorage.getItem("colorMode")
		if(colorModeStorageItem == null){
			return;
		}
		darkMode = (colorModeStorageItem === "dark")	
	}

	function setColorModeSetting(){
		localStorage.setItem("colorMode", darkMode ? "dark" : "light")
	}

	
	onMount(() => {
		fetchCSV()
		loadColorModeSetting()
	})

	function toggleColorMode(){
		darkMode = !darkMode
		setColorModeSetting()	
	}
</script>

<style lang="scss">
	:global(*) {
		transition-property: color, background-color, border-color;
		transition-timing-function: ease;
		transition-duration: .2s;
	}

	:global(body) {
		padding: 0;
	}

	:global(main) {
		color: var(--text-color);
		background: var(--page-bg);
		width: 100vw;
		height: 100vh;
	}

	:global(.site-dark) {
		--page-bg: #1F222A; 
		--panel-bg: #282C31;
		--btn-bg: #1A1C22;
		--btn-bg-hover: rgba(255,255,255,0.01);
		--text-color: white;
		--text-soft-color: #999;
	}

	:global(.site-light){
		--page-bg: white;
		--panel-bg: #e5e9f0;
		--btn-bg: white;
		--btn-bg-hover: #eceff4;
		--text-color: black;
		--text-soft-color: #4c566a;
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
        box-sizing: border-box;
        align-items: center; 

		h1{
			margin-left: 20px;
			font-size: 1.8rem;
		}

		span {
			cursor: pointer;
		}	
    }	
</style>

<svelte:head>
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0" />
</svelte:head>

<main class="{darkMode ? "site-dark" : "site-light"}">
	<div class="wrapper">
		<nav>
			<h1>Die 🎈 Louise</h1>
			<span class="material-symbols-outlined" on:click={toggleColorMode}>
				{darkMode ? "light_mode" : "dark_mode"}
			</span>
		</nav>
		{#if fetched}
			<Dashboard logs={logs} />
		{/if}
	</div>
</main>
