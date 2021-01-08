<template>
  <v-app>
    <Header></Header>
    <nuxt />
  </v-app>
</template>

<script>
import Header from '@/components/header'

export default {
  components: { Header },
}
</script>
