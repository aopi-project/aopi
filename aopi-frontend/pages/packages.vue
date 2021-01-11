<template>
  <div>Found packages by query: {{ query }}</div>
</template>

<script>
export default {
  name: 'Packages',
  computed: {
    query() {
      return this.$route.query.q || null
    },
  },
}
</script>
