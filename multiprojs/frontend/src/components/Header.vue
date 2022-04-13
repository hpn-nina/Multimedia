<script setup>

</script>

<template>
  <header>
    <ul>
        <li><RouterLink to="/">HOME</RouterLink></li>
        <li><RouterLink to="/XMLLab">XML LAB</RouterLink></li>
    </ul>
  </header>
</template>

<style scoped>
ul {
  list-style: none;
}

ul > li {
  display: flex;
  flex: 1
}

a {
  text-decoration: none;
  color: white;
}
</style>
