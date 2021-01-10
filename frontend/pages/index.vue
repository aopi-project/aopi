<template>
  <div class="w-100 search_page">
    <v-autocomplete
      :search-input.sync="searchTerm"
      :items="items"
      :loading="isLoading"
      :autofocus="true"
      :clearable="true"
      :hide-no-data="true"
      class="centered w-100 mw-60"
      label="Search packages"
      placeholder="Start typing to Search"
      prepend-icon="mdi-magnify"
      search-input.sync=""
      @change="search"
    ></v-autocomplete>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoading: false,
      items: [],
      searchTerm: null,
    }
  },
  watch: {
    async searchTerm(value) {
      const response = await this.$axios.get('/packages', {
        params: { page: 0, name: value, limit: 10 },
      })
      this.items = response.data.map((item) => item.name)
    },
  },
  async mounted() {
    if (this.$backend_settings.usersEnabled && !this.$auth.loggedIn) {
      await this.$router.push('/login')
    }
  },
  methods: {
    async logout() {
      await this.$auth.logout()
      await this.$router.push('/login')
    },
    search(name) {},
  },
}
</script>

<style scoped>
.search_page {
  background-color: blue;
}
</style>
