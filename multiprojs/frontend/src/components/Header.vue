<script setup>

</script>

<template>
  <header>
    <ul class="pb-2 pt-2">
        <li class="mr-2"><RouterLink to="/">HOME</RouterLink></li>
        <li class="mr-2"><RouterLink to="/html-lab">HTML LAB</RouterLink></li>
        <li class="mr-2"><RouterLink to="/xml-lab">XML LAB</RouterLink></li>
    </ul>
  </header>
</template>

<style scoped>
ul {
  list-style: none;
  background-color: black;
  display: flex;
}

ul > li {
  display: inline;
  flex: 1;
  justify-content: space-around;
}

ul > li:after {
  border-right: 1px solid white;
}

a {
  text-decoration: none;
  color: white;
}

a:hover {
  color: pink
}
</style>
