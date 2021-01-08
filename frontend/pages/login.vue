<template>
  <v-col class="centered">
    <v-row>a</v-row>
    <v-row>b</v-row>
  </v-col>
</template>

<script>
export default {
  name: 'Login',
}
</script>

<style scoped>
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-right: -50%;
  transform: translate(-50%, -50%);
}
</style>
