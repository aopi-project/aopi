<template>
  <div class="w-100 search_page">
    <v-autocomplete
      flat
      rounded
      :autofocus="true"
      :clearable="true"
      :hide-no-data="true"
      :items="items"
      :search-input.sync="searchTerm"
      class="centered w-100 mw-60"
      label="Search packages"
      :append-icon="null"
      placeholder="Start typing to Search"
      prepend-icon="mdi-magnify"
      search-input.sync=""
      item-text="name"
      item-value="name"
      @keyup.13="raw_search"
      @change="search"
    >
      <template v-slot:item="data">
        <template>
          <v-list-item-avatar>
            <img
              :src="'languages/' + data.item.language.toLowerCase() + '.svg'"
            />
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ data.item.name }}</v-list-item-title>
          </v-list-item-content>
        </template>
      </template>
    </v-autocomplete>
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
      if (value === null || value.length < 2) {
        this.items = []
        return
      }
      const response = await this.$axios.get('/packages', {
        params: { page: 0, name: value, limit: 10 },
        progress: false,
      })
      this.items = response.data
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
    search(name) {
      this.$router.push(`/packages?q=${name}`)
    },
    raw_search() {
      this.search(this.searchTerm)
    },
  },
}
</script>

<style scoped>
.search_page {
  background-color: blue;
}
</style>

<style lang="scss">
.v-list {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}
</style>
